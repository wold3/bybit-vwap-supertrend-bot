import logging
from flask import Flask, request, jsonify

from strategy.strategy_wrapper import execute_signal
from services.logger_service import setup_logger

from database.repository import get_summary
from risk.risk_engine import get_risk_status
from execution.position_manager import position_manager

setup_logger()
logger = logging.getLogger(__name__)

app = Flask(__name__)


# =====================================================
# Health Check
# =====================================================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# =====================================================
# TradingView Webhook
# =====================================================
@app.route("/webhook", methods=["POST"])
def webhook():

    try:
        data = request.json

        logger.info("WEBHOOK RECEIVED: %s", data)

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
# Dashboard Summary API (FIXED)
# =====================================================
@app.route("/api/summary", methods=["GET"])
def summary():

    try:

        summary_data = get_summary()
        risk_data = get_risk_status()
        position_data = position_manager.status()

        return jsonify({
            "summary": summary_data,
            "risk": risk_data,
            "position": position_data,
        })

    except Exception as e:
        logger.exception(e)

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


# =====================================================
# Risk API
# =====================================================
@app.route("/api/risk", methods=["GET"])
def risk():

    try:
        return jsonify(get_risk_status())
    except Exception as e:
        logger.exception(e)
        return jsonify({"error": str(e)}), 500


# =====================================================
# Position API
# =====================================================
@app.route("/api/position", methods=["GET"])
def position():

    try:
        return jsonify(position_manager.status())
    except Exception as e:
        logger.exception(e)
        return jsonify({"error": str(e)}), 500


# =====================================================
# Main
# =====================================================
if __name__ == "__main__":

    logger.info("Starting Bybit Trading Bot...")

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
    )
