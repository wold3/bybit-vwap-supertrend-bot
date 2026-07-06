import time
import random

from indicators.vwap_supertrend import calculate_vwap, supertrend
from ml_filter import ml_filter

from portfolio.position_manager import position_manager
from risk.risk_engine import risk_engine


# =================================================
# MOCK MARKET DATA (실전에서는 WebSocket으로 교체)
# =================================================
def get_market_data():

    prices = [65000 + random.randint(-80, 80) for _ in range(30)]
    volumes = [random.randint(1, 10) for _ in range(30)]

    return prices, volumes


# =================================================
# BASE SIGNAL (VWAP + Supertrend)
# =================================================
def generate_base_signal(prices, volumes):

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

    # 🚨 1. GLOBAL RISK GATE
    if not risk_engine.can_trade():
        print("[STRATEGY] BLOCKED BY RISK ENGINE")
        return

    # =================================================
    # 2. POSITION CHECK
    # =================================================
    position = position_manager.get_position(symbol)

    if position:

        # SL / TP 체크 (engine 내부 로직 호출)
        exit_signal = engine.check_risk(symbol)

        if exit_signal:
            print(f"[STRATEGY] EXIT SIGNAL: {exit_signal}")

        return

    # =================================================
    # 3. MARKET DATA
    # =================================================
    prices, volumes = get_market_data()

    # =================================================
    # 4. BASE SIGNAL (TECH FILTER)
    # =================================================
    base_signal = generate_base_signal(prices, volumes)

    if not base_signal:
        print("[STRATEGY] NO TECH SIGNAL")
        return

    # =================================================
    # 5. ML FILTER (QUALITY FILTER)
    # =================================================
    allow, prob = ml_filter.allow_trade(prices, volumes)

    if not allow:
        print(f"[ML FILTER] BLOCKED | prob={prob:.2f}")
        return

    print(f"[ML FILTER] PASS | prob={prob:.2f}")

    # =================================================
    # 6. FINAL EXECUTION
    # =================================================
    engine.execute(
        symbol=symbol,
        side=base_signal,
        qty=0.001,
        price=0
    )

    time.sleep(0.5)
