import time
import logging
import threading
from datetime import datetime

from execution.execution_engine import engine
from risk.risk_engine import risk_engine
from services.telegram_service import get_telegram

logger = logging.getLogger(__name__)


class WatchdogService:

    def __init__(self):

        self.running = False
        self.last_heartbeat = datetime.utcnow()
        self.interval = 10  # 10초 체크

    # =====================================================
    # 시스템 상태 체크
    # =====================================================

    def check_system(self):

        status = risk_engine.status()

        # 1. 위험 상태 체크
        if status["risk_score"] < 20:
            logger.warning("CRITICAL RISK STATE")

            tg = get_telegram()
            if tg:
                tg.risk_update()

        # 2. 드로우다운 체크
        if status["drawdown"] > 0.15:
            logger.warning("DRAWDOWN ALERT")

            tg = get_telegram()
            if tg:
                tg.drawdown_alert()

        # 3. 엔진 상태 체크
        if engine.is_busy():
            logger.warning("Execution engine busy")

        return True

    # =====================================================
    # heartbeat 업데이트
    # =====================================================

    def heartbeat(self):

        self.last_heartbeat = datetime.utcnow()

        tg = get_telegram()
        if tg:
            tg.heartbeat()

    # =====================================================
    # 메인 루프
    # =====================================================

    def run(self):

        self.running = True

        logger.info("Watchdog started")

        while self.running:

            try:

                self.check_system()

                # 1분마다 heartbeat
                if (datetime.utcnow() - self.last_heartbeat).seconds > 60:
                    self.heartbeat()

                time.sleep(self.interval)

            except Exception as e:

                logger.error(f"Watchdog error: {str(e)}")

                tg = get_telegram()
                if tg:
                    tg.error(e)

                time.sleep(5)

    # =====================================================
    # start / stop
    # =====================================================

    def start(self):

        thread = threading.Thread(
            target=self.run,
            daemon=True
        )

        thread.start()

        logger.info("Watchdog thread started")

    def stop(self):

        self.running = False

        logger.info("Watchdog stopped")


# =====================================================
# Singleton
# =====================================================

watchdog = WatchdogService()
