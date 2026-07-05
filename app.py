from flask import Flask, request

from sequence_builder import build_sequence
from world_agent import WorldAgent
from bybit_api import execute
from strategy_wrapper import execute_strategy
from risk_engine import RiskEngine
from portfolio_manager import PortfolioManager


app = Flask(__name__)

agent = WorldAgent()
risk = RiskEngine()
portfolio = PortfolioManager()


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    symbol = data["symbol"]
    price = data["price"]
    qty = data["qty"]
    orderbook = data.get("orderbook")

    # ==========================
    # STATE
    # ==========================

    state_seq = build_sequence(price, orderbook)

    # ==========================
    # PLANNING
    # ==========================

    action = agent.act(state_seq)

    signal = ["HOLD", "BUY", "SELL"][action]

    decision = execute_strategy(signal, price)

    if not decision["success"]:
        return {"status": "filtered"}

    # ==========================
    # SAFETY LAYER
    # ==========================

    if not portfolio.allow_trade():
        return {"status": "risk_blocked"}

    # ==========================
    # EXECUTION
    # ==========================

    order = execute(signal, symbol, qty)

    pnl = 0.0  # real PnL hook 필요

    risk.update(pnl)
    portfolio.update(symbol, pnl)

    return {
        "status": "success",
        "signal": signal,
        "cvar": risk.cvar(),
        "exposure": portfolio.risk_exposure()
    }


if __name__ == "__main__":
    app.run()
