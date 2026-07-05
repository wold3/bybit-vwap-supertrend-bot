from flask import Flask, request, jsonify

from signal_parser import validate
from bybit_api import execute
from state import can_trade

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True, silent=True)

    ok, result = validate(data)

    if not ok:
        return jsonify({"error": result}), 400

    if not can_trade():
        return jsonify({"error": "trade limit reached"}), 429

    res = execute(
        result["signal"],
        result["symbol"],
        result["qty"]
    )

    print(f"[EXECUTE] {result['signal']} | {result['symbol']} | {result['qty']}")

    return jsonify({
        "success": True,
        "result": res
    })


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
