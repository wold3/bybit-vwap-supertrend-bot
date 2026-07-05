from risk_engine import RiskEngine

risk_engine = RiskEngine()


def compute_reward(pnl):

    risk_engine.update(pnl)

    return risk_engine.risk_penalty(pnl)


def update_trade_result(pnl):
    # placeholder for PnL tracking
    pass
