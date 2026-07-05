from flask import Flask, request, jsonify

from signal_parser import validate
from bybit_api import execute
from state import (
    can_trade,
    position,
    update_position,
    update_pnl,
    add_trade
)
from telegram import send_message
from config import MAX_DAILY_LOSS

app = Flask(__name__)


# =========================
# WEBHOOK
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True, silent=True)

    ok, result = validate(data)

    if not ok:
        send_message(f"❌ INVALID SIGNAL: {result}")
        return jsonify({"error": result}), 400

    if position["daily_pnl"] <= MAX_DAILY_LOSS:
        send_message("⚠️ DAILY LOSS LIMIT HIT")
        return jsonify({"error": "loss limit"}), 403

    if not can_trade():
        send_message("⚠️ TRADE LIMIT REACHED")
        return jsonify({"error": "limit"}), 429

    signal = result["signal"]

    res = execute(
        signal,
        result["symbol"],
        result["qty"]
    )

    add_trade()

    send_message(
        f"📊 TRADE\n"
        f"{signal}\n"
        f"{result['symbol']}\n"
        f"qty: {result['qty']}"
    )

    print(f"[EXECUTE] {signal}")

    return jsonify({
        "success": True,
        "result": res
    })


# =========================
# PnL DASHBOARD
# =========================
@app.route("/pnl")
def pnl():

    return jsonify({
        "daily_pnl": position["daily_pnl"],
        "trades": position["trades"],
        "highest_profit": position["highest_profit"],
        "entry_price": position["entry_price"]
    })


# =========================
# HEALTH CHECK
# =========================
@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
