from flask import Flask, request, jsonify

from signal_parser import validate
from bybit_api import execute
from state import can_trade, position, add_trade, update_pnl
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

    # 🔥 AI 필터
    if USE_AI_FILTER:
        allowed, reason = allow_trade()
        if not allowed:
            send_message(f"🚫 FILTER: {reason}")
            return jsonify({"error": reason}), 403

    # 🔥 손실 제한
    if position["daily_pnl"] <= MAX_DAILY_LOSS:
        send_message("⚠️ DAILY LOSS LIMIT HIT")
        return jsonify({"error": "loss limit"}), 403

    # 🔥 거래 제한
    if not can_trade():
        send_message("⚠️ TRADE LIMIT")
        return jsonify({"error": "limit"}), 429

    signal = result["signal"]

    res = execute(signal, result["symbol"], result["qty"])

    add_trade()

    send_message(
        f"📊 TRADE\n"
        f"{signal}\n"
        f"{result['symbol']}\n"
        f"qty: {result['qty']}"
    )

    print(f"[EXECUTE] {signal}")

    return jsonify({"success": True, "result": res})


# =========================
# PnL DASHBOARD
# =========================
@app.route("/pnl")
def pnl():
    return jsonify(position)


# =========================
# HEALTH CHECK
# =========================
@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
