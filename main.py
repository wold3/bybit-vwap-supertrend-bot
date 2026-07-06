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
# GLOBAL PRICE
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
# TRADING LOOP (TP/SL 포함)
# =====================================================
def run_trading():

    logger.info("TRADING STARTED")

    global latest_price

    while True:

        try:

            # =========================
            # 1. WS 가격 체크
            # =========================
            if latest_price is None:
                time.sleep(0.3)
                continue

            price = latest_price

            # =========================
            # 2. TP / SL 체크 (핵심)
            # =========================
            exit_reason = engine.check_exit(SYMBOL, price)

            if exit_reason:
                engine.close_position(SYMBOL, exit_reason, price)

                # risk reset (청산 반영)
                risk_engine.update(0)

                logger.info(f"CLOSE POSITION: {exit_reason} PRICE={price}")

                time.sleep(0.5)
                continue

            # =========================
            # 3. 전략 판단
            # =========================
            decision = brain.decide("auto", price)
            strategy = decision["strategy"]

            # =========================
            # 4. 실행
            # =========================
            execute_strategy(
                signal=strategy,
                price=price,
                symbol=SYMBOL,
                equity=1000
            )

            # =========================
            # 5. REAL PnL 계산
            # =========================
            pnl = engine.calculate_pnl(SYMBOL, price)

            # =========================
            # 6. risk / learning
            # =========================
            risk_engine.update(pnl)
            brain.record(strategy, pnl)

            # =========================
            # 7. log
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

    ws_client.set_price_callback(on_price)
    ws_client.start()

    run_trading()
