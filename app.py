from flask import Flask, request, jsonify

from signal_parser import validate
from rl_predictor_dqn import decide
from bybit_api import execute
from state import can_trade

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True)

    ok, result = validate(data)

    if not ok:
        return {"error": result}, 400

    symbol = result["symbol"]
    qty = result["qty"]

    price = float(data.get("price", 0))

    action = decide(price)

    if not can_trade():
        return {"error": "rate_limit"}, 429

    if action == 0:
        return {"action": "HOLD"}

    if action == 1:
        execute("BUY", symbol, qty)
        return {"action": "BUY"}

    if action == 2:
        execute("SELL", symbol, qty)
        return {"action": "SELL"}

    return {"ok": True}


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
