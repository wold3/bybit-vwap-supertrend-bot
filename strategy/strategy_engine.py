import time
import random


# ================================
# SIMPLE STRATEGY ENGINE
# ================================
def generate_signal():

    # placeholder 전략 (VWAP / Supertrend 붙일 자리)
    return random.choice(["BUY", "SELL", None])


def run_strategy(engine):

    signal = generate_signal()

    if signal:

        print("[STRATEGY]", signal)

        engine.execute(
            symbol="BTCUSDT",
            side=signal,
            qty=0.001,
            price=0
        )
