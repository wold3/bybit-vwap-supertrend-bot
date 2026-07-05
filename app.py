import logging
from flask import Flask, request

from config import HOST, PORT, DEBUG
from bybit_api import execute
from strategy_wrapper import execute_strategy
from telegram import send_trade, send_error

from sequence_builder import build_sequence
from ssl_trainer import SSLTrainer
from transformer_agent import TransformerAgent
from risk_engine import RiskEngine


app = Flask(__name__)
logger = logging.getLogger(__name__)

ssl = SSLTrainer()
agent = TransformerAgent()
risk = RiskEngine()


@app.route("/webhook", methods=["POST"])
def webhook():

    try:

        data = request.get_json()

        symbol = data["symbol"]
        price = data["price"]
        qty = data["qty"]
        orderbook = data.get("orderbook")

        # ==========================
        # SEQUENCE
        # ==========================

        state_seq = build_sequence(price, orderbook)

        # ==========================
        # SELF-SUPERVISED LEARNING
        # ==========================

        ssl.add(state_seq)
        ssl.train_step()

        # ==========================
        # POLICY (Transformer)
        # ==========================

        action = agent.act(state_seq)

        signal = ["HOLD", "BUY", "SELL"][action]

        decision = execute_strategy(signal, price)

        if not decision["success"]:
            return {"status": "filtered"}

        order = execute(signal, symbol, qty)

        if not order.get("success"):
            send_error(order.get("error"))
            return order, 500

        send_trade(signal, symbol, qty, price)

        # ==========================
        # RISK-ADJUSTED REWARD
        # ==========================

        pnl = 0.0  # real PnL 연결 가능

        risk.update(pnl)
        reward = risk.risk_penalty(pnl)

        agent.store(state_seq, action, reward)
        agent.train()

        return {
            "status": "success",
            "signal": signal,
            "cvar": risk.cvar()
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
