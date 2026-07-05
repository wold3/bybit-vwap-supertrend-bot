import time

trade_count = 0
last_reset = time.time()


def can_trade():
    global trade_count, last_reset

    now = time.time()

    if now - last_reset > 60:
        trade_count = 0
        last_reset = now

    if trade_count >= 3:
        return False

    trade_count += 1
    return True
