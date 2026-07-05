import time

trade_count = 0
last_reset = time.time()

positions = {
    "BTCUSDT": {"active": False, "entry_price": 0, "highest_price": 0, "trailing_stop": 0, "daily_pnl": 0, "stop_loss": 0},
    "ETHUSDT": {"active": False, "entry_price": 0, "highest_price": 0, "trailing_stop": 0, "daily_pnl": 0, "stop_loss": 0},
    "SOLUSDT": {"active": False, "entry_price": 0, "highest_price": 0, "trailing_stop": 0, "daily_pnl": 0, "stop_loss": 0}
}


def get_position(symbol):
    return positions[symbol]


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


def update_price(symbol, price):
    pos = positions[symbol]
    if pos["active"]:
        pos["highest_price"] = max(pos["highest_price"], price)


def update_trailing(symbol):
    pos = positions[symbol]

    if not pos["active"]:
        return

    entry = pos["entry_price"]
    high = pos["highest_price"]

    if entry == 0:
        return

    if high > entry * 1.01:
        pos["trailing_stop"] = max(pos["trailing_stop"], high * 0.995)


def should_exit(symbol, price):
    pos = positions[symbol]
    return pos["active"] and price <= pos["trailing_stop"]
