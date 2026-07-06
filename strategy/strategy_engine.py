import time
import random

from portfolio.position_manager import position_manager


# =====================================================
# STRATEGY ENGINE (FINAL)
# =====================================================
def generate_signal():

    # -------------------------------------------------
    # TODO: 여기에 VWAP / Supertrend / ML 붙이면 됨
    # -------------------------------------------------
    return random.choice(["BUY", "SELL", None])


# =====================================================
# MAIN LOOP
# =====================================================
def run_strategy(engine):

    symbol = "BTCUSDT"

    # ============================================
    # 1. 현재 포지션 확인
    # ============================================
    position = position_manager.get_position(symbol)

    # ============================================
    # 2. SL/TP 먼저 체크 (핵심)
    # ============================================
    if position:

        exit_signal = engine.check_risk(symbol)

        if exit_signal:
            print(f"[STRATEGY] EXIT EXECUTED: {exit_signal}")
            return

        # 포지션 있으면 신규 진입 안함 (단순 구조)
        return

    # ============================================
    # 3. 신규 진입 신호 생성
    # ============================================
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

    # ============================================
    # throttle
    # ============================================
    time.sleep(0.5)
