import time
import logging

from config import SYMBOL

from api.websocket_client import ws_client
from api.order_manager import order_manager

from ai.trading_brain import brain
from strategy.strategy_router import update_market_state
from strategy.strategy_wrapper import execute_strategy

from execution.execution_engine import engine
from risk.risk_engine import risk_engine

from services.telegram_service import init_telegram, get_telegram
from services.watchdog_service import watchdog


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

latest_price = None


# =====================================================
# INIT
# =====================================================

def init_system():

    logger.info("SYSTEM INIT START")

    init_telegram(
        token="YOUR_TELEGRAM_TOKEN",
        chat_id="YOUR_CHAT_ID"
    )

    watchdog.start()

    logger.info("SYSTEM READY")


# =====================================================
# WS CALLBACK
# =====================================================

def on_price(price):
    global latest_price
    latest_price = price
    update_market_state(price, 0)


# =====================================================
# MAIN LOOP
# =====================================================

def run_trading():

    logger.info("TRADING STARTED")

    equity = 1000

    while True:

        try:

            if latest_price is None:
                time.sleep(0.2)
                continue

            price = latest_price

            # =================================================
            # 1) ORDER SYNC (체결 상태)
            # =================================================
            order_manager.sync_orders()

            # =================================================
            # 2) POSITION SYNC (핵심)
            # =================================================
            engine.sync_positions(SYMBOL)

            # =================================================
            # 3) TP / SL CHECK
            # =================================================
            exit_reason = engine.check_exit(SYMBOL, price)

            if exit_reason:

                engine.close_position(SYMBOL, exit_reason)

                risk_engine.update(0)

                logger.info(f"TP/SL CLOSED: {exit_reason}")

                time.sleep(0.5)
                continue

            # =================================================
            # 4) STRATEGY
            # =================================================
            decision = brain.decide("auto", price)

            strategy = decision["strategy"]

            # =================================================
            # 5) EXECUTION
            # =================================================
            execute_strategy(
                signal=strategy,
                price=price,
                symbol=SYMBOL,
                equity=equity
            )

            # =================================================
            # 6) REAL PnL (engine 내부 sync 기반)
            # =================================================
            pnl = engine.get_real_pnl(SYMBOL) if hasattr(engine, "get_real_pnl") else 0

            risk_engine.update(pnl)
            brain.record(strategy, pnl)

            logger.info(f"PRICE={price} STRATEGY={strategy} PNL={pnl}")

            time.sleep(2)

        except Exception as e:

            logger.error(f"MAIN ERROR: {str(e)}")

            tg = get_telegram()
            if tg:
                tg.error(e)

            time.sleep(5)


# =====================================================
# ENTRY
# =====================================================

if __name__ == "__main__":

    init_system()

    ws_client.set_price_callback(on_price)
    ws_client.start()

    run_trading()
