import logging

from flask import Flask, jsonify, request

from bybit_api import execute
from config import DEBUG, HOST, PORT
from signal_parser import validate
from state import can_trade, get_status
from telegram import send_error, send_status, send_trade

from strategy_wrapper import execute_strategy


# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


# =====================================================
# Flask App
# =====================================================

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "name": "Bybit AI Trading Bot",
        "version": "2.0",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "trade": get_status()
    })


@app.route("/webhook", methods=["POST"])
def webhook():

    try:

        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400

        ok, result = validate(data)

        if not ok:
            return jsonify({"error": result}), 400

        if not can_trade():
            return jsonify({"error": "Rate limit"}), 429

        signal = result["signal"]
        symbol = result["symbol"]
        qty = result["qty"]
        price = result["price"]

        # =================================================
        # CORE DECISION ENGINE (Strategy Wrapper)
        # =================================================

        decision = execute_strategy(signal, price)

        if not decision["success"]:

            logger.info(
                "Filtered | reason=%s | signal=%s",
                decision["reason"],
                signal,
            )

            return jsonify({
                "status": "filtered",
                "reason": decision["reason"],
                "strategy": decision["strategy"],
                "regime": decision["regime"],
            })

        final_signal = signal  # TV signal 기준 실행

        logger.info(
            "EXECUTE | signal=%s | strategy=%s | regime=%s",
            final_signal,
            decision["strategy"],
            decision["regime"],
        )

        # =================================================
        # ORDER EXECUTION
        # =================================================

        order = execute(
            final_signal,
            symbol,
            qty,
        )

        if not order.get("success", True):

            send_error(order.get("error", "Unknown Error"))

            return jsonify(order), 500

        send_trade(
            final_signal,
            symbol,
            qty,
            price,
        )

        return jsonify({
            "status": "success",
            "strategy": decision["strategy"],
            "regime": decision["regime"],
            "order": order,
        })

    except Exception as e:

        logger.exception(e)

        send_error(str(e))

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    logger.info("Starting Bybit AI Trading Bot...")

    send_status("🚀 Bot Started")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG,
    )
