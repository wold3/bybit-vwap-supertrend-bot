import logging

from flask import Flask, request, jsonify

from config import HOST, PORT, DEBUG
from signal_parser import validate
from rl_predictor_dqn import decide
from bybit_api import execute
from state import can_trade, get_status

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
        "trade_status": get_status()
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

        signal = result["signal"]
        symbol = result["symbol"]
        qty = result["qty"]
        price = result["price"]

        # AI 판단
        ai_action = decide(price)

        action_map = {
            0: "HOLD",
            1: "BUY",
            2: "SELL"
        }

        ai_signal = action_map.get(ai_action, "HOLD")

        logging.info(
            "Webhook=%s | AI=%s | %s %.6f",
            signal,
            ai_signal,
            symbol,
            qty
        )

        # HOLD이면 주문하지 않음
        if ai_signal == "HOLD":
            return jsonify({
                "status": "ok",
                "action": "HOLD",
                "reason": "AI decision"
            })

        # TradingView와 AI가 같은 방향일 때만 주문
        if signal != ai_signal:
            return jsonify({
                "status": "filtered",
                "tv_signal": signal,
                "ai_signal": ai_signal
            })

        order = execute(
            ai_signal,
            symbol,
            qty
        )

        if not order.get("success", False):

            logging.error(order)

            return jsonify(order), 500

        send(f"{ai_signal} {symbol} qty={qty}")

        return jsonify({
            "status": "success",
            "signal": ai_signal,
            "symbol": symbol,
            "qty": qty,
            "price": price,
            "order": order
        })

    except Exception as e:

        logging.exception(e)

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    logging.info("Starting Bybit AI Trading Bot...")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
