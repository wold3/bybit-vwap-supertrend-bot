import logging
from flask import Flask, request

from config import HOST, PORT, DEBUG
from bybit_api import execute
from strategy_wrapper import execute_strategy
from telegram import send_trade, send_error

from transformer_agent import TransformerAgent
from sequence_builder import build_sequence
from state import compute_reward, update_trade_result
from risk_engine import RiskEngine


app = Flask(__name__)
logger = logging.getLogger(__name__)

agent = TransformerAgent()
risk_engine = RiskEngine()


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

        action = agent.act(state_seq)

        signal = ["HOLD", "BUY", "SELL"][action]

        # ==========================
        # STRATEGY FILTER
        # ==========================

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
        # PnL (SIMPLIFIED HOOK)
        # ==========================

        pnl = 0.0  # real execution 연결 가능

        reward = compute_reward(pnl)

        agent.store(state_seq, action, reward)

        agent.train()

        update_trade_result(pnl)

        return {
            "status": "success",
            "signal": signal,
            "reward": reward,
            "cvar": risk_engine.cvar()
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
