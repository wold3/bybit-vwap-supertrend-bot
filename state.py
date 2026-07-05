import time

trade_count = 0
last_reset = time.time()

positions = {
    "BTCUSDT": {"active": False, "entry_price": 0, "highest_price": 0, "trailing_stop": 0},
    "ETHUSDT": {"active": False, "entry_price": 0, "highest_price": 0, "trailing_stop": 0},
    "SOLUSDT": {"active": False, "entry_price": 0, "highest_price": 0, "trailing_stop": 0}
}


def get_position(symbol):
    return positions[symbol]


def can_trade():
    global trade_count, last_reset

    if time.time() - last_reset > 60:
        trade_count = 0
        last_reset = time.time()

    if trade_count >= MAX_TRADES_PER_MIN:
        return False

    trade_count += 1
    return True


def update_price(symbol, price):
    if positions[symbol]["active"]:
        positions[symbol]["highest_price"] = max(
            positions[symbol]["highest_price"],
            price
        )


def update_trailing(symbol):
    pos = positions[symbol]

    if not pos["active"]:
        return

    if pos["highest_price"] > pos["entry_price"] * 1.01:
        pos["trailing_stop"] = max(
            pos["trailing_stop"],
            pos["highest_price"] * 0.995
        )


def should_exit(symbol, price):
    pos = positions[symbol]
    return pos["active"] and price <= pos["trailing_stop"]
