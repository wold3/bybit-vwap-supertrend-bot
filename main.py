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

# =====================================================
# GLOBAL PRICE STATE
# =====================================================
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

    try:
        if price is None:
            return

        latest_price = price
        update_market_state(price, 0)

    except Exception as e:
        logger.error(f"on_price error: {e}")


# =====================================================
# TRADING LOOP
# =====================================================
def run_trading():

    global latest_price

    logger.info("TRADING STARTED")

    equity = 1000

    while True:

        try:

            # 🚨 WAIT FOR REAL DATA
            if latest_price is None:
                time.sleep(0.5)
                continue

            price = latest_price

            update_market_state(price, 0)

            # =========================
            # STRATEGY
            # =========================
            decision = brain.decide("auto", price)
            signal = decision["strategy"]

            # =========================
            # EXECUTION
            # =========================
            execute_strategy(
                signal=signal,
                price=price,
                symbol=SYMBOL,
                equity=equity
            )

            # =========================
            # RISK
            # =========================
            pnl = (price % 10) - 5
            risk_engine.update(pnl)

            brain.record(signal, pnl)

            logger.info(f"PRICE={price} STRATEGY={signal} PNL={pnl}")

            time.sleep(1)

        except Exception as e:

            logger.error(f"MAIN ERROR: {e}")

            tg = get_telegram()
            if tg:
                tg.error(e)

            time.sleep(5)


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":

    init_system()

    ws_client.set_price_callback(on_price)
    ws_client.start()

    run_trading()
