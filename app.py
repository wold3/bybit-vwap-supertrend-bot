import logging

from flask import Flask, jsonify, request

from config import DEBUG, HOST, PORT
from signal_parser import validate
from state import can_trade, get_status, update_trade_result, compute_reward
from bybit_api import execute
from telegram import send_error, send_status, send_trade
from strategy_wrapper import execute_strategy

from dqn_agent import Agent


# ==========================
# INIT
# ==========================

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

        signal = result["signal"]
        symbol = result["symbol"]
        qty = result["qty"]
        price = result["price"]

        # ==========================
        # AI DECISION
        # ==========================

        state_vec = [price, 0, 0]
        action = agent.act(state_vec)

        ai_signal = ["HOLD", "BUY", "SELL"][action]

        # ==========================
        # FILTER
        # ==========================

        decision = execute_strategy(signal, price)

        if not decision["success"]:
            return {"status": "filtered"}

        # ==========================
        # EXECUTE
        # ==========================

        order = execute(ai_signal, symbol, qty)

        if not order.get("success"):
            send_error(order.get("error"))
            return order, 500

        send_trade(ai_signal, symbol, qty, price)

        # ==========================
        # LEARNING STEP (NEW)
        # ==========================

        pnl = 0  # 실제 pnl 연결 가능

        reward = compute_reward(pnl)

        next_state = [price, 0, 0]

        agent.buffer.push(
            state_vec,
            action,
            reward,
            next_state
        )

        agent.train()
        agent.soft_update()

        update_trade_result(pnl)

        return {
            "status": "success",
            "action": ai_signal
        }

    except Exception as e:
        logger.exception(e)
        send_error(str(e))
        return {"error": str(e)}, 500


# ==========================
# MAIN
# ==========================
if __name__ == "__main__":

    send_status("🚀 DQN Trading Bot Started")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
