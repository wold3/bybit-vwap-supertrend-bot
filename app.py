from flask import Flask, request, jsonify

from signal_parser import validate
from bybit_api import execute
from state import (
    can_trade,
    position,
    update_position,
    update_pnl
)
from config import TRAILING_STEP, MAX_DAILY_LOSS

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True, silent=True)

    ok, result = validate(data)

    if not ok:
        return jsonify({"error": result}), 400

    # 🔥 손실 제한 체크
    if position["daily_pnl"] <= MAX_DAILY_LOSS:
        return jsonify({"error": "daily loss limit reached"}), 403

    if not can_trade():
        return jsonify({"error": "trade limit reached"}), 429

    signal = result["signal"]

    # 🔥 트레일링 로직 (단순 구조)
    if signal == "BUY":

        entry_price = data.get("price", 0)
        profit = data.get("profit", 0)

        update_position(entry_price, profit)

    elif signal == "SELL":

        if position["highest_profit"] >= TRAILING_STEP:
            print("[TRAILING EXIT] profit protected")

    res = execute(
        signal,
        result["symbol"],
        result["qty"]
    )

    print(f"[EXECUTE] {signal} | {result['symbol']} | {result['qty']}")

    return jsonify({
        "success": True,
        "result": res
    })


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
