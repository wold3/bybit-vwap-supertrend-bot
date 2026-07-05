from config import RISK_PER_TRADE, MIN_ORDER_QTY, MAX_ORDER_QTY


def get_balance():
    return 1000


def calculate_qty(entry_price, stop_loss):

    risk = get_balance() * RISK_PER_TRADE
    distance = abs(entry_price - stop_loss)

    if distance == 0:
        return MIN_ORDER_QTY

    qty = risk / distance

    return round(max(MIN_ORDER_QTY, min(qty, MAX_ORDER_QTY)), 6)
