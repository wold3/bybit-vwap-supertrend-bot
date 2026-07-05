from flask import Flask, request

from world_agent import WorldAgent
from bybit_api import execute
from strategy_wrapper import execute_strategy

app = Flask(__name__)

agent = WorldAgent()


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    symbol = data["symbol"]
    price = data["price"]
    qty = data["qty"]

    state = [price] * 5

    action = agent.act(state)

    signal = ["HOLD", "BUY", "SELL"][action]

    decision = execute_strategy(signal, price)

    if not decision["success"]:
        return {"status": "filtered"}

    order = execute(signal, symbol, qty)

    return {
        "status": "success",
        "signal": signal,
        "order": order
    }


if __name__ == "__main__":
    app.run()
