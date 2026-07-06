import logging

from api.order_manager import order_manager
from risk.risk_engine import risk_engine
from database.database import SessionLocal
from database.repository import add_trade, add_log

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def __init__(self):

        self.busy = False

    # =====================================================
    # 상태 체크
    # =====================================================

    def is_busy(self):

        return self.busy

    # =====================================================
    # 메인 실행
    # =====================================================

    def execute(self, signal, symbol, qty, price, leverage):

        self.busy = True

        db = SessionLocal()

        try:

            # -------------------------
            # 1. 리스크 체크
            # -------------------------
            if not risk_engine.allow_trade():
                logger.warning("TRADE BLOCKED by risk engine")

                add_log(db, "WARNING", "Trade blocked by risk engine")

                return {
                    "success": False,
                    "reason": "risk_block"
                }

            # -------------------------
            # 2. 주문 실행
            # -------------------------
            order_id = order_manager.place_market_order(
                symbol=symbol,
                side=signal,
                qty=qty,
                leverage=leverage
            )

            if not order_id:
                add_log(db, "ERROR", "Order failed")

                return {
                    "success": False,
                    "reason": "order_failed"
                }

            # -------------------------
            # 3. DB 저장
            # -------------------------
            trade = add_trade(
                db=db,
                symbol=symbol,
                side=signal,
                qty=qty,
                price=price,
                leverage=leverage
            )

            # -------------------------
            # 4. 상태 기록
            # -------------------------
            add_log(db, "INFO", f"Trade executed {symbol} {signal}")

            logger.info(f"EXECUTED: {symbol} {signal} qty={qty}")

            return {
                "success": True,
                "order_id": order_id,
                "trade_id": trade.id
            }

        except Exception as e:

            logger.error(f"Execution error: {str(e)}")

            add_log(db, "ERROR", str(e))

            return {
                "success": False,
                "reason": "exception",
                "error": str(e)
            }

        finally:
            db.close()
            self.busy = False


# =====================================================
# SINGLETON
# =====================================================

engine = ExecutionEngine()

# =====================================================
# SINGLETON
# =====================================================

engine = ExecutionEngine()


# =====================================================
# Compatibility Wrapper
# =====================================================

def execute_order(signal, symbol, price, equity, win_rate):
    """
    strategy_wrapper.py에서 호출하는 호환 함수

    현재 ExecutionEngine.execute()는
    qty와 leverage를 요구하므로 기본값을 사용한다.
    """

    qty = 1
    leverage = 1

    return engine.execute(
        signal=signal,
        symbol=symbol,
        qty=qty,
        price=price,
        leverage=leverage,
    )
