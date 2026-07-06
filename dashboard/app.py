from flask import Flask, jsonify
import time

# 🔥 핵심: 프로젝트 실제 구조
from trade_db import trade_db


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

    # 안전 처리 (없어도 서버 안 죽게)
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
