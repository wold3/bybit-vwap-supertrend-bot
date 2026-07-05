import logging

from flask import Flask, jsonify, request

from config import DEBUG, HOST, PORT
from signal_parser import validate
from state import can_trade, get_status, sync_real_pnl
from bybit_api import execute
from telegram import send_error, send_status, send_trade
from strategy_wrapper import execute_strategy

from websocket_stream import start_ws


# =====================================================
# LOGGING
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


# =====================================================
# APP
# =====================================================

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "name": "Bybit AI Trading Bot",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify(get_status())


@app.route("/pnl")
def pnl():

    sync_real_pnl("BTCUSDT")

    return jsonify(get_status())


@app.route("/dashboard")
def dashboard():
    return """
    <h1>Trading Bot Running</h1>
    <p>/pnl active</p>
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
            return jsonify({"error": "Rate limit"}), 429

        signal = result["signal"]
        symbol = result["symbol"]
        qty = result["qty"]
        price = result["price"]

        decision = execute_strategy(signal, price)

        if not decision["success"]:
            return jsonify({
                "status": "filtered",
                "reason": decision["reason"]
            })

        order = execute(signal, symbol, qty)

        if not order.get("success"):
            send_error(order.get("error"))
            return jsonify(order), 500

        send_trade(signal, symbol, qty, price)

        # 🔥 WebSocket이 자동으로 pnl sync 하지만 fallback
        sync_real_pnl(symbol)

        return jsonify({
            "status": "success",
            "order": order
        })

    except Exception as e:

        logger.exception(e)
        send_error(str(e))

        return jsonify({"error": str(e)}), 500


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    logger.info("Starting Trading Bot...")

    send_status("🚀 Trading Bot Started")

    # 🔥 WebSocket start
    start_ws("BTCUSDT")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG,
    )
