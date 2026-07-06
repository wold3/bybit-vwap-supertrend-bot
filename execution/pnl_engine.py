from api.bybit_client import bybit


class PnLEngine:

    def get(self, symbol):

        res = bybit.position(symbol)

        pnl = 0

        for p in res.get("result", {}).get("list", []):
            pnl += float(p.get("unrealisedPnl", 0))

        return pnl


pnl_engine = PnLEngine()
