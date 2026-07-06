import time
import logging

from services.telegram_service import init_telegram, get_telegram
from services.watchdog_service import watchdog

from ai.trading_brain import brain

from strategy.strategy_router import update_market_state
from strategy.strategy_wrapper import execute_strategy

from risk.risk_engine import risk_engine
from execution.execution_engine import execute_order


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


# =====================================================
# CONFIG
# =====================================================

SYMBOL = "BTCUSDT"


# =====================================================
# 초기화
# =====================================================

def init_system():

    logger.info("Initializing system...")

    init_telegram(
        token="YOUR_TELEGRAM_TOKEN",
        chat_id="YOUR_CHAT_ID"
    )

    watchdog.start()

    logger.info("System initialized")


# =====================================================
# 시장 데이터 mock (실전에서는 WebSocket 교체)
# =====================================================

def get_market_data():

    # TODO: Bybit WebSocket 연결로 교체
    import random

    price = 65000 + random.randint(-100, 100)
    volume = random.randint(100, 1000)

    return price, volume


# =====================================================
# 트레이딩 루프
# =====================================================

def run_trading():

    logger.info("Trading started")

    equity = 1000

    while True:

        try:

            price, volume = get_market_data()

            update_market_state(price, volume)

            decision = brain.decide(signal="auto", price=price)

            result = execute_strategy(
                signal="auto",
                price=price,
                symbol=SYMBOL,
                equity=equity
            )

            # mock pnl update (실거래에서는 체결 기준으로 변경)
            pnl = (price % 10) - 5

            risk_engine.update(pnl, price, 1)

            # brain learning
            brain.record(decision["strategy"], pnl)

            logger.info(
                f"PRICE={price} STRATEGY={decision['strategy']} PNL={pnl}"
            )

            time.sleep(2)

        except Exception as e:

            logger.error(f"MAIN LOOP ERROR: {str(e)}")

            tg = get_telegram()
            if tg:
                tg.error(e)

            time.sleep(5)


# =====================================================
# ENTRY
# =====================================================

if __name__ == "__main__":

    init_system()
    run_trading()
