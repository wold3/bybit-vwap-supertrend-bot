import time
import logging

from config import SYMBOL

from api.websocket_client import ws_client
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
# 실시간 가격 처리
# =====================================================

def on_price(price):

    volume = 0  # 현재 구조에서는 optional

    update_market_state(price, volume)


# =====================================================
# 트레이딩 루프
# =====================================================

def run_trading():

    logger.info("TRADING STARTED")

    equity = 1000

    while True:

        try:

            price, volume = None, None  # WebSocket 기반이면 callback으로 대체

            # mock price (실전에서는 ws callback 사용)
            import random
            price = 65000 + random.randint(-50, 50)

            update_market_state(price, volume)

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
# ENTRY POINT
# =====================================================

if __name__ == "__main__":

    init_system()

    # WebSocket 시작 (실전 데이터)
    ws_client.set_price_callback(on_price)
    ws_client.start()

    # 트레이딩 루프 시작
    run_trading()
