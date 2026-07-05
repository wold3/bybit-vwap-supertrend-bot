import logging
from flask import Flask, jsonify, request

from config import DEBUG, HOST, PORT
from signal_parser import validate
from state import compute_real_pnl, update_trade_result, get_status
from bybit_api import execute
from feature_engine import get_feature_vector
from dqn_agent import Agent
from telegram import send_trade, send_error
from strategy_wrapper import execute_strategy


app = Flask(__name__)
logger = logging.getLogger(__name__)

agent = Agent()


@app.route("/webhook", methods=["POST"])
def webhook():

    try:

        data = request.get_json(silent=True)

        if not data:
            return {"error": "Invalid JSON"}, 400

        ok, result = validate(data)

        if not ok:
            return {"error": result}, 400

        symbol = result["symbol"]
        price = result["price"]
        qty = result["qty"]
        orderbook = result.get("orderbook", None)

        # ==========================
        # FEATURE
        # ==========================

        state_vec = get_feature_vector(price, orderbook)

        action = agent.act(state_vec)

        signal = ["HOLD", "BUY", "SELL"][action]

        # ==========================
        # FILTER
        # ==========================

        decision = execute_strategy(signal, price)

        if not decision["success"]:
            return {"status": "filtered"}

        # ==========================
        # EXECUTE
        # ==========================

        order = execute(signal, symbol, qty)

        if not order.get("success"):
            send_error(order.get("error"))
            return order, 500

        send_trade(signal, symbol, qty, price)

        # ==========================
        # REAL PnL REWARD
        # ==========================

        reward = compute_real_pnl(price, price, qty, state_vec[2])

        next_state = get_feature_vector(price, orderbook)

        agent.buffer.push(state_vec, action, reward, next_state)

        agent.train()
        agent.soft_update()

        update_trade_result(reward)

        return {
            "status": "success",
            "signal": signal,
            "reward": reward
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
