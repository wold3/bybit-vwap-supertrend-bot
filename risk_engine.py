state = {
    "daily_pnl": 0,
    "consecutive_losses": 0
}


def update_pnl(pnl):

    state["daily_pnl"] += pnl

    if pnl < 0:
        state["consecutive_losses"] += 1
    else:
        state["consecutive_losses"] = 0


def should_stop_trading():

    if state["daily_pnl"] <= -30:
        return True

    if state["consecutive_losses"] >= 5:
        return True

    return False
