import time

trade_count = 0
last_reset = time.time()

position = {
    "active": False,
    "entry_price": 0,
    "highest_price": 0,
    "trailing_stop": 0,
    "daily_pnl": 0,
    "trades": 0
}


def can_trade():
    global trade_count, last_reset

    now = time.time()

    if now - last_reset > 60:
        trade_count = 0
        last_reset = now

    if trade_count >= MAX_TRADES_PER_MIN:
        return False

    trade_count += 1
    return True


def add_trade():
    position["trades"] += 1


def update_price(price):
    if not position["active"]:
        return

    position["highest_price"] = max(position["highest_price"], price)


def update_trailing():
    entry = position["entry_price"]
    high = position["highest_price"]

    if entry == 0:
        return

    gain_pct = ((high - entry) / entry) * 100

    if gain_pct < 1.0:
        return

    new_stop = high * (1 - 0.005)

    position["trailing_stop"] = max(position["trailing_stop"], new_stop)


def should_exit(price):
    if not position["active"]:
        return False

    return price <= position["trailing_stop"]


def update_pnl(pnl):
    position["daily_pnl"] += pnl


def reset_day():
    position["daily_pnl"] = 0
    position["trades"] = 0
