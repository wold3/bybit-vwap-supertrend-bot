import logging

from api.order_manager import order_manager
from risk.risk_engine import risk_engine
from database.database import SessionLocal
from database.repository import add_trade, add_log

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def __init__(self):
        self.busy = False

    def is_busy(self):
        return self.busy

    # =====================================================
    # EXECUTE (FIXED)
    # =====================================================
    def execute(self, signal, symbol, qty, price, leverage):

        if self.busy:
            return {"success": False, "reason": "busy"}

        self.busy = True
        db = SessionLocal()

        try:

            # -------------------------
            # 1. risk check
            # -------------------------
            if not risk_engine.allow_trade():
                add_log(db, "WARNING", "Trade blocked by risk engine")

                return {
                    "success": False,
                    "reason": "risk_block"
                }

            # -------------------------
            # 2. order
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
            # 3. db trade log
            # -------------------------
            trade = add_trade(
                db=db,
                symbol=symbol,
                side=signal,
                qty=qty,
                price=price,
                leverage=leverage
            )

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


engine = ExecutionEngine()


# =====================================================
# wrapper FIX
# =====================================================
def execute_order(signal, symbol, price, equity, win_rate):

    qty = max(1, int(equity * 0.01))  # 1% risk sizing
    leverage = 1

    return engine.execute(
        signal=signal,
        symbol=symbol,
        qty=qty,
        price=price,
        leverage=leverage,
    )
