import logging

from services.event_bus import event_bus

from api.order_manager import order_manager
from execution.execution_engine import safe_execute
from risk.risk_engine import risk_engine

from ai.trading_brain import brain
from strategy.strategy_wrapper import execute_strategy

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

            decision = brain.decide(symbol, price)
            strategy = decision["strategy"]

            safe_execute(
                execute_strategy,
                signal=strategy,
                price=price,
                symbol=symbol,
                equity=1000
            )

            pnl = 0
            risk_engine.update(pnl)
            brain.record(strategy, pnl)

            print(f"[{symbol}] PRICE={price} STRAT={strategy} PNL={pnl}")

        except Exception as e:
            logger.error(f"WORKER ERROR: {str(e)}")
