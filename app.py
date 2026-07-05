import logging

from flask import Flask, jsonify, request

from config import DEBUG, HOST, PORT
from signal_parser import validate
from state import can_trade, get_status
from bybit_api import execute
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


# =====================================================
# BASIC ROUTES
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


# =====================================================
# PnL API
# =====================================================

@app.route("/pnl")
def pnl():
    return jsonify(get_status())


# =====================================================
# DASHBOARD (HTML UI)
# =====================================================

@app.route("/dashboard")
def dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trading Bot Dashboard</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {
                font-family: Arial;
                background: #0f172a;
                color: #e2e8f0;
                text-align: center;
                padding-top: 50px;
            }
            .box {
                display: inline-block;
                padding: 20px;
                border-radius: 10px;
                background: #1e293b;
                margin: 10px;
                min-width: 200px;
            }
        </style>
    </head>
    <body>

        <h1>📊 Trading Bot Dashboard</h1>

        <div class="box">
            <h2>Status</h2>
            <p>RUNNING</p>
        </div>

        <div class="box">
            <h2>API</h2>
            <p>/pnl</p>
        </div>

        <div class="box">
            <h2>Refresh</h2>
            <p>5 sec auto</p>
        </div>

    </body>
    </html>
    """


# =====================================================
# WEBHOOK (MAIN TRADING ENGINE)
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

        order = execute(
            final_signal,
            symbol,
            qty,
        )

        if not order.get("success", False):

            send_error(order.get("error", "Unknown error"))

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
