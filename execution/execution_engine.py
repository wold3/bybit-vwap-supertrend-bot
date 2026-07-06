def calc_tp_sl(price, volatility, regime):

    if regime == "TREND_UP":
        tp_mult = 2.0
        sl_mult = 1.0
    elif regime == "RANGE":
        tp_mult = 1.0
        sl_mult = 0.7
    else:
        tp_mult = 0.8
        sl_mult = 0.5

    tp = price * (1 + volatility * tp_mult)
    sl = price * (1 - volatility * sl_mult)

    return tp, sl


def trailing_stop(entry_price, current_price, regime):

    trail_pct = 0.3 if regime == "TREND_UP" else 0.6
    return current_price * (1 - trail_pct / 100)


def move_to_breakeven(entry_price, current_price):

    if current_price >= entry_price * 1.01:
        return entry_price
    return None


def partial_take_profit(entry_price, price):

    pnl_pct = (price - entry_price) / entry_price * 100

    if pnl_pct >= 2.0:
        return 1.0
    if pnl_pct >= 1.0:
        return 0.6
    if pnl_pct >= 0.5:
        return 0.3

    return 0.0
