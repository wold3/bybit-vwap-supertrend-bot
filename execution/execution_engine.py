from portfolio.position_manager import position_manager
from risk.risk_engine import risk_engine


class ExecutionEngine:

    def __init__(self):
        self.busy = False

    def execute(self, signal, symbol, qty, price, leverage):

        self.busy = True

        try:

            # -------------------------
            # risk check
            # -------------------------
            if not risk_engine.allow_trade():
                return {"success": False, "reason": "risk_block"}

            # -------------------------
            # position open (REAL FIX)
            # -------------------------
            position_manager.open_position(
                symbol=symbol,
                side=signal,
                qty=qty,
                price=price
            )

            return {
                "success": True,
                "symbol": symbol,
                "side": signal,
                "qty": qty
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }

        finally:
            self.busy = False


engine = ExecutionEngine()
