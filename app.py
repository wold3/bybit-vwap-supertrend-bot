import logging
from flask import Flask, request

from config import HOST, PORT, DEBUG
from bybit_api import execute
from strategy_wrapper import execute_strategy
from telegram import send_trade, send_error

from sequence_builder import build_sequence
from world_agent import WorldAgent
from imagination_trainer import ImaginationTrainer
from feature_engine import get_feature_vector


app = Flask(__name__)
logger = logging.getLogger(__name__)

agent = WorldAgent()
trainer = ImaginationTrainer()


@app.route("/webhook", methods=["POST"])
def webhook():

    try:

        data = request.get_json()

        symbol = data["symbol"]
        price = data["price"]
        qty = data["qty"]
        orderbook = data.get("orderbook")

        # ==========================
        # STATE SEQUENCE
        # ==========================

        state_seq = build_sequence(price, orderbook)

        # ==========================
        # WORLD MODEL ACTION
        # ==========================

        action = agent.act(state_seq)

        signal = ["HOLD", "BUY", "SELL"][action]

        decision = execute_strategy(signal, price)

        if not decision["success"]:
            return {"status": "filtered"}

        # ==========================
        # EXECUTION
        # ==========================

        order = execute(signal, symbol, qty)

        if not order.get("success"):
            send_error(order.get("error"))
            return order, 500

        send_trade(signal, symbol, qty, price)

        # ==========================
        # IMAGINATION TRAINING
        # ==========================

        trainer.push(state_seq)
        trainer.train_step()

        return {
            "status": "success",
            "signal": signal
        }

    except Exception as e:
        logger.exception(e)
        send_error(str(e))
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
