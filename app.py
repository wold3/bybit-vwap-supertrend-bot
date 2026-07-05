import logging

from flask import Flask, jsonify, request

from config import DEBUG, HOST, PORT
from signal_parser import validate
from state import can_trade, get_status, compute_reward, update_trade_result
from bybit_api import execute
from dqn_agent import Agent
from feature_engine import get_feature_vector
from telegram import send_trade, send_error
from strategy_wrapper import execute_strategy


app = Flask(__name__)
logger = logging.getLogger(__name__)

agent = Agent()


# ==========================
# WEBHOOK
# ==========================
@app.route("/webhook", methods=["POST"])
def webhook():

    try:

        data = request.get_json(silent=True)

        if not data:
            return {"error": "Invalid JSON"}, 400

        ok, result = validate(data)

        if not ok:
            return {"error": result}, 400

        if not can_trade():
            return {"error": "Rate limit"}, 429

        symbol = result["symbol"]
        price = result["price"]
        qty = result["qty"]
        orderbook = result.get("orderbook", None)

        # ==========================
        # FEATURE VECTOR (NEW)
        # ==========================

        state_vec = get_feature_vector(price, orderbook)

        action = agent.act(state_vec)

        ai_signal = ["HOLD", "BUY", "SELL"][action]

        # ==========================
        # STRATEGY FILTER
        # ==========================

        decision = execute_strategy(ai_signal, price)

        if not decision["success"]:
            return {"status": "filtered"}

        # ==========================
        # EXECUTION
        # ==========================

        order = execute(ai_signal, symbol, qty)

        if not order.get("success"):
            send_error(order.get("error"))
            return order, 500

        send_trade(ai_signal, symbol, qty, price)

        # ==========================
        # REWARD (simplified hook)
        # ==========================

        reward = 0.0  # 실거래 PnL 연결 가능

        next_state = get_feature_vector(price, orderbook)

        agent.buffer.push(
            state_vec,
            action,
            reward,
            next_state
        )

        agent.train()
        agent.soft_update()

        update_trade_result(reward)

        return {
            "status": "success",
            "action": ai_signal,
            "features": state_vec
        }

    except Exception as e:
        logger.exception(e)
        send_error(str(e))
        return {"error": str(e)}, 500


# ==========================
# MAIN
# ==========================
if __name__ == "__main__":

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
