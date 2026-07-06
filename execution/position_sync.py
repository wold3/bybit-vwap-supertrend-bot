import logging
from api.bybit_client import bybit
from execution.order_lifecycle import lifecycle
from risk.risk_engine import risk

logger = logging.getLogger(__name__)


class PositionSync:

    def sync(self, symbol):

        try:

            res = bybit.position(symbol)

            positions = res.get("result", {}).get("list", [])

            total_pnl = 0.0

            for p in positions:

                if p.get("symbol") != symbol:
                    continue

                size = float(p.get("size", 0))
                pnl = float(p.get("unrealisedPnl", 0))

                total_pnl += pnl

                # =========================
                # order 상태 보정
                # =========================
                if size == 0:

                    for oid, o in lifecycle.orders.items():

                        if o["symbol"] == symbol:
                            o["status"] = "CLOSED"

            risk.update_pnl(total_pnl)

            return total_pnl

        except Exception as e:
            logger.error(f"SYNC ERROR: {e}")
            return 0.0


position_sync = PositionSync()
