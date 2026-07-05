import time

state = {
    "daily_pnl": 0,
    "start_balance": 1000,
    "peak_balance": 1000,
    "consecutive_losses": 0,
    "halt": False,
    "last_reset": time.time()
}


def update_pnl(pnl):

    state["daily_pnl"] += pnl

    if pnl < 0:
        state["consecutive_losses"] += 1
    else:
        state["consecutive_losses"] = 0


def should_stop_trading():

    drawdown = (state["peak_balance"] - state["start_balance"]) / state["start_balance"] * 100

    if state["daily_pnl"] <= -30:
        return True

    if state["consecutive_losses"] >= 5:
        return True

    if drawdown >= 5:
        return True

    return False
