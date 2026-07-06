import logging

from api.order_manager import order_manager
from risk.risk_engine import risk_engine
from database.database import SessionLocal
from database.repository import add_trade, add_log

from api.bybit_client import bybit_client   # ✅ 추가

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def __init__(self):
        self.busy = False

    def is_busy(self):
        return self.busy

    # =====================================================
    # 🔥 REAL PnL FETCH
    # =====================================================
    def get_real_pnl(self, symbol):

        try:
            resp = bybit_client._request(
                "GET",
                "/v5/position/list",
                {
                    "category": "linear",
                    "symbol": symbol
                }
            )

            positions = resp.get("result", {}).get("list", [])

            if not positions:
                return 0.0

            pos = positions[0]

            pnl = float(pos.get("unrealisedPnl", 0))
            return pnl

        except Exception as e:
            logger.error(f"PnL fetch error: {str(e)}")
            return 0.0

    # =====================================================
    # MAIN EXECUTION
    # =====================================================
    def execute(self, signal, symbol, qty, price, leverage):

        self.busy = True
        db = SessionLocal()

        try:

            # -------------------------
            # 1. risk check
            # -------------------------
            if not risk_engine.allow_trade():
                logger.warning("TRADE BLOCKED")

                add_log(db, "WARNING", "Trade blocked by risk engine")

                return {"success": False, "reason": "risk_block"}

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
                return {"success": False, "reason": "order_failed"}

            # -------------------------
            # 3. DB save
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

            logger.info(f"EXECUTED: {symbol} {signal}")

            # -------------------------
            # 4. 🔥 REAL PnL update
            # -------------------------
            pnl = self.get_real_pnl(symbol)

            risk_engine.update(pnl)

            logger.info(f"REAL PnL={pnl}")

            return {
                "success": True,
                "order_id": order_id,
                "trade_id": trade.id,
                "pnl": pnl
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
