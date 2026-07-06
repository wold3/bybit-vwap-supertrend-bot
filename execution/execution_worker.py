import logging

from services.event_bus import event_bus
from execution.execution_engine import engine
from execution.order_manager import order_manager
from risk.risk_engine import risk_engine
from ai.trading_brain import brain

logger = logging.getLogger(__name__)


def worker_loop():

    q = event_bus.subscribe()

    while True:

        event = q.get()

        if event["type"] != "TICK":
            continue

        symbol = event["symbol"]
        price = event["price"]

        order_manager.sync()

        decision = brain.decide(symbol, price)
        signal = decision["strategy"]

        engine.execute(
            signal=signal,
            symbol=symbol,
            qty=1,
            price=price
        )

        pnl = 0  # real PnL hook 자리

        risk_engine.update_pnl(pnl)

        print(f"[v6] {symbol} {price} {signal} PnL={risk_engine.pnl}")
