from flask import Flask, request, jsonify

from signal_parser import validate
from bybit_api import execute
from state import can_trade, position, update_position, update_pnl
from telegram import send_message
from config import MAX_DAILY_LOSS

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True, silent=True)

    ok, result = validate(data)

    if not ok:
        send_message(f"❌ INVALID SIGNAL: {result}")
        return jsonify({"error": result}), 400

    # 🔥 손실 제한
    if position["daily_pnl"] <= MAX_DAILY_LOSS:
        send_message("⚠️ DAILY LOSS LIMIT HIT - STOP TRADING")
        return jsonify({"error": "daily loss limit"}), 403

    # 🔥 거래 제한
    if not can_trade():
        send_message("⚠️ TRADE LIMIT REACHED")
        return jsonify({"error": "trade limit"}), 429

    signal = result["signal"]

    res = execute(
        signal,
        result["symbol"],
        result["qty"]
    )

    # 🔔 텔레그램 알림
    send_message(
        f"📊 TRADE EXECUTED\n"
        f"Signal: {signal}\n"
        f"Symbol: {result['symbol']}\n"
        f"Qty: {result['qty']}"
    )

    print(f"[EXECUTE] {signal} {result['symbol']}")

    return jsonify({
        "success": True,
        "result": res
    })


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
