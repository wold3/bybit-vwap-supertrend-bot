from flask import Flask, jsonify, render_template

from database.repository import (
    get_summary,
    get_recent_trades,
    get_positions,
    get_bot_state,
)

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
# SUMMARY API
# =====================================================
@app.route("/api/summary")
def summary():

    return jsonify(get_summary())


# =====================================================
# TRADES API
# =====================================================
@app.route("/api/trades")
def trades():

    return jsonify([
        {
            "symbol": t.symbol,
            "side": t.side,
            "qty": t.qty,
            "price": t.price,
            "pnl": t.pnl,
            "status": t.status,
        }
        for t in get_recent_trades(50)
    ])


# =====================================================
# POSITIONS API
# =====================================================
@app.route("/api/positions")
def positions():

    return jsonify([
        {
            "symbol": p.symbol,
            "side": p.side,
            "qty": p.qty,
            "entry_price": p.entry_price,
            "unrealized_pnl": p.unrealized_pnl,
        }
        for p in get_positions()
    ])


# =====================================================
# RISK API
# =====================================================
@app.route("/api/risk")
def risk():

    return jsonify(get_risk_status())


# =====================================================
# PERFORMANCE API
# =====================================================
@app.route("/api/performance")
def performance():

    return jsonify(performance_analyzer.total_performance())


# =====================================================
# BOT STATUS
# =====================================================
@app.route("/api/bot")
def bot():

    return jsonify(get_bot_state())


# =====================================================
# RUN
# =====================================================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
