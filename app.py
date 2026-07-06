import logging
from flask import Flask, request, jsonify

from strategy.strategy_wrapper import execute_signal
from services.logger_service import setup_logger

# =====================================================
# Logger
# =====================================================
setup_logger()
logger = logging.getLogger(__name__)

# =====================================================
# App
# =====================================================
app = Flask(__name__)


# =====================================================
# Health Check
# =====================================================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })


# =====================================================
# TradingView Webhook
# =====================================================
@app.route("/webhook", methods=["POST"])
def webhook():

    try:
        data = request.json

        logger.info("WEBHOOK RECEIVED: %s", data)

        signal = data.get("signal")
        symbol = data.get("symbol")
        qty = data.get("qty")
        price = data.get("price")

        result = execute_signal(
            data=data,
            symbol=symbol,
            qty=qty,
            price=price,
        )

        return jsonify(result)

    except Exception as e:
        logger.exception(e)

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


# =====================================================
# Bot Status
# =====================================================
@app.route("/status", methods=["GET"])
def status():

    return jsonify({
        "service": "bybit-trading-bot",
        "status": "running",
    })


# =====================================================
# Main
# =====================================================
if __name__ == "__main__":

    logger.info("Starting Trading Bot Server...")

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
    )
