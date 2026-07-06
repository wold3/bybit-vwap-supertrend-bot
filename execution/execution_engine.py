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

        # 내부 포지션 캐시
        self.positions = {}

        self.tp_ratio = 0.02
        self.sl_ratio = 0.01

    # =====================================================
    # 🔥 REAL POSITION SYNC (핵심)
    # =====================================================
    def sync_positions(self, symbol):

        try:
            resp = bybit_client.get_position(symbol)

            data = resp.get("result", {}).get("list", [])

            new_positions = {}

            for p in data:

                size = float(p.get("size", 0))

                if size == 0:
                    continue

                side = p.get("side")
                avg_price = float(p.get("avgPrice", 0))

                new_positions[symbol] = {
                    "side": side,
                    "entry_price": avg_price,
                    "qty": size
                }

            self.positions = new_positions

        except Exception as e:
            logger.error(f"SYNC ERROR: {str(e)}")

    # =====================================================
    # PnL 계산
    # =====================================================
    def calculate_pnl(self, symbol, price):

        pos = self.positions.get(symbol)

        if not pos:
            return 0

        entry = pos["entry_price"]
        qty = pos["qty"]

        if pos["side"] == "Buy":
            return (price - entry) * qty
        else:
            return (entry - price) * qty

    # =====================================================
    # TP / SL
    # =====================================================
    def check_exit(self, symbol, price):

        pos = self.positions.get(symbol)

        if not pos:
            return None

        entry = pos["entry_price"]
        side = pos["side"]

        if side == "Buy":

            if price >= entry * (1 + self.tp_ratio):
                return "TP"

            if price <= entry * (1 - self.sl_ratio):
                return "SL"

        else:

            if price <= entry * (1 - self.tp_ratio):
                return "TP"

            if price >= entry * (1 + self.sl_ratio):
                return "SL"

        return None

    # =====================================================
    # CLOSE
    # =====================================================
    def close_position(self, symbol, reason, price):

        logger.info(f"CLOSE {symbol} reason={reason} price={price}")

        if symbol in self.positions:
            del self.positions[symbol]

    # =====================================================
    # EXECUTE
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
            logger.error(str(e))
            return {"success": False}

        finally:
            db.close()
            self.busy = False


engine = ExecutionEngine()
