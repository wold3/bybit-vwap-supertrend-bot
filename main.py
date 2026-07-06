import time
import logging

from config import SYMBOL
from api.websocket_client import ws_client

from ai.trading_brain import brain
from strategy.strategy_router import update_market_state
from strategy.strategy_wrapper import execute_strategy
from risk.risk_engine import risk_engine
from market.candle_builder import candle_builder

from services.telegram_service import init_telegram, get_telegram
from services.watchdog_service import watchdog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

latest_price = {"value": None, "ts": 0}


def init_system():

    logger.info("SYSTEM INIT START")

    init_telegram("YOUR_TOKEN", "YOUR_CHAT_ID")

    watchdog.start()

    logger.info("SYSTEM READY")


def on_price(price):

    latest_price["value"] = price
    latest_price["ts"] = time.time()

    candle_builder.update(price)

    update_market_state(price, 0)


def run_trading():

    logger.info("TRADING STARTED")

    equity = 1000

    while True:

        try:

            price = latest_price["value"]
            ts = latest_price["ts"]

            if price is None or time.time() - ts > 5:
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

            logger.info(f"PRICE={price} STRATEGY={decision['strategy']} PNL={pnl}")

            time.sleep(2)

        except Exception as e:
            logger.error(f"MAIN ERROR: {e}")
            time.sleep(5)


if __name__ == "__main__":

    init_system()

    ws_client.set_price_callback(on_price)
    ws_client.start()

    run_trading()
