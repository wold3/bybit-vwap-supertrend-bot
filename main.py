import time
import logging

from config import SYMBOL
from api.websocket_client import ws_client

from ai.trading_brain import brain
from strategy.strategy_router import update_market_state
from strategy.strategy_wrapper import execute_strategy
from risk.risk_engine import risk_engine
from services.telegram_service import init_telegram, get_telegram
from services.watchdog_service import watchdog

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

latest_price = {"value": None}


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

    latest_price["value"] = price
    update_market_state(price, 0)


# =====================================================
# TRADING LOOP (FIXED)
# =====================================================
def run_trading():

    logger.info("TRADING STARTED")

    equity = 1000

    while True:

        try:

            price = latest_price["value"]

            if price is None:
                time.sleep(0.5)
                continue

            decision = brain.decide("auto", price)

            result = execute_strategy(
                signal="auto",
                price=price,
                symbol=SYMBOL,
                equity=equity
            )

            pnl = (price % 10) - 5

            risk_engine.update(pnl)
            brain.record(decision["strategy"], pnl)

            logger.info(
                f"PRICE={price} STRATEGY={decision['strategy']} PNL={pnl}"
            )

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
