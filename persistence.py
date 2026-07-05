import json
import os

FILE = "state.json"


def save(world):

    data = {
        "price": world.market.price,
        "agents": [
            {
                "capital": a.capital,
                "strategy": a.strategy
            }
            for a in world.agents
        ]
    }

    with open(FILE, "w") as f:
        json.dump(data, f)


def load(world):

    if not os.path.exists(FILE):
        return world

    with open(FILE, "r") as f:
        data = json.load(f)

    world.market.price = data["price"]

    for i, a in enumerate(world.agents):
        if i < len(data["agents"]):
            a.capital = data["agents"][i]["capital"]
            a.strategy = data["agents"][i]["strategy"]

    return world
