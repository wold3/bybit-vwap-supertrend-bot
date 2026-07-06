import logging

from api.order_manager import order_manager
from risk.risk_engine import risk_engine
from database.database import SessionLocal
from database.repository import add_trade, add_log

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def __init__(self):

        self.busy = False

        # 포지션 저장
        self.positions = {}

        # TP / SL 설정
        self.tp_ratio = 0.02   # +2%
        self.sl_ratio = 0.01   # -1%

    # =====================================================
    # PnL 계산
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
    # TP / SL 체크 (핵심 추가)
    # =====================================================
    def check_exit(self, symbol, current_price):

        pos = self.positions.get(symbol)

        if not pos:
            return None

        entry = pos["entry_price"]
        side = pos["side"]

        # 상승 기준
        if side == "Buy":

            tp = entry * (1 + self.tp_ratio)
            sl = entry * (1 - self.sl_ratio)

            if current_price >= tp:
                return "TP"
            if current_price <= sl:
                return "SL"

        # 하락 기준
        else:

            tp = entry * (1 - self.tp_ratio)
            sl = entry * (1 + self.sl_ratio)

            if current_price <= tp:
                return "TP"
            if current_price >= sl:
                return "SL"

        return None

    # =====================================================
    # 포지션 종료
    # =====================================================
    def close_position(self, symbol, reason, price):

        pos = self.positions.get(symbol)

        if not pos:
            return

        pnl = self.calculate_pnl(symbol, price)

        logger.info(f"CLOSE {symbol} reason={reason} pnl={pnl}")

        del self.positions[symbol]

    # =====================================================
    # 실행
    # =====================================================
    def execute(self, signal, symbol, qty, price, leverage):

        self.busy = True
        db = SessionLocal()

        try:

            if not risk_engine.allow_trade():
                add_log(db, "WARNING", "Risk blocked")
                return {"success": False}

            order_id = order_manager.place_market_order(
                symbol=symbol,
                side=signal,
                qty=qty,
                leverage=leverage
            )

            if not order_id:
                return {"success": False}

            # 포지션 생성
            self.positions[symbol] = {
                "side": signal,
                "entry_price": price,
                "qty": qty
            }

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
