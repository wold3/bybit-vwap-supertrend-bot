from flask import Flask, jsonify

from world import World

app = Flask(__name__)

world = World()


@app.route("/step", methods=["GET"])
def step():

    price = world.step()

    return jsonify({
        "price": price,
        "population": len(world.agents)
    })


@app.route("/status")
def status():

    return jsonify({
        "price": world.market.price,
        "agents": len(world.agents)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
