import logging

from flask import Flask, jsonify, request

from config import DEBUG, HOST, PORT
from signal_parser import validate
from state import can_trade, get_status, compute_reward, update_trade_result
from bybit_api import execute
from dqn_agent import Agent
from portfolio import PortfolioAgent
from telegram import send_trade, send_error


app = Flask(__name__)

agent = Agent()
portfolio = PortfolioAgent()


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

        price_map = result["prices"]  # dict 형태 가정

        symbols = portfolio.symbols

        # ==========================
        # MULTI STATE BUILD
        # ==========================

        market_states = {
            s: [price_map[s], 0, 0]
            for s in symbols
        }

        actions = {}
        pnls = {}

        # ==========================
        # AI DECISION PER SYMBOL
        # ==========================

        for symbol in symbols:

            state_vec = market_states[symbol]

            action = agent.act(state_vec)

            actions[symbol] = action

            signal = ["HOLD", "BUY", "SELL"][action]

            if signal == "HOLD":
                pnls[symbol] = 0
                continue

            order = execute(signal, symbol, 0.001)

            pnls[symbol] = 0  # 실제 pnl 연결 가능

        # ==========================
        # REWARD (PORTFOLIO LEVEL)
        # ==========================

        reward = compute_reward(pnls)

        for symbol in symbols:

            agent.buffer.push(
                market_states[symbol],
                actions[symbol],
                reward,
                market_states[symbol]
            )

        agent.train()
        agent.soft_update()

        update_trade_result(reward)

        return {
            "status": "success",
            "reward": reward,
            "actions": actions
        }

    except Exception as e:
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
