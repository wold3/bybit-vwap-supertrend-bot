def risk_rebalance(daily_pnl, win_streak):

    if daily_pnl > 3:
        return {
            "action": "reduce_leverage",
            "factor": 0.5
        }

    if daily_pnl < -2:
        return {
            "action": "stop"
        }

    if win_streak >= 3:
        return {
            "action": "reduce_size",
            "factor": 0.7
        }

    return {
        "action": "normal"
    }
