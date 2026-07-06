import time
import logging
import threading

from config import SYMBOLS

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


latest_price = {}


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
# WS CALLBACK (multi symbol)
# =====================================================
def on_price(symbol, price):

    latest_price[symbol] = price
    update_market_state(price, 0)


# =====================================================
# SYMBOL WORKER
# =====================================================
def symbol_loop(symbol):

    equity = 1000

    while True:

        try:

            if symbol not in latest_price:
                time.sleep(0.2)
                continue

            price = latest_price[symbol]

            # =========================
            # SYNC
            # =========================
            order_manager.sync_orders()
            engine.sync_positions(symbol)

            # =========================
            # TP / SL
            # =========================
            exit_reason = engine.check_exit(symbol, price)

            if exit_reason:
                engine.close_position(symbol, exit_reason)
                risk_engine.update(0)
                logger.info(f"[{symbol}] CLOSED {exit_reason}")
                time.sleep(0.5)
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
                equity=equity
            )

            # =========================
            # PnL
            # =========================
            pnl = engine.get_real_pnl(symbol) if hasattr(engine, "get_real_pnl") else 0

            risk_engine.update(pnl)
            brain.record(strategy, pnl)

            logger.info(f"[{symbol}] PRICE={price} STRAT={strategy} PNL={pnl}")

            time.sleep(2)

        except Exception as e:
            logger.error(f"[{symbol}] ERROR: {str(e)}")
            time.sleep(5)


# =====================================================
# MAIN
# =====================================================
def run_trading():

    logger.info("TRADING STARTED")

    threads = []

    for symbol in SYMBOLS:

        t = threading.Thread(
            target=symbol_loop,
            args=(symbol,),
            daemon=True
        )

        t.start()
        threads.append(t)

    while True:
        time.sleep(10)


# =====================================================
# ENTRY
# =====================================================
if __name__ == "__main__":

    init_system()

    ws_client.set_price_callback(on_price)
    ws_client.start()

    run_trading()
