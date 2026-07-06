from execution.execution_engine import engine


def execute_strategy(signal, price, symbol, equity):

    # 간단 position sizing (초기 안정형)
    qty = max(1, int(equity * 0.001))

    leverage = 1

    return engine.execute(
        signal=signal,
        symbol=symbol,
        qty=qty,
        price=price,
        leverage=leverage
    )
