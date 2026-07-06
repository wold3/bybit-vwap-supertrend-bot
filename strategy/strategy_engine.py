import time

from indicators.vwap_supertrend import calculate_vwap, supertrend
from portfolio.position_manager import position_manager
from risk.risk_engine import risk_engine


# =================================================
# MOCK MARKET DATA (실전에서는 WS로 교체)
# =================================================
def get_market_data():

    import random

    prices = [65000 + random.randint(-50, 50) for _ in range(20)]
    volumes = [random.randint(1, 10) for _ in range(20)]

    return prices, volumes


# =================================================
# SIGNAL
# =================================================
def generate_signal():

    prices, volumes = get_market_data()

    vwap = calculate_vwap(prices, volumes)
    st = supertrend(prices)

    last_price = prices[-1]

    if last_price > vwap and st == "UP":
        return "BUY"

    if last_price < vwap and st == "DOWN":
        return "SELL"

    return None


# =================================================
# STRATEGY ENGINE
# =================================================
def run_strategy(engine):

    symbol = "BTCUSDT"

    # 🚨 RISK GATE
    if not risk_engine.can_trade():
        print("[STRATEGY] BLOCKED BY RISK")
        return

    position = position_manager.get_position(symbol)

    # 포지션 있으면 진입 금지 + SL/TP 체크
    if position:

        exit_signal = engine.check_risk(symbol)

        if exit_signal:
            print(f"[STRATEGY] EXIT: {exit_signal}")
            return

        return

    # 신규 진입
    signal = generate_signal()

    if signal:

        print(f"[STRATEGY] SIGNAL: {signal}")

        engine.execute(
            symbol=symbol,
            side=signal,
            qty=0.001,
            price=0
        )

    time.sleep(0.5)
