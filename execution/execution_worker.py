import logging

from services.event_bus import event_bus
from execution.orderbook_engine import orderbook_engine
from execution.execution_engine import engine
from risk.risk_engine import risk_engine
from ai.trading_brain import brain

logger = logging.getLogger(__name__)


def worker_loop():

    q = event_bus.subscribe()

    while True:

        try:

            event = q.get()

            # ORDERBOOK
            if event["type"] == "ORDERBOOK":

                orderbook_engine.update(
                    event["symbol"],
                    event["bids"],
                    event["asks"]
                )
                continue

            # TICK
            if event["type"] != "TICK":
                continue

            symbol = event["symbol"]
            price = event["price"]

            liquidity = orderbook_engine.liquidity_score(symbol)

            if liquidity < 100:
                continue

            decision = brain.decide(symbol, price)
            signal = decision["strategy"]

            engine.execute(
                signal=signal,
                symbol=symbol,
                qty=1,
                price=price
            )

            pnl = 0
            risk_engine.update_pnl(pnl)

            print(f"[v5] {symbol} {price} {signal} LQ={liquidity}")

        except Exception as e:
            logger.error(f"WORKER ERROR: {e}")
