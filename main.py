import time
import threading

from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL,
    BYBIT_BASE_URL,
)

from market.websocket_client import ws_client
from services.private_ws_client import private_ws_client

from portfolio.bybit_wallet import wallet
from execution.order_manager import order_manager

from strategy.strategy_engine import strategy_engine
from risk.risk_manager import risk_manager

from watchdog.watchdog import watchdog
from core.bot_guard import bot_guard

from utils.logger import (
    bot_logger,
    error_logger,
)


# ==========================================================
# HEARTBEAT
# ==========================================================

def heartbeat_loop():

    while bot_guard.is_running():

        try:

            bot_guard.heartbeat()

        except Exception as e:

            print("[HEARTBEAT ERROR]", e)
            error_logger.error(str(e))

        time.sleep(60)


# ==========================================================
# STRATEGY LOOP
# ==========================================================

def strategy_loop():

    print("[START] STRATEGY LOOP")

    while bot_guard.is_running():

        try:

            # 일일 손실 제한
            if not risk_manager.check_daily_loss():

                print("[STRATEGY STOP] DAILY LOSS LIMIT")

                bot_logger.warning("Daily loss limit reached")

                bot_guard.stop()

                break

            # 전략 엔진이 내부적으로 WS 데이터를 사용
            time.sleep(1)

        except Exception as e:

            print("[STRATEGY LOOP ERROR]", e)

            error_logger.error(str(e))

            time.sleep(3)


# ==========================================================
# START
# ==========================================================

def start_bot():

    print("====================================")
    print("VWAP SUPERTREND BOT START")
    print("LIVE :", LIVE_TRADING)
    print("SYMBOL :", DEFAULT_SYMBOL)
    print("BASE :", BYBIT_BASE_URL)
    print("====================================")

    bot_logger.info("BOT START")

    # -----------------------------
    # WATCHDOG
    # -----------------------------
    watchdog.start()

    # -----------------------------
    # WALLET
    # -----------------------------
    equity = wallet.get_equity()

    print("[ACCOUNT EQUITY]", equity)

    bot_logger.info(f"ACCOUNT EQUITY : {equity}")

    # -----------------------------
    # RISK INIT
    # -----------------------------
    risk_manager.initialize()

    # -----------------------------
    # PUBLIC WS
    # -----------------------------
    public_thread = threading.Thread(
        target=ws_client.start,
        daemon=True,
    )
    public_thread.start()

    # -----------------------------
    # PRIVATE WS
    # -----------------------------
    private_thread = threading.Thread(
        target=private_ws_client.start,
        daemon=True,
    )
    private_thread.start()

    # -----------------------------
    # STRATEGY
    # -----------------------------
    strategy_thread = threading.Thread(
        target=strategy_loop,
        daemon=True,
    )
    strategy_thread.start()

    # -----------------------------
    # HEARTBEAT
    # -----------------------------
    heartbeat_thread = threading.Thread(
        target=heartbeat_loop,
        daemon=True,
    )
    heartbeat_thread.start()

    print("[BOT RUNNING]")

    bot_logger.info("BOT RUNNING")


# ==========================================================
# STOP
# ==========================================================

def stop_bot():

    print("\n[BOT STOPPING]")

    bot_logger.info("BOT STOPPING")

    bot_guard.stop()

    try:
        ws_client.stop()
    except Exception as e:
        error_logger.error(str(e))

    try:
        private_ws_client.stop()
    except Exception as e:
        error_logger.error(str(e))

    try:
        watchdog.stop()
    except Exception as e:
        error_logger.error(str(e))

    print("[BOT STOPPED]")

    bot_logger.info("BOT STOPPED")


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    try:

        start_bot()

        while bot_guard.is_running():
            time.sleep(1)

    except KeyboardInterrupt:

        stop_bot()

    except Exception as e:

        print("[MAIN ERROR]", e)

        error_logger.exception(str(e))

        stop_bot()
