import time

trade_count = 0
last_reset = time.time()

position = {
    "entry_price": 0,
    "highest_profit": 0,
    "daily_pnl": 0,
    "trades": 0
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


def add_trade():
    position["trades"] += 1


def update_position(entry_price, profit):
    position["entry_price"] = entry_price
    position["highest_profit"] = max(position["highest_profit"], profit)


def update_pnl(pnl):
    position["daily_pnl"] += pnl


def reset_day():
    position["daily_pnl"] = 0
    position["trades"] = 0
    position["highest_profit"] = 0
