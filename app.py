import logging

from flask import Flask, jsonify, request

from bybit_api import execute
from config import DEBUG, HOST, PORT
from rl_predictor_dqn import decide
from signal_parser import validate
from state import can_trade, get_status
from telegram import send_error, send_status, send_trade

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

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
            return jsonify({
                "error": "Invalid JSON."
            }), 400

        ok, result = validate(data)

        if not ok:
            return jsonify({
                "error": result
            }), 400

        if not can_trade():
            return jsonify({
                "error": "Rate limit exceeded."
            }), 429

        tv_signal = result["signal"]
        symbol = result["symbol"]
        qty = result["qty"]
        price = result["price"]

        ai_action = decide(price)

        action_map = {
            0: "HOLD",
            1: "BUY",
            2: "SELL"
        }

        ai_signal = action_map.get(ai_action, "HOLD")

        logger.info(
            "TV=%s AI=%s SYMBOL=%s QTY=%s PRICE=%s",
            tv_signal,
            ai_signal,
            symbol,
            qty,
            price
        )

        if ai_signal == "HOLD":

            return jsonify({
                "status": "hold",
                "reason": "AI HOLD"
            })

        if ai_signal != tv_signal:

            logger.info("Signal filtered.")

            return jsonify({
                "status": "filtered",
                "tv_signal": tv_signal,
                "ai_signal": ai_signal
            })

        order = execute(
            ai_signal,
            symbol,
            qty
        )

        if not order.get("success", False):

            send_error(order.get("error", "Unknown Error"))

            return jsonify(order), 500

        send_trade(
            ai_signal,
            symbol,
            qty,
            price
        )

        return jsonify({
            "status": "success",
            "order": order
        })

    except Exception as e:

        logger.exception(e)

        send_error(str(e))

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    logger.info("Starting Bybit AI Trading Bot...")

    send_status("🚀 Bybit AI Trading Bot Started")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
