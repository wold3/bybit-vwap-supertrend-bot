import logging
import time
import threading

from flask import Flask, request, jsonify

from strategy.strategy_wrapper import execute_strategy
from execution.execution_engine import engine
from risk.risk_engine import risk_engine
from services.logger_service import logger_service
from services.report_service import send_daily_report

app = Flask(__name__)

logger = logger_service


# =====================================================
# Health Check
# =====================================================
@app.route("/health", methods=["GET"])
def health():

    return jsonify(
        {
            "status": "ok",
            "engine": engine.health(),
            "risk": risk_engine.health(),
        }
    )


# =====================================================
# Webhook (TradingView)
# =====================================================
@app.route("/webhook", methods=["POST"])
def webhook():

    try:

        data = request.get_json()

        signal = data.get("signal")
        symbol = data.get("symbol")
        price = data.get("price")
        qty = data.get("qty")

        logger.info(
            "Webhook received %s %s",
            signal,
            symbol,
        )

        result = execute_strategy(
            signal=signal,
            price=price,
            symbol=symbol,
            qty=qty,
        )

        return jsonify(result)

    except Exception as e:

        logger.exception("Webhook error")

        return jsonify(
            {
                "success": False,
                "error": str(e),
            }
        ), 500


# =====================================================
# Engine Monitor
# =====================================================
def monitor_engine():

    while True:

        try:

            status = engine.status()

            logger.info(
                "Engine status: %s",
                status,
            )

        except Exception as e:

            logger.exception(e)

        time.sleep(60)


# =====================================================
# Daily Report Scheduler
# =====================================================
def report_scheduler():

    last_date = None

    while True:

        try:

            current_date = time.strftime("%Y-%m-%d")

            if current_date != last_date:

                send_daily_report()

                last_date = current_date

        except Exception as e:

            logger.exception(e)

        time.sleep(300)


# =====================================================
# Startup Threads
# =====================================================
def start_background_tasks():

    t1 = threading.Thread(
        target=monitor_engine,
        daemon=True,
    )

    t2 = threading.Thread(
        target=report_scheduler,
        daemon=True,
    )

    t1.start()
    t2.start()


# =====================================================
# Main
# =====================================================
if __name__ == "__main__":

    logger.info("Starting Trading Bot")

    start_background_tasks()

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
    )
