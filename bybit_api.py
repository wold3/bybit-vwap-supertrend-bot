import time
from pybit.unified_trading import HTTP

from config import *
from state import load_state, save_state

session = HTTP(
    testnet=TESTNET,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET
)

STATE = load_state()

LAST = ""
LAST_TIME = 0


def log(msg):
    print(msg)


# -------------------------
# Position
# -------------------------

def get_position(symbol):

    try:
        res = session.get_positions(
            category=CATEGORY,
            symbol=symbol
        )
        return res["result"]["list"][0]
    except:
        return None


def get_side(symbol):

    pos = get_position(symbol)

    if not pos:
        return None

    if float(pos["size"]) == 0:
        return None

    return "LONG" if pos["side"] == "Buy" else "SHORT"


# -------------------------
# TP / SL
# -------------------------

def calc_tp_sl(price, side):

    if side == "LONG":
        return (
            price * (1 + TAKE_PROFIT_PCT / 100),
            price * (1 - STOP_LOSS_PCT / 100)
        )

    return (
        price * (1 - TAKE_PROFIT_PCT / 100),
        price * (1 + STOP_LOSS_PCT / 100)
    )


# -------------------------
# Order
# -------------------------

def order(side, qty, symbol, reduce=False, tp=None, sl=None):

    return session.place_order(
        category=CATEGORY,
        symbol=symbol,
        side=side,
        orderType="Market",
        qty=str(qty),
        reduceOnly=reduce,
        positionIdx=POSITION_IDX,
        takeProfit=tp,
        stopLoss=sl
    )


# -------------------------
# Close
# -------------------------

def close(symbol):

    pos = get_position(symbol)

    if not pos:
        return None

    size = float(pos["size"])

    if size == 0:
        return None

    side = pos["side"]

    close_side = "Sell" if side == "Buy" else "Buy"

    return order(close_side, size, symbol, reduce=True)


# -------------------------
# Telegram (optional)
# -------------------------

def notify(msg):
    print(msg)


# -------------------------
# Risk
# -------------------------

def risk_ok():

    # placeholder (확장 가능)
    return True


# -------------------------
# State
# -------------------------

def save(symbol, signal):

    STATE[symbol] = signal
    save_state(STATE)


# -------------------------
# Execute
# -------------------------

def execute(signal, symbol, qty):

    global LAST, LAST_TIME

    now = time.time()

    if signal == LAST and now - LAST_TIME < 5:
        return None

    LAST = signal
    LAST_TIME = now

    if not risk_ok():
        return None

    save(symbol, signal)

    log(f"{signal} {symbol}")

    # BUY
    if signal == "BUY":

        if get_side(symbol) == "SHORT":
            close(symbol)

        entry = order("Buy", qty, symbol)

        try:
            price = float(entry["result"]["price"])
        except:
            price = 0

        tp, sl = calc_tp_sl(price, "LONG")

        return entry

    # SHORT
    if signal == "SHORT":

        if get_side(symbol) == "LONG":
            close(symbol)

        entry = order("Sell", qty, symbol)

        try:
            price = float(entry["result"]["price"])
        except:
            price = 0

        tp, sl = calc_tp_sl(price, "SHORT")

        return entry

    # EXIT LONG
    if signal == "SELL":
        return close(symbol)

    # EXIT SHORT
    if signal == "EXIT":
        return close(symbol)

    return None
