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

# =========================
# 추가 (포지션 sync)
# =========================
from portfolio.sync_engine import sync_engine
from portfolio.position_manager import position_manager


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
# WebSocket callback
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
# 트레이딩 루프 (SYNC 포함 핵심 수정)
# =====================================================
def run_trading():

    logger.info("TRADING STARTED")

    equity = 1000

    while True:

        try:

            # =================================================
            # 12) BYBIT POSITION SYNC (핵심 추가)
            # =================================================
            sync_engine.sync(SYMBOL)

            price = latest_price["price"]

            # WS 아직 안 들어왔을 때 방어
            if price is None:
                time.sleep(0.5)
                continue

            volume = latest_price["volume"]

            # 전략 판단
            decision = brain.decide("auto", price)

            # 실행
            result = execute_strategy(
                signal="auto",
                price=price,
                symbol=SYMBOL,
                equity=equity
            )

            # PnL (real position 기반)
            pnl = position_manager.update_pnl(price)
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

    ws_client.set_price_callback(on_price)
    ws_client.start()

    run_trading()
