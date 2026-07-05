import logging

from pybit.unified_trading import HTTP

from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    TESTNET,
    LEVERAGE,
)

logger = logging.getLogger(__name__)


# =====================================================
# Session
# =====================================================

session = HTTP(
    testnet=TESTNET,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)


# =====================================================
# Order Execution
# =====================================================

def execute(signal, symbol, qty):
    """
    Execute market order on Bybit
    """

    signal = signal.upper()

    try:

        # -----------------------------
        # Side Mapping
        # -----------------------------

        if signal == "BUY":
            side = "Buy"

        elif signal in ("SELL", "SHORT"):
            side = "Sell"

        elif signal == "EXIT":
            # position close (reduce-only sell)
            side = "Sell"

        else:
            raise ValueError(f"Unknown signal: {signal}")

        # -----------------------------
        # Place Order
        # -----------------------------

        response = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=str(round(float(qty), 6)),
            timeInForce="IOC",
            reduceOnly=(signal == "EXIT"),
        )

        logger.info(
            "ORDER EXECUTED | signal=%s symbol=%s qty=%s",
            signal,
            symbol,
            qty,
        )

        return {
            "success": True,
            "signal": signal,
            "response": response,
        }

    except Exception as e:

        logger.exception("Order failed")

        return {
            "success": False,
            "error": str(e),
        }


# =====================================================
# Balance
# =====================================================

def get_balance():

    try:

        result = session.get_wallet_balance(
            accountType="UNIFIED"
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as e:

        logger.exception("Balance fetch failed")

        return {
            "success": False,
            "error": str(e),
        }


# =====================================================
# Position
# =====================================================

def get_position(symbol):

    try:

        result = session.get_positions(
            category="linear",
            symbol=symbol,
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as e:

        logger.exception("Position fetch failed")

        return {
            "success": False,
            "error": str(e),
        }


# =====================================================
# Ticker
# =====================================================

def get_ticker(symbol):

    try:

        result = session.get_tickers(
            category="linear",
            symbol=symbol,
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as e:

        logger.exception("Ticker fetch failed")

        return {
            "success": False,
            "error": str(e),
        }
