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
# GLOBAL PRICE STORE
# =====================================================
latest_price = None


# =====================================================
# WS CALLBACK
# =====================================================
def on_price(price):
    global latest_price

    latest_price = price
    update_market_state(price, volume=0)


# =====================================================
# INIT SYSTEM
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
# TRADING LOOP (REAL PnL VERSION)
# =====================================================
def run_trading():

    logger.info("TRADING STARTED")

    global latest_price

    while True:

        try:

            # =========================
            # WS price 없으면 skip
            # =========================
            if latest_price is None:
                time.sleep(0.3)
                continue

            price = latest_price

            # =========================
            # 전략 판단
            # =========================
            decision = brain.decide("auto", price)
            strategy = decision["strategy"]

            # =========================
            # 실행 (실제 order)
            # =========================
            result = execute_strategy(
                signal=strategy,
                price=price,
                symbol=SYMBOL,
                equity=1000
            )

            # =========================
            # REAL PnL 계산 (핵심)
            # =========================
            pnl = engine.calculate_pnl(SYMBOL, price)

            # =========================
            # risk / learning update
            # =========================
            risk_engine.update(pnl)
            brain.record(strategy, pnl)

            # =========================
            # log
            # =========================
            logger.info(
                f"PRICE={price} STRATEGY={strategy} PNL={pnl}"
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

    # WS 시작
    ws_client.set_price_callback(on_price)
    ws_client.start()

    # 트레이딩 시작
    run_trading()
