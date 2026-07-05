from flask import Flask, request

from environment import Environment
from agent_system import AgentSystem
from strategy import filter_signal

app = Flask(__name__)

env = Environment()
system = AgentSystem()


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    price = data["price"]

    # ==========================
    # AGENT ACTIONS
    # ==========================

    actions = system.act_all(price)

    # ==========================
    # MARKET STEP
    # ==========================

    price, rewards = env.step(actions)

    system.update_all(rewards)

    # ==========================
    # SIGNAL OUTPUT (EMERGENT)
    # ==========================

    buy = actions.count(1)
    sell = actions.count(2)

    if buy > sell:
        signal = "BUY"
    elif sell > buy:
        signal = "SELL"
    else:
        signal = "HOLD"

    if not filter_signal(signal):
        return {"status": "filtered"}

    return {
        "price": price,
        "signal": signal,
        "actions": actions,
        "rewards": rewards
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
