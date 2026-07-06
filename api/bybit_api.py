import logging
import time
from functools import wraps

from pybit.unified_trading import HTTP

from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    TESTNET,
)

logger = logging.getLogger(__name__)

session = HTTP(
    testnet=TESTNET,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)


# =====================================================
# Retry
# =====================================================

def retry(max_retry=3, delay=1):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            last_error = None

            for i in range(max_retry):

                try:
                    return func(*args, **kwargs)

                except Exception as e:

                    last_error = e

                    logger.warning(
                        "%s retry %d/%d : %s",
                        func.__name__,
                        i + 1,
                        max_retry,
                        e,
                    )

                    time.sleep(delay)

            raise last_error

        return wrapper

    return decorator


# =====================================================
# Common
# =====================================================

def _convert_side(signal: str) -> str:

    signal = signal.upper()

    if signal == "BUY":
        return "Buy"

    if signal in (
        "SELL",
        "SHORT",
        "EXIT",
    ):
        return "Sell"

    raise ValueError(
        f"Unknown signal : {signal}"
    )


# =====================================================
# Market Order
# =====================================================

@retry()
def execute(
    signal,
    symbol,
    qty,
):
    """
    Backward compatible wrapper
    """

    return execute_market(
        signal,
        symbol,
        qty,
    )


@retry()
def execute_market(
    signal,
    symbol,
    qty,
):

    side = _convert_side(signal)

    logger.info(
        "MARKET %s %s qty=%s",
        side,
        symbol,
        qty,
    )

    response = session.place_order(
        category="linear",
        symbol=symbol,
        side=side,
        orderType="Market",
        qty=str(qty),
        timeInForce="IOC",
    )

    return {
        "success": True,
        "response": response,
    }


# =====================================================
# Limit Order
# =====================================================

@retry()
def execute_limit(
    signal,
    symbol,
    qty,
    price,
):

    side = _convert_side(signal)

    logger.info(
        "LIMIT %s %s qty=%s price=%s",
        side,
        symbol,
        qty,
        price,
    )

    response = session.place_order(
        category="linear",
        symbol=symbol,
        side=side,
        orderType="Limit",
        qty=str(qty),
        price=str(price),
        timeInForce="GTC",
    )

    return {
        "success": True,
        "response": response,
    }

# =====================================================
# Cancel Order
# =====================================================

@retry()
def cancel_order(
    symbol,
    order_id,
):

    logger.info(
        "CANCEL %s order=%s",
        symbol,
        order_id,
    )

    response = session.cancel_order(
        category="linear",
        symbol=symbol,
        orderId=order_id,
    )

    return {
        "success": True,
        "response": response,
    }


# =====================================================
# Cancel All Orders
# =====================================================

@retry()
def cancel_all_orders(symbol):

    logger.info(
        "CANCEL ALL %s",
        symbol,
    )

    response = session.cancel_all_orders(
        category="linear",
        symbol=symbol,
    )

    return {
        "success": True,
        "response": response,
    }


# =====================================================
# Open Orders
# =====================================================

@retry()
def get_open_orders(symbol):

    result = session.get_open_orders(
        category="linear",
        symbol=symbol,
    )

    return result.get(
        "result",
        {},
    ).get(
        "list",
        [],
    )


# =====================================================
# Order History
# =====================================================

@retry()
def get_order_history(
    symbol,
    limit=50,
):

    result = session.get_order_history(
        category="linear",
        symbol=symbol,
        limit=limit,
    )

    return result.get(
        "result",
        {},
    ).get(
        "list",
        [],
    )


# =====================================================
# Position
# =====================================================

@retry()
def get_positions(symbol=None):

    kwargs = {
        "category": "linear",
    }

    if symbol:
        kwargs["symbol"] = symbol

    result = session.get_positions(
        **kwargs,
    )

    return result.get(
        "result",
        {},
    ).get(
        "list",
        [],
    )


@retry()
def get_position(symbol):

    positions = get_positions(symbol)

    if not positions:
        return None

    return positions[0]


# =====================================================
# Close Position
# =====================================================

