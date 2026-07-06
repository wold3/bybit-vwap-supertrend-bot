from api.bybit_client import bybit
from execution.order_lifecycle import lifecycle
from risk.risk_engine import risk

class PositionSync:

    def sync(self, symbol):

        res = bybit.position(symbol)

        pnl = 0.0

        for p in res.get("result", {}).get("list", []):

            pnl += float(p.get("unrealisedPnl", 0))

            if float(p.get("size", 0)) == 0:

                for oid, o in lifecycle.orders.items():
                    if o["symbol"] == symbol:
                        o["status"] = "CLOSED"

        risk.update_pnl(pnl)

        return pnl

position_sync = PositionSync()
