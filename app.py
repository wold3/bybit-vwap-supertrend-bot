import logging

from flask import Flask, request, jsonify

from config import HOST, PORT, DEBUG
from signal_parser import validate
from rl_predictor_dqn import decide
from bybit_api import execute
from state import can_trade

try:
    from telegram import send
except ImportError:
    def send(message):
        pass


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "name": "Bybit AI Trading Bot",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "bybit-ai-bot"
    })


@app.route("/webhook", methods=["POST"])
def webhook():

    try:

        data = request.get_json(silent=True)

        if data is None:
            return jsonify({
                "error": "invalid json"
            }), 400

        ok, result = validate(data)

        if not ok:
            return jsonify({
                "error": result
            }), 400

        if not can_trade():
            return jsonify({
                "error": "rate_limit"
            }), 429

        symbol = result["symbol"]
        qty = result["qty"]

        price = float(data.get("price", 0))

        action = decide(price)

        if action == 0:

            logging.info("HOLD %s", symbol)

            return jsonify({
                "action": "HOLD"
            })

        if action == 1:

            response = execute("BUY", symbol, qty)

            logging.info("BUY %s %.6f", symbol, qty)

            send(f"BUY {symbol} qty={qty}")

            return jsonify({
                "action": "BUY",
                "result": response
            })

        if action == 2:

            response = execute("SELL", symbol, qty)

            logging.info("SELL %s %.6f", symbol, qty)

            send(f"SELL {symbol} qty={qty}")

            return jsonify({
                "action": "SELL",
                "result": response
            })

        return jsonify({
            "action": "UNKNOWN"
        }), 400

    except Exception as e:

        logging.exception(e)

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    logging.info("Starting Bybit AI Bot...")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
