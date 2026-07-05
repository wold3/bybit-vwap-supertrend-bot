import time

trade_count = 0
last_reset = time.time()

def can_trade():

    global trade_count, last_reset

    if time.time() - last_reset > 60:
        trade_count = 0
        last_reset = time.time()

    if trade_count >= MAX_TRADES_PER_MIN:
        return False

    trade_count += 1
    return True
