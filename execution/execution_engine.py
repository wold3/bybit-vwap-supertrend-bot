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
    # EXECUTE
    # =====================================================
    def execute(self, signal, symbol, qty, price, leverage):

        self.busy = True
        db = SessionLocal()

        try:

            # risk check
            if not risk_engine.allow_trade():
                add_log(db, "WARNING", "blocked by risk engine")
                return {"success": False, "reason": "risk_block"}

            # order
            order_id = order_manager.place_market_order(
                symbol=symbol,
                side=signal,
                qty=qty,
                leverage=leverage
            )

            if not order_id:
                add_log(db, "ERROR", "order failed")
                return {"success": False, "reason": "order_failed"}

            # db save
            trade = add_trade(
                db=db,
                symbol=symbol,
                side=signal,
                qty=qty,
                price=price,
                leverage=leverage
            )

            add_log(db, "INFO", f"executed {symbol} {signal}")

            return {
                "success": True,
                "order_id": order_id,
                "trade_id": trade.id
            }

        except Exception as e:
            logger.error(f"Execution error: {str(e)}")
            add_log(db, "ERROR", str(e))

            return {"success": False, "reason": "exception"}

        finally:
            db.close()
            self.busy = False


engine = ExecutionEngine()


def execute_order(signal, symbol, price, equity, win_rate):

    return engine.execute(
        signal=signal,
        symbol=symbol,
        qty=1,
        price=price,
        leverage=1
    )
