import time
import logging

from services.event_bus import event_bus
from api.order_manager import order_manager
from execution.execution_engine import engine
from ai.trading_brain import brain
from risk.risk_engine import risk_engine
from strategy.strategy_wrapper import execute_strategy

logger = logging.getLogger(__name__)


def worker_loop():

    q = event_bus.subscribe()

    latest_price = {}

    while True:

        try:

            event = q.get()

            if event["type"] == "PRICE":

                symbol = event["symbol"]
                price = event["price"]

                latest_price[symbol] = price

                # =========================
                # SYNC (real-time)
                # =========================
                order_manager.sync_orders()
                engine.sync_positions(symbol)

                # =========================
                # TP/SL
                # =========================
                exit_reason = engine.check_exit(symbol, price)

                if exit_reason:
                    engine.close_position(symbol, exit_reason)
                    risk_engine.update(0)
                    logger.info(f"[{symbol}] CLOSED {exit_reason}")
                    continue

                # =========================
                # STRATEGY
                # =========================
                decision = brain.decide(symbol, price)
                strategy = decision["strategy"]

                # =========================
                # EXECUTION
                # =========================
                execute_strategy(
                    signal=strategy,
                    price=price,
                    symbol=symbol,
                    equity=1000
                )

                # =========================
                # PnL
                # =========================
                pnl = engine.get_real_pnl(symbol)

                risk_engine.update(pnl)
                brain.record(strategy, pnl)

                logger.info(f"[{symbol}] PRICE={price} STRAT={strategy} PNL={pnl}")

        except Exception as e:
            logger.error(f"WORKER ERROR: {str(e)}")
            time.sleep(0.1)
