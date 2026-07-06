def atr(candles, period=10):

    trs = []

    for i in range(1, len(candles)):
        c = candles[i]
        p = candles[i - 1]

        tr = max(
            c["high"] - c["low"],
            abs(c["high"] - p["close"]),
            abs(c["low"] - p["close"])
        )

        trs.append(tr)

    if len(trs) < period:
        return None

    return sum(trs[-period:]) / period


def supertrend(candles, period=10, multiplier=3):

    if len(candles) < period + 1:
        return None

    a = atr(candles, period)
    if a is None:
        return None

    last = candles[-1]

    hl2 = (last["high"] + last["low"]) / 2

    upper = hl2 + multiplier * a
    lower = hl2 - multiplier * a

    close = last["close"]

    if close > upper:
        return "BUY"
    elif close < lower:
        return "SELL"
    return "HOLD"
