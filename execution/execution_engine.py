import logging

from api.order_manager import order_manager
from risk.risk_engine import risk_engine
from database.database import SessionLocal
from database.repository import add_trade, add_log

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def __init__(self):
        self.busy = False
        self.positions = {}   # ✅ 포지션 저장 추가

    def is_busy(self):
        return self.busy

    # =====================================================
    # 포지션 PnL 계산 (핵심 추가)
    # =====================================================
    def calculate_pnl(self, symbol, current_price):

        pos = self.positions.get(symbol)

        if not pos:
            return 0

        entry = pos["entry_price"]
        qty = pos["qty"]

        if pos["side"] == "Buy":
            return (current_price - entry) * qty
        else:
            return (entry - current_price) * qty

    # =====================================================
    # 실행
    # =====================================================
    def execute(self, signal, symbol, qty, price, leverage):

        self.busy = True
        db = SessionLocal()

        try:

            if not risk_engine.allow_trade():
                add_log(db, "WARNING", "Risk blocked")
                return {"success": False, "reason": "risk_block"}

            # =========================
            # ORDER
            # =========================
            order_id = order_manager.place_market_order(
                symbol=symbol,
                side=signal,
                qty=qty,
                leverage=leverage
            )

            if not order_id:
                add_log(db, "ERROR", "Order failed")
                return {"success": False, "reason": "order_failed"}

            # =========================
            # POSITION 저장 (핵심)
            # =========================
            self.positions[symbol] = {
                "side": signal,
                "entry_price": price,
                "qty": qty
            }

            trade = add_trade(
                db=db,
                symbol=symbol,
                side=signal,
                qty=qty,
                price=price,
                leverage=leverage
            )

            add_log(db, "INFO", f"Trade executed {symbol} {signal}")

            logger.info(f"EXECUTED: {symbol} {signal}")

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
