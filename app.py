from flask import Flask, request, jsonify

from signal_parser import validate
from bybit_api import execute
from state import (
    positions,
    get_position,
    can_trade,
    update_price,
    update_trailing,
    should_exit
)

from telegram import send_message
from config import USE_AI_FILTER, MAX_DAILY_LOSS
from ai_filter import allow_trade

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True, silent=True)

    ok, result = validate(data)

    if not ok:
        send_message(f"❌ INVALID {result}")
        return jsonify({"error": result}), 400

    symbol = result["symbol"]
    price = float(data.get("price", 0))
    qty = result["qty"]

    pos = get_position(symbol)

    # AI 필터
    if USE_AI_FILTER:
        ok_filter, reason = allow_trade()
        if not ok_filter:
            return jsonify({"blocked": reason}), 403

    # 트레일링 업데이트
    update_price(symbol, price)
    update_trailing(symbol)

    # EXIT
    if should_exit(symbol, price):
        execute("SELL", symbol, qty)
        send_message(f"🚨 EXIT {symbol} @ {price}")
        pos["active"] = False
        return jsonify({"exit": True})

    # 손실 제한
    if pos["daily_pnl"] <= MAX_DAILY_LOSS:
        return jsonify({"error": "loss limit"}), 403

    # 거래 제한
    if not can_trade():
        return jsonify({"error": "limit"}), 429

    # 진입
    if result["signal"] == "BUY":

        pos["active"] = True
        pos["entry_price"] = price
        pos["highest_price"] = price
        pos["trailing_stop"] = price * 0.995

        execute("BUY", symbol, qty)

        send_message(f"📈 ENTRY {symbol} @ {price}")

    return jsonify({"ok": True})


@app.route("/pnl")
def pnl():
    return jsonify(positions)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
