def calculate_vwap(candles):

    if not candles:
        return None

    tpv = 0
    vol = 0

    for c in candles:
        tp = (c["high"] + c["low"] + c["close"]) / 3
        v = 1

        tpv += tp * v
        vol += v

    return tpv / vol if vol else None
