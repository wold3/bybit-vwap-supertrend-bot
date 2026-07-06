from flask import Flask, jsonify
import time

from database.repository import trade_db
from execution.pnl_engine import pnl_engine


app = Flask(__name__)


# ================================
# HOME
# ================================
@app.route("/")
def home():

    return """
    <h1>🚀 AUTO TRADING DASHBOARD (DB MODE)</h1>
    <p>Status: RUNNING</p>
    <ul>
        <li>/status</li>
        <li>/pnl</li>
        <li>/trades</li>
    </ul>
    """


# ================================
# STATUS
# ================================
@app.route("/status")
def status():

    return jsonify({
        "status": "RUNNING",
        "time": time.time()
    })


# ================================
# PnL
# ================================
@app.route("/pnl")
def pnl():

    try:

        return jsonify({
            "symbol": "BTCUSDT",
            "pnl": pnl_engine.get("BTCUSDT"),
            "status": "LIVE"
        })

    except Exception as e:

        return jsonify({"error": str(e)})


# ================================
# TRADE LIST (DB 핵심)
# ================================
@app.route("/trades")
def trades():

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


# ================================
# SERVER RUN
# ================================
if __name__ == "__main__":

    print("🚀 Dashboard running on http://localhost:5000")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
