from flask import Flask, jsonify, render_template
import time

from trade_db import trade_db

app = Flask(__name__)

# =================================================
# LIVE DATA STORAGE (WS에서 업데이트)
# =================================================
latest_price = {"price": 0, "time": 0}
equity_curve = []


# =================================================
# HOME
# =================================================
@app.route("/")
def home():
    return render_template("dashboard.html")


# =================================================
# PRICE API (REALTIME CHART)
# =================================================
@app.route("/api/price")
def price():
    return jsonify(latest_price)


# =================================================
# EQUITY API (PnL CHART)
# =================================================
@app.route("/api/equity")
def equity():
    return jsonify(equity_curve)


# =================================================
# TRADES
# =================================================
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


# =================================================
# UPDATE HOOK (WS에서 호출)
# =================================================
def update_price(price):

    latest_price["price"] = price
    latest_price["time"] = time.time()


def update_equity(pnl):

    equity_curve.append({
        "time": int(time.time()),
        "value": pnl
    })

    if len(equity_curve) > 500:
        equity_curve.pop(0)


if __name__ == "__main__":

    print("🚀 DASHBOARD RUNNING")

    app.run(host="0.0.0.0", port=5000, debug=False)
