import time
import logging

from config import SYMBOL
from api.websocket_client import ws_client

from ai.trading_brain import brain
from strategy.strategy_router import update_market_state
from strategy.strategy_wrapper import execute_strategy

from risk.risk_engine import risk_engine
from services.watchdog_service import watchdog
from services.telegram_service import init_telegram, get_telegram


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


latest_price = None


# =========================
# WS callback
# =========================
def on_price(price, volume):
    global latest_price
    latest_price = price
    update_market_state(price, volume)


# =========================
# init
# =========================
def init_system():

    logger.info("SYSTEM INIT START")

    init_telegram(
        token="YOUR_TELEGRAM_TOKEN",
        chat_id="YOUR_CHAT_ID"
    )

    watchdog.start()

    logger.info("SYSTEM READY")


# =========================
# trading loop (FIXED)
# =========================
def run_trading():

    logger.info("TRADING STARTED")

    equity = 1000

    global latest_price

    while True:

        try:

            # ❗ WS price 없으면 skip (중요)
            if latest_price is None:
                time.sleep(0.5)
                continue

            price = latest_price

            decision = brain.decide("auto", price)

            result = execute_strategy(
                signal=decision["strategy"],
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

            time.sleep(1)

        except Exception as e:
            logger.error(f"MAIN ERROR: {str(e)}")

            tg = get_telegram()
            if tg:
                tg.error(e)

            time.sleep(3)


# =========================
# ENTRY
# =========================
if __name__ == "__main__":

    init_system()

    ws_client.set_price_callback(on_price)
    ws_client.start()

    run_trading()
