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
# 공유 최신 가격 저장소
# =====================================================
latest_price = {
    "price": None,
    "volume": 0
}


# =====================================================
# WS callback
# =====================================================
def on_price(price, volume):

    latest_price["price"] = price
    latest_price["volume"] = volume

    update_market_state(price, volume)


# =====================================================
# 초기화
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
# 트레이딩 루프 (REAL WS 기반)
# =====================================================
def run_trading():

    logger.info("TRADING STARTED")

    equity = 1000

    while True:

        try:

            price = latest_price["price"]

            # -------------------------
            # WS 아직 안 들어왔을 때 방어
            # -------------------------
            if price is None:
                time.sleep(0.5)
                continue

            volume = latest_price["volume"]

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
