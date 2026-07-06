import logging

from services.event_bus import event_bus
from api.order_manager import order_manager
from execution.execution_engine import engine
from risk.risk_engine import risk_engine
from ai.trading_brain import brain

logger = logging.getLogger(__name__)


def worker_loop():

    q = event_bus.subscribe()

    while True:

        try:

            event = q.get()

            if event["type"] != "PRICE":
                continue

            symbol = event["symbol"]
            price = event["price"]

            order_manager.sync_orders()

            exit_reason = engine.check_exit(symbol, price)

            if exit_reason:
                engine.close_position(symbol, exit_reason)

                pnl = engine.get_real_pnl(symbol)
                risk_engine.update_pnl(pnl)

                continue

            decision = brain.decide(symbol, price)
            signal = decision["strategy"]

            engine.execute(
                signal=signal,
                symbol=symbol,
                qty=1,
                price=price
            )

            pnl = engine.get_real_pnl(symbol)

            risk_engine.update_pnl(pnl)
            brain.record(signal, pnl)

            print(f"[{symbol}] {price} {signal} PnL={pnl}")

        except Exception as e:
            logger.error(f"WORKER ERROR: {e}")
