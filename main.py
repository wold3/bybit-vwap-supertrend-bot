import time
import logging

from config import SYMBOL
from api.websocket_client import ws_client
from api.order_manager import order_manager

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
last_price = {
    "price": 0,
    "volume": 0
}


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
def on_price(price, volume):

    last_price["price"] = price
    last_price["volume"] = volume

    update_market_state(price, volume)


# =====================================================
# TRADING LOOP
# =====================================================
def run_trading():

    logger.info("TRADING STARTED")

    equity = 1000

    while True:

        try:

            # =================================================
            # 1. PRICE FETCH (WS 기반)
            # =================================================
            price = last_price["price"]
            volume = last_price["volume"]

            if price == 0:
                time.sleep(1)
                continue

            # =================================================
            # 2. ORDER SYNC (핵심)
            # =================================================
            order_manager.sync_orders()

            # =================================================
            # 3. STRATEGY DECISION
            # =================================================
            decision = brain.decide("auto", price)

            # =================================================
            # 4. EXECUTION
            # =================================================
            result = execute_strategy(
                signal="auto",
                price=price,
                symbol=SYMBOL,
                equity=equity
            )

            # =================================================
            # 5. RISK UPDATE (mock pnl)
            # =================================================
            pnl = (price % 10) - 5
            risk_engine.update(pnl)

            brain.record(decision["strategy"], pnl)

            # =================================================
            # 6. LOGGING
            # =================================================
            logger.info(
                f"PRICE={price} "
                f"STRATEGY={decision['strategy']} "
                f"PNL={pnl} "
                f"OPEN_ORDERS={len(order_manager.open_orders)}"
            )

            time.sleep(2)

        except Exception as e:

            logger.error(f"MAIN ERROR: {str(e)}")

            tg = get_telegram()
            if tg:
                tg.error(e)

            time.sleep(5)


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":

    init_system()

    # WebSocket start
    ws_client.set_price_callback(on_price)
    ws_client.start()

    # trading loop
    run_trading()
