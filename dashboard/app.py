from flask import Flask, jsonify
import time

from trade_db import trade_db   # 🔥 핵심 수정 (이게 맞음)


app = Flask(__name__)


@app.route("/")
def home():
    return "🚀 DASHBOARD RUNNING"


@app.route("/status")
def status():
    return jsonify({
        "status": "RUNNING",
        "time": time.time()
    })


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


@app.route("/pnl-history")
def pnl_history():

    # 기존 프로젝트에 없을 수도 있음 → 안전 fallback
    try:
        rows = trade_db.get_pnl_history()
    except:
        rows = []

    return jsonify([
        {
            "pnl": r[0],
            "time": r[1]
        }
        for r in rows
    ])


if __name__ == "__main__":

    print("🚀 Dashboard running on http://localhost:5000")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
