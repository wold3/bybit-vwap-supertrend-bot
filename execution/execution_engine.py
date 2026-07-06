import logging

from api.order_manager import order_manager
from api.bybit_client import bybit_client
from risk.risk_engine import risk_engine
from database.database import SessionLocal
from database.repository import add_trade, add_log

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def __init__(self):

        self.busy = False

        # 심플 캐시
        self.positions = {}

        self.tp_ratio = 0.02
        self.sl_ratio = 0.01

    # =====================================================
    # POSITION SYNC
    # =====================================================
    def sync_positions(self, symbol):

        try:
            resp = bybit_client._request(
                "GET",
                "/v5/position/list",
                {
                    "category": "linear",
                    "symbol": symbol
                }
            )

            data = resp.get("result", {}).get("list", [])

            if not data:
                self.positions.pop(symbol, None)
                return

            p = data[0]

            size = float(p.get("size", 0))
            if size == 0:
                self.positions.pop(symbol, None)
                return

            self.positions[symbol] = {
                "side": p.get("side"),
                "entry": float(p.get("avgPrice", 0)),
                "qty": size
            }

        except Exception as e:
            logger.error(f"SYNC ERROR: {str(e)}")

    # =====================================================
    # EXIT CHECK
    # =====================================================
    def check_exit(self, symbol, price):

        pos = self.positions.get(symbol)

        if not pos:
            return None

        entry = pos["entry"]
        side = pos["side"]

        if side == "Buy":

            if price >= entry * (1 + self.tp_ratio):
                return "TP"

            if price <= entry * (1 - self.sl_ratio):
                return "SL"

        else:

            if price <= entry * (1 + self.tp_ratio):
                return "TP"

            if price >= entry * (1 - self.sl_ratio):
                return "SL"

        return None

    # =====================================================
    # 🔥 REAL CLOSE ORDER (핵심)
    # =====================================================
    def close_position(self, symbol, reason):

        try:

            pos = self.positions.get(symbol)

            if not pos:
                return False

            side = pos["side"]

            close_side = "Sell" if side == "Buy" else "Buy"

            qty = pos["qty"]

            resp = order_manager.place_market_order(
                symbol=symbol,
                side=close_side,
                qty=qty,
                leverage=1
            )

            logger.info(f"CLOSE ORDER SENT {symbol} reason={reason}")

            self.positions.pop(symbol, None)

            return True

        except Exception as e:
            logger.error(f"CLOSE ERROR: {str(e)}")
            return False

    # =====================================================
    # EXECUTION
    # =====================================================
    def execute(self, signal, symbol, qty, price, leverage):

        self.busy = True
        db = SessionLocal()

        try:

            order_id = order_manager.place_market_order(
                symbol=symbol,
                side=signal,
                qty=qty,
                leverage=leverage
            )

            if not order_id:
                return {"success": False}

            add_trade(
                db=db,
                symbol=symbol,
                side=signal,
                qty=qty,
                price=price,
                leverage=leverage
            )

            add_log(db, "INFO", f"OPEN {symbol} {signal}")

            return {"success": True, "order_id": order_id}

        except Exception as e:
            add_log(db, "ERROR", str(e))
            return {"success": False}

        finally:
            db.close()
            self.busy = False


engine = ExecutionEngine()
