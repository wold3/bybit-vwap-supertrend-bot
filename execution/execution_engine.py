import logging

from risk.risk_engine import risk_engine
from api.order_manager import order_manager

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def __init__(self):
        self.busy = False

    # =====================================================
    # 상태 확인
    # =====================================================
    def is_busy(self):
        return self.busy

    # =====================================================
    # 메인 실행 (핵심)
    # =====================================================
    def execute(self, signal, symbol, qty, price, leverage=1):

        self.busy = True

        try:

            # =================================================
            # 1) RISK CHECK (킬스위치)
            # =================================================
            if not risk_engine.allow_trade():
                logger.warning("🚨 TRADE BLOCKED (RISK)")
                return {
                    "success": False,
                    "reason": "risk_block"
                }

            # =================================================
            # 2) ORDER EXECUTION
            # =================================================
            order_id = order_manager.place_market_order(
                symbol=symbol,
                side=signal,
                qty=qty,
                leverage=leverage
            )

            if not order_id:
                logger.error("❌ ORDER FAILED")
                return {
                    "success": False,
                    "reason": "order_failed"
                }

            # =================================================
            # 3) RISK UPDATE (거래 카운트)
            # =================================================
            risk_engine.add_trade()

            # =================================================
            # 4) LOG
            # =================================================
            logger.info(
                f"EXECUTED → {symbol} {signal} qty={qty} order_id={order_id}"
            )

            return {
                "success": True,
                "order_id": order_id
            }

        except Exception as e:

            logger.error(f"EXECUTION ERROR: {str(e)}")

            return {
                "success": False,
                "reason": "exception",
                "error": str(e)
            }

        finally:
            self.busy = False


# =====================================================
# SINGLETON
# =====================================================
engine = ExecutionEngine()
