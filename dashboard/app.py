from flask import Flask, jsonify, render_template

from database.trade_db import trade_db

app = Flask(__name__)


# =================================================
# DASHBOARD PAGE
# =================================================
@app.route("/")
def home():
    return render_template("dashboard.html")


# =================================================
# TRADES
# =================================================
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


# =================================================
# EQUITY CURVE
# =================================================
@app.route("/api/equity")
def equity():

    rows = trade_db.get_equity_history()

    return jsonify([
        {
            "equity": r[0],
            "time": r[1]
        }
        for r in rows
    ])


# RUN
if __name__ == "__main__":

    print("🚀 Dashboard running on http://localhost:5000")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
