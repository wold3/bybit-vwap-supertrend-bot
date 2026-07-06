from flask import Flask, jsonify
from storage.trade_db import trade_db
from execution.pnl_tracker import pnl_tracker

app = Flask(__name__)


# ================================
# 전체 거래 조회
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
# 전체 PnL
# ================================
@app.route("/pnl")
def pnl():

    return jsonify({
        "total_pnl": pnl_tracker.total_pnl()
    })


# ================================
# 시스템 상태
# ================================
@app.route("/status")
def status():

    return jsonify({
        "status": "RUNNING",
        "service": "AUTO_TRADING_BOT"
    })


# ================================
# 서버 실행
# ================================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
