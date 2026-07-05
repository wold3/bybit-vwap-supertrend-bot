from flask import Flask, request, jsonify

from signal_parser import validate
from bybit_api import execute

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True, silent=True)

    ok, result = validate(data)

    if not ok:
        return jsonify({"error": result}), 400

    res = execute(
        result["signal"],
        result["symbol"],
        result["qty"]
    )

    return jsonify({
        "success": True,
        "result": str(res)
    })


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
