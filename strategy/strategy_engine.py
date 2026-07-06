import time
import random

from portfolio.position_manager import position_manager
from risk.risk_engine import risk_engine


# =====================================================
# SIGNAL GENERATOR (placeholder)
# =====================================================
def generate_signal():

    # TODO: VWAP / Supertrend / ML
    return random.choice(["BUY", "SELL", None])


# =====================================================
# STRATEGY ENGINE
# =====================================================
def run_strategy(engine):

    symbol = "BTCUSDT"

    # =================================================
    # 🚨 GLOBAL RISK GATE (최상단 차단)
    # =================================================
    if not risk_engine.can_trade():
        print("[STRATEGY] BLOCKED BY RISK ENGINE")
        return

    # =================================================
    # 1. 포지션 체크
    # =================================================
    position = position_manager.get_position(symbol)

    if position:

        # SL / TP 체크 (execution 내부 아님 → strategy가 트리거)
        exit_signal = engine.check_risk(symbol)

        if exit_signal:
            print(f"[STRATEGY] EXIT: {exit_signal}")
            return

        # 포지션 있으면 신규 진입 금지
        return

    # =================================================
    # 2. 신규 진입
    # =================================================
    signal = generate_signal()

    if signal:

        print(f"[STRATEGY] SIGNAL: {signal}")

        engine.execute(
            symbol=symbol,
            side=signal,
            qty=0.001,
            price=0
        )

    else:

        print("[STRATEGY] NO SIGNAL")

    time.sleep(0.5)
