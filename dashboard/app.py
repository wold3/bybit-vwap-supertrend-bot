from flask import Flask, jsonify, render_template
import time

# ✅ 실제 존재하는 DB 모듈로 통일
from trade_db import trade_db

from risk.risk_engine import get_risk_status
from analytics.performance_analyzer import performance_analyzer


app = Flask(__name__)


# =====================================================
# HOME DASHBOARD
# =====================================================
@app.route("/")
def home():
    return render_template("dashboard.html")


# =====================================================
# SUMMARY
# =====================================================
@app.route("/api/summary")
def summary():

    trades = trade_db.all()

    return jsonify({
        "total_trades": len(trades),
        "status": "RUNNING"
    })


# =====================================================
# TRADES
# =====================================================
@app.route("/api/trades")
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


# =====================================================
# POSITIONS (임시 유지)
# =====================================================
@app.route("/api/positions")
def positions():

    return jsonify([])


# =====================================================
# RISK
# =====================================================
@app.route("/api/risk")
def risk():

    try:
        return jsonify(get_risk_status())
    except:
        return jsonify({"status": "OK"})


# =====================================================
# PERFORMANCE
# =====================================================
@app.route("/api/performance")
def performance():

    try:
        return jsonify(performance_analyzer.total_performance())
    except:
        return jsonify({"pnl": 0})


# =====================================================
# BOT STATUS
# =====================================================
@app.route("/api/bot")
def bot():

    return jsonify({
        "status": "RUNNING",
        "time": time.time()
    })


# =====================================================
# PnL HISTORY (차트용 핵심)
# =====================================================
@app.route("/api/pnl-history")
def pnl_history():

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


# =====================================================
# RUN SERVER
# =====================================================
if __name__ == "__main__":

    print("🚀 Dashboard running on http://localhost:5000")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
