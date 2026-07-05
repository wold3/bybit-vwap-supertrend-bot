state = {
    "pnl": 0,
    "loss_streak": 0
}


def update_pnl(pnl):

    state["pnl"] += pnl

    if pnl < 0:
        state["loss_streak"] += 1
    else:
        state["loss_streak"] = 0


def should_stop():

    if state["pnl"] < -30:
        return True

    if state["loss_streak"] >= 5:
        return True

    return False
