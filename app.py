import atexit
import logging

from flask import Flask, jsonify, render_template

from config import DEBUG, HOST, PORT, validate
from database.session import init_db
from persistence import load, save
from world import World

# =====================================================
# Config Validation
# =====================================================

validate()

# =====================================================
# Database
# =====================================================

init_db()

# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

# =====================================================
# Flask
# =====================================================

app = Flask(__name__)

# =====================================================
# World
# =====================================================

world = load(World())

# =====================================================
# Auto Save
# =====================================================


def shutdown():

    logger.info("Saving world state...")

    save(world)


atexit.register(shutdown)

# =====================================================
# Dashboard
# =====================================================


@app.route("/")
def dashboard():

    return render_template("dashboard.html")


# =====================================================
# Step Simulation
# =====================================================


@app.route("/step")
def step():

    try:

        price = world.step()

        save(world)

        return jsonify(
            {
                "success": True,
                "price": round(price, 4),
                "population": len(world.agents),
            }
        )

    except Exception as e:

        logger.exception(e)

        return (
            jsonify(
                {
                    "success": False,
                    "error": str(e),
                }
            ),
            500,
        )


# =====================================================
# Status
# =====================================================


@app.route("/status")
def status():

    return jsonify(
        {
            "success": True,
            "price": round(world.market.price, 4),
            "population": len(world.agents),
            "volatility": round(
                world.metrics.volatility(),
                6,
            ),
            "trend": round(
                world.metrics.trend(),
                4,
            ),
        }
    )


# =====================================================
# Metrics
# =====================================================


@app.route("/metrics")
def metrics():

    return jsonify(
        {
            "success": True,
            "volatility": round(
                world.metrics.volatility(),
                6,
            ),
            "trend": round(
                world.metrics.trend(),
                4,
            ),
        }
    )


# =====================================================
# Save
# =====================================================


@app.route("/save")
def save_state():

    save(world)

    return jsonify(
        {
            "success": True,
            "message": "State saved.",
        }
    )


# =====================================================
# Reset
# =====================================================


@app.route("/reset")
def reset():

    global world

    world = World()

    save(world)

    return jsonify(
        {
            "success": True,
            "message": "World reset.",
        }
    )


# =====================================================
# Health Check
# =====================================================


@app.route("/health")
def health():

    return jsonify(
        {
            "status": "ok",
            "database": True,
            "population": len(world.agents),
            "mode": "simulation",
        }
    )


# =====================================================
# Version
# =====================================================


@app.route("/version")
def version():

    return jsonify(
        {
            "name": "Bybit VWAP SuperTrend Bot",
            "version": "3.0",
            "mode": "simulation",
        }
    )


# =====================================================
# Main
# =====================================================

if __name__ == "__main__":

    logger.info("Artificial Economy Server Started")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG,
    )
