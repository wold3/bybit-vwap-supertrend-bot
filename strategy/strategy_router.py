from market.candle_builder import candle_builder
from strategy.vwap import calculate_vwap
from strategy.supertrend import calculate_supertrend

from config import SYMBOL

import pandas as pd


def update_market_state(price, volume):

    candle_builder.update(
        SYMBOL,
        price,
        volume
    )

    candles = candle_builder.get_candles(SYMBOL)

    if len(candles) < 20:
        return {
            "price": price,
            "vwap": None,
            "signal": None
        }

    df = pd.DataFrame(candles)

    vwap = calculate_vwap(df)

    trend = calculate_supertrend(df)

    if trend is True:
        signal = "Buy"
    elif trend is False:
        signal = "Sell"
    else:
        signal = None

    return {
        "price": price,
        "vwap": vwap,
        "signal": signal
    }
