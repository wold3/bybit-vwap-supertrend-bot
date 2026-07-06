def volume_filter(volume):
    return volume > 0


def spread_filter(spread):
    return spread < 0.5


def cooldown_filter(last_trade_time, current_time):
    if last_trade_time is None:
        return True

    return (current_time - last_trade_time) > 30
