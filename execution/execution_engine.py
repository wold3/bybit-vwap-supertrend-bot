import logging
from threading import Lock

from api.order_manager import order_manager
from risk.risk_engine import risk_engine
from database.database import SessionLocal
from database.repository import add_trade, add_log

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def __init__(self):
        self.busy = False
        self.lock = Lock()

    # =====================================================
    # 상태 체크
    # =====================================================
    def is_busy(self):
        return self.busy

    # =====================================================
    # 메인 실행
    # =====================================================
    def execute(self, signal, symbol, qty, price, leverage):

        with self.lock:
            if self.busy:
                logger.warning("Execution skipped (busy)")
                return {"success": False, "reason": "busy"}

            self.busy = True

        db = SessionLocal()

        try:

            # -------------------------
            # 1. risk check
            # -------------------------
            if not risk_engine.allow_trade():
                logger.warning("TRADE BLOCKED by risk engine")
                add_log(db, "WARNING", "Trade blocked by risk engine")

                return {
                    "success": False,
                    "reason": "risk_block"
                }

            # -------------------------
            # 2. order execution
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
            # 3. trade DB
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
            # 4. REALISTIC PNL INIT
            # -------------------------
            risk_engine.update(0)  # init hook

            add_log(db, "INFO", f"Trade executed {symbol} {signal}")

            logger.info(f"EXECUTED: {symbol} {signal} qty={qty}")

            return {
                "success": True,
                "order_id": order_id,
                "trade_id": getattr(trade, "id", None)
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
# WRAPPER (strategy compatibility)
# =====================================================
def execute_order(signal, symbol, price, equity, win_rate):

    qty = 1
    leverage = 1

    return engine.execute(
        signal=signal,
        symbol=symbol,
        qty=qty,
        price=price,
        leverage=leverage
    )
