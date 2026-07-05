from flask import Flask, jsonify

from world import World
from persistence import save, load

app = Flask(__name__)

world = World()
world = load(world)


@app.route("/step")
def step():

    price = world.step()
    save(world)

    return jsonify({
        "price": price,
        "population": len(world.agents)
    })


@app.route("/metrics")
def metrics():

    return jsonify({
        "volatility": world.metrics.volatility(),
        "trend": world.metrics.trend()
    })


@app.route("/status")
def status():

    return jsonify({
        "price": world.market.price,
        "population": len(world.agents)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
