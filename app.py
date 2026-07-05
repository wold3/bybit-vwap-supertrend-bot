from flask import Flask, request, jsonify

from signal_parser import validate
from rl_predictor import decide
from bybit_api import execute
from risk_engine import should_stop, update_pnl
from state import can_trade

from telegram import send

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    if should_stop():
        return jsonify({"blocked": "risk"}), 403

    data = request.get_json(force=True)

    ok, result = validate(data)

    if not ok:
        return jsonify({"error": result}), 400

    symbol = result["symbol"]
    price = float(data.get("price", 0))
    qty = result["qty"]

    action = decide(price)

    # RL 결정
    if action == 0:
        return jsonify({"rl": "HOLD"})

    if not can_trade():
        return jsonify({"error": "rate_limit"}), 429

    if action == 1:
        execute("BUY", symbol, qty)
        send(f"BUY {symbol} {price}")
        return jsonify({"rl": "BUY"})

    if action == 2:
        execute("SELL", symbol, qty)
        update_pnl(-1)
        send(f"SELL {symbol} {price}")
        return jsonify({"rl": "SELL"})


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
