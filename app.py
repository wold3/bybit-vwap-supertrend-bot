"""
app.py

TradingView Webhook Server
"""

import logging
import os
from flask import Flask, request, jsonify

from config import HOST, PORT, DEBUG
from signal_parser import validate
from bybit_api import (
    execute_signal,
    get_position,
    get_position_side,
    ping
)

# ----------------------------------
# Flask
# ----------------------------------

app = Flask(__name__)

# ----------------------------------
# Logging
# ----------------------------------

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("webhook")

if not logger.handlers:

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        "logs/webhook.log",
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def log(msg):

    print(msg)

    logger.info(msg)


# ----------------------------------
# Health Check
# ----------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify(
        {
            "project": "Bybit VWAP SuperTrend Bot",
            "status": "running"
        }
    )


@app.route("/health", methods=["GET"])
def health():

    api = ping()

    return jsonify(
        {
            "server": "ok",
            "bybit": api
        }
    )


# ----------------------------------
# Position
# ----------------------------------

@app.route("/position", methods=["GET"])
def position():

    side = get_position_side()

    pos = get_position()

    return jsonify(
        {
            "side": side,
            "position": pos
        }
    )


# ----------------------------------
# TradingView Webhook
# ----------------------------------

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(
        force=True,
        silent=True
    )

    log("--------------------------------------")
    log(f"REQUEST : {data}")

    ok, result = validate(data)

    if not ok:

        log(result)

        return jsonify(
            {
                "success": False,
                "error": result
            }
        ), 400

    signal = result["signal"]
    symbol = result["symbol"]
    qty = result["qty"]

    order = execute_signal(
        signal=signal,
        symbol=symbol,
        qty=qty
    )

    return jsonify(
        {
            "success": True,
            "signal": signal,
            "symbol": symbol,
            "qty": qty,
            "result": order
        }
    )


# ----------------------------------
# Error
# ----------------------------------

@app.errorhandler(Exception)
def handle_error(error):

    log(error)

    return jsonify(
        {
            "success": False,
            "error": str(error)
        }
    ), 500


# ----------------------------------
# Main
# ----------------------------------

if __name__ == "__main__":

    print("------------------------------------")
    print("Bybit VWAP SuperTrend Bot")
    print("------------------------------------")

    print(f"HOST : {HOST}")
    print(f"PORT : {PORT}")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
