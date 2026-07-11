from market.candle_builder import candle_builder
from strategy.vwap import calculate_vwap
from strategy.supertrend import supertrend
from config import SYMBOL


def update_market_state(price, volume):

    # 새 틱 반영
    candle_builder.update(
        SYMBOL,
        price,
        volume
    )

    # 최신 캔들 조회
    candles = candle_builder.get_candles(
        SYMBOL
    )

    # 데이터 부족 시
    if len(candles) < 20:
        return {
            "price": price,
            "vwap": None,
            "signal": None
        }

    vwap = calculate_vwap(candles)
    signal = supertrend(candles)

    return {
        "price": price,
        "vwap": vwap,
        "signal": signal
    }
