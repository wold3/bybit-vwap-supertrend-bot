import time

trade_count = 0
last_reset = time.time()

position = {
    "entry_price": 0,
    "highest_profit": 0,
    "daily_pnl": 0
}


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


def update_position(entry_price, profit):
    global position

    position["entry_price"] = entry_price
    position["highest_profit"] = max(position["highest_profit"], profit)


def update_pnl(pnl):
    global position
    position["daily_pnl"] += pnl
