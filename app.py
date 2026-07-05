from flask import Flask, request

from system import EconomySystem
from environment import Environment

app = Flask(__name__)

system = EconomySystem()
env = Environment()


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    price_input = data["price"]

    # ==========================
    # MACRO + AGENTS
    # ==========================

    actions, liquidity = system.step(price_input)

    # ==========================
    # MARKET SIMULATION
    # ==========================

    price, rewards = env.step(actions, liquidity)

    # ==========================
    # UPDATE AGENTS
    # ==========================

    for i, agent in enumerate(system.agents):
        agent.update(rewards[i])

    return {
        "price": price,
        "liquidity": liquidity,
        "actions": actions,
        "rewards": rewards
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