@retry()
def close_position(symbol):

    position = get_position(symbol)

    if position is None:
        return {
            "success": False,
            "error": "No position",
        }

    size = float(
        position.get("size", 0)
    )

    if size <= 0:
        return {
            "success": False,
            "error": "Position size is zero",
        }

    side = position.get("side")

    close_side = (
        "Sell"
        if side == "Buy"
        else "Buy"
    )

    logger.info(
        "CLOSE %s size=%s",
        symbol,
        size,
    )

    response = session.place_order(
        category="linear",
        symbol=symbol,
        side=close_side,
        orderType="Market",
        qty=str(size),
        reduceOnly=True,
        timeInForce="IOC",
    )

    return {
        "success": True,
        "response": response,
    }


# =====================================================
# Reduce Only Order
# =====================================================

@retry()
def reduce_only_order(
    signal,
    symbol,
    qty,
):

    side = _convert_side(signal)

    logger.info(
        "REDUCE %s %s qty=%s",
        side,
        symbol,
        qty,
    )

    response = session.place_order(
        category="linear",
        symbol=symbol,
        side=side,
        orderType="Market",
        qty=str(qty),
        reduceOnly=True,
        timeInForce="IOC",
    )

    return {
        "success": True,
        "response": response,
    }

# =====================================================
# Wallet
# =====================================================

@retry()
def get_wallet_balance():

    result = session.get_wallet_balance(
        accountType="UNIFIED",
    )

    return result


@retry()
def get_balance(coin="USDT"):

    result = session.get_wallet_balance(
        accountType="UNIFIED",
    )

    accounts = (
        result.get("result", {})
        .get("list", [])
    )

    if not accounts:
        return 0.0

    coins = accounts[0].get("coin", [])

    for item in coins:

        if item.get("coin") == coin:

            return float(
                item.get(
                    "walletBalance",
                    0,
                )
            )

    return 0.0


# =====================================================
# Market
# =====================================================

@retry()
def get_ticker(symbol):

    result = session.get_tickers(
        category="linear",
        symbol=symbol,
    )

    tickers = (
        result.get("result", {})
        .get("list", [])
    )

    if not tickers:
        return None

    return tickers[0]


@retry()
def get_last_price(symbol):

    ticker = get_ticker(symbol)

    if ticker is None:
        return None

    return float(
        ticker.get(
            "lastPrice",
            0,
        )
    )


@retry()
def get_kline(
    symbol,
    interval="1",
    limit=200,
):

    result = session.get_kline(
        category="linear",
        symbol=symbol,
        interval=interval,
        limit=limit,
    )

    return (
        result.get("result", {})
        .get("list", [])
    )


# =====================================================
# Leverage
# =====================================================

@retry()
def set_leverage(
    symbol,
    leverage,
):

    logger.info(
        "SET LEVERAGE %s -> %s",
        symbol,
        leverage,
    )

    response = session.set_leverage(
        category="linear",
        symbol=symbol,
        buyLeverage=str(leverage),
        sellLeverage=str(leverage),
    )

    return {
        "success": True,
        "response": response,
    }


# =====================================================
# TP / SL
# =====================================================

@retry()
def set_trading_stop(
    symbol,
    take_profit=None,
    stop_loss=None,
    trailing_stop=None,
):

    params = {
        "category": "linear",
        "symbol": symbol,
    }

    if take_profit is not None:
        params["takeProfit"] = str(
            take_profit
        )

    if stop_loss is not None:
        params["stopLoss"] = str(
            stop_loss
        )

    if trailing_stop is not None:
        params["trailingStop"] = str(
            trailing_stop
        )

    response = session.set_trading_stop(
        **params
    )

    return {
        "success": True,
        "response": response,
    }


# =====================================================
# Unrealized PnL
# =====================================================

@retry()
def get_unrealized_pnl(symbol):

    position = get_position(symbol)

    if position is None:
        return 0.0

    return float(
        position.get(
            "unrealisedPnl",
            0,
        )
    )


# =====================================================
# Position Value
# =====================================================

@retry()
def get_position_value(symbol):

    position = get_position(symbol)

    if position is None:
        return 0.0

    return float(
        position.get(
            "positionValue",
            0,
        )
    )


# =====================================================
# Margin
# =====================================================

@retry()
def get_position_margin(symbol):

    position = get_position(symbol)

    if position is None:
        return 0.0

    return float(
        position.get(
            "positionIM",
            0,
        )
    )
