from flask import Flask, request, jsonify

from signal_parser import validate
from bybit_api import execute
from state import (
    position,
    can_trade,
    add_trade,
    update_price,
    update_trailing,
    should_exit
)

from telegram import send_message
from config import MAX_DAILY_LOSS, USE_AI_FILTER
from ai_filter import allow_trade

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True, silent=True)

    ok, result = validate(data)

    if not ok:
        send_message(f"❌ INVALID: {result}")
        return jsonify({"error": result}), 400

    price = float(data.get("price", 0))
    symbol = result["symbol"]
    qty = result["qty"]

    # 🔥 AI 필터
    if USE_AI_FILTER:
        ok_filter, reason = allow_trade()
        if not ok_filter:
            send_message(f"🚫 FILTER BLOCK: {reason}")
            return jsonify({"error": reason}), 403

    # 🔥 손실 제한
    if position["daily_pnl"] <= MAX_DAILY_LOSS:
        send_message("⚠️ DAILY LOSS LIMIT")
        return jsonify({"error": "loss limit"}), 403

    # 🔥 거래 제한
    if not can_trade():
        send_message("⚠️ TRADE LIMIT")
        return jsonify({"error": "limit"}), 429

    # =========================
    # 트레일링 로직
    # =========================
    update_price(price)
    update_trailing()

    if should_exit(price):
        execute("SELL", symbol, qty)

        send_message(f"🚨 TRAILING EXIT\nPrice: {price}")

        position["active"] = False

        return jsonify({"status": "trailing exit"})

    # =========================
    # 진입
    # =========================
    if result["signal"] == "BUY":

        position["active"] = True
        position["entry_price"] = price
        position["highest_price"] = price
        position["trailing_stop"] = price * 0.995

        execute("BUY", symbol, qty)

        add_trade()

        send_message(f"📈 ENTRY {symbol} @ {price}")

    return jsonify({"success": True})


@app.route("/pnl")
def pnl():
    return jsonify(position)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
