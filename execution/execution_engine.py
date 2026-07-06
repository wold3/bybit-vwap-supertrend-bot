import logging

from api.bybit_client import bybit_client
from risk.risk_engine import risk_engine
from api.order_manager import order_manager

logger = logging.getLogger(__name__)


class ExecutionEngine:

    def __init__(self):
        self.busy = False

    # =====================================================
    # REAL PnL (핵심 개선)
    # =====================================================
    def get_real_pnl(self, symbol):

        try:

            res = bybit_client.get_positions(symbol)

            items = res.get("result", {}).get("list", [])

            total_pnl = 0.0

            for p in items:

                if p.get("symbol") == symbol:

                    total_pnl += float(p.get("unrealisedPnl", 0))

            return total_pnl

        except Exception as e:
            logger.error(f"PnL ERROR: {e}")
            return 0

    # =====================================================
    # EXIT LOGIC (SL/TP)
    # =====================================================
    def check_exit(self, symbol, price):

        pnl = self.get_real_pnl(symbol)

        if pnl <= -10:
            return "STOP_LOSS"

        if pnl >= 20:
            return "TAKE_PROFIT"

        return None

    # =====================================================
    # CLOSE POSITION
    # =====================================================
    def close_position(self, symbol, reason):

        logger.warning(f"CLOSE {symbol} ({reason})")

        order_manager.place_market_order(
            symbol=symbol,
            side="Sell",
            qty=1
        )

    # =====================================================
    # EXECUTE
    # =====================================================
    def execute(self, signal, symbol, qty, price, leverage=1):

        self.busy = True

        try:

            if not risk_engine.allow_trade():
                return {"success": False, "reason": "risk_block"}

            order_id = order_manager.place_market_order(
                symbol=symbol,
                side=signal,
                qty=qty,
                leverage=leverage
            )

            if not order_id:
                return {"success": False, "reason": "order_failed"}

            risk_engine.add_trade()

            logger.info(f"EXECUTED {symbol} {signal}")

            return {"success": True, "order_id": order_id}

        finally:
            self.busy = False


engine = ExecutionEngine()
