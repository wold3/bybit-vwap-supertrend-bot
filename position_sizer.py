from config import RISK_PER_TRADE, MIN_ORDER_QTY, MAX_ORDER_QTY


def get_balance():
    return 1000


def calculate_qty(entry_price, stop_loss):

    balance = get_balance()

    risk_amount = balance * RISK_PER_TRADE

    stop_distance = abs(entry_price - stop_loss)

    if stop_distance == 0:
        return MIN_ORDER_QTY

    qty = risk_amount / stop_distance

    return round(max(MIN_ORDER_QTY, min(qty, MAX_ORDER_QTY)), 6)
