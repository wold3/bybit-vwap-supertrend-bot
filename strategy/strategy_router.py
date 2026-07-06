from market.candle_builder import candle_builder
from strategy.vwap import calculate_vwap
from strategy.supertrend import supertrend


def update_market_state(price, volume):

    candles = candle_builder.get_candles()

    vwap = calculate_vwap(candles)
    signal = supertrend(candles)

    return {
        "price": price,
        "vwap": vwap,
        "signal": signal
    }
