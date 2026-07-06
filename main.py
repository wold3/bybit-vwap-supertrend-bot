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


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =====================================================
# STATE
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
# PnL CALC (REAL)
# =====================================================
def calculate_pnl():

    pnl = 0.0

    for order in order_manager.get_filled_orders().values():

        entry = order.get("entry_price") or 0
        qty = order.get("qty", 1)

        if entry > 0:
            pnl += (last_price["price"] - entry) * qty

    return pnl


# =====================================================
# TRADING LOOP
# =====================================================
def run_trading():

    logger.info("TRADING STARTED")

    equity = 1000

    while True:

        try:

            price = last_price["price"]
            volume = last_price["volume"]

            if price == 0:
                time.sleep(1)
                continue

            # =================================================
            # ORDER SYNC (real price 전달)
            # =================================================
            order_manager.sync_orders(price)

            # =================================================
            # STRATEGY
            # =================================================
            decision = brain.decide("auto", price)

            result = execute_strategy(
                signal="auto",
                price=price,
                symbol=SYMBOL,
                equity=equity
            )

            # =================================================
            # REAL PnL
            # =================================================
            pnl = calculate_pnl()
            risk_engine.update(pnl)

            brain.record(decision["strategy"], pnl)

            logger.info(
                f"PRICE={price} "
                f"STRATEGY={decision['strategy']} "
                f"PNL={pnl:.2f} "
                f"OPEN={len(order_manager.open_orders)} "
                f"FILLED={len(order_manager.filled_orders)}"
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
