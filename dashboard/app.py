from flask import Flask, jsonify
import time

from storage.trade_db import trade_db
from execution.pnl_engine import pnl_engine


# =========================================================
# FLASK APP
# =========================================================
app = Flask(__name__)


# =========================================================
# HOME (브라우저 기본 페이지)
# =========================================================
@app.route("/")
def home():

    return """
    <h1>🚀 AUTO TRADING BOT DASHBOARD</h1>
    <p>Status: RUNNING</p>
    <p>Endpoints:</p>
    <ul>
        <li>/status</li>
        <li>/pnl</li>
        <li>/trades</li>
    </ul>
    """


# =========================================================
# SYSTEM STATUS
# =========================================================
@app.route("/status")
def status():

    return jsonify({
        "status": "RUNNING",
        "timestamp": time.time()
    })


# =========================================================
# TOTAL PNL
# =========================================================
@app.route("/pnl")
def pnl():

    try:
        total = pnl_engine.get("BTCUSDT")

        return jsonify({
            "symbol": "BTCUSDT",
            "pnl": total,
            "status": "LIVE"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# =========================================================
# TRADE LIST
# =========================================================
@app.route("/trades")
def trades():

    try:

        rows = trade_db.all()

        return jsonify([
            {
                "id": r[0],
                "symbol": r[1],
                "side": r[2],
                "qty": r[3],
                "price": r[4],
                "pnl": r[5],
                "time": r[6]
            }
            for r in rows
        ])

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# =========================================================
# SERVER START
# =========================================================
if __name__ == "__main__":

    print("🚀 Dashboard starting on http://localhost:5000")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
