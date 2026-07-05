import logging

from flask import Flask, jsonify, request

from config import DEBUG, HOST, PORT
from signal_parser import validate
from state import can_trade, get_status, update_pnl
from bybit_api import execute
from telegram import send_error, send_status, send_trade
from strategy_wrapper import execute_strategy

# 👉 추가 (트레이드 저장)
from trade_db import init_db, insert_trade


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


# =====================================================
# INIT DB
# =====================================================

init_db()


# =====================================================
# ROUTES
# =====================================================

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


@app.route("/pnl")
def pnl():
    return jsonify(get_status())


@app.route("/dashboard")
def dashboard():
    return """
    <html>
    <head>
        <title>Trading Bot</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body style="background:#0f172a;color:white;text-align:center;">
        <h1>Trading Bot Dashboard</h1>
        <p>Status: RUNNING</p>
        <p>Check /pnl</p>
    </body>
    </html>
    """


# =====================================================
# WEBHOOK
# =====================================================

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
            return jsonify({"error": "Rate limit exceeded"}), 429

        signal = result["signal"]
        symbol = result["symbol"]
        qty = result["qty"]
        price = result["price"]

        # =================================================
        # STRATEGY ENGINE
        # =================================================

        decision = execute_strategy(signal, price)

        if not decision["success"]:

            logger.info(
                "FILTERED | reason=%s | signal=%s",
                decision["reason"],
                signal,
            )

            return jsonify({
                "status": "filtered",
                "reason": decision["reason"],
                "strategy": decision["strategy"],
                "regime": decision["regime"],
            })

        final_signal = signal

        logger.info(
            "EXECUTE | signal=%s | strategy=%s | regime=%s",
            final_signal,
            decision["strategy"],
            decision["regime"],
        )

        # =================================================
        # ORDER EXECUTION
        # =================================================

        order = execute(final_signal, symbol, qty)

        if not order.get("success", False):

            send_error(order.get("error", "Unknown error"))

            return jsonify(order), 500

        # =================================================
        # SUCCESS ACTIONS
        # =================================================

        send_trade(final_signal, symbol, qty, price)

        insert_trade(symbol, final_signal, qty, price, 0)

        # (선택) pnl 업데이트 - 현재 단순 구조
        update_pnl(0)

        logger.info(
            "TRADE DONE | %s %s %s",
            final_signal,
            symbol,
            qty
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


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    logger.info("Starting Trading Bot...")

    send_status("🚀 Trading Bot Started")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG,
    )
