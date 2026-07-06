from api.bybit_client import bybit_client


class PnLEngine:

    def get_position_pnl(self, symbol):

        try:

            res = bybit_client.get_positions(symbol)

            items = res.get("result", {}).get("list", [])

            total_pnl = 0.0
            total_size = 0.0

            for p in items:

                if p.get("symbol") != symbol:
                    continue

                pnl = float(p.get("unrealisedPnl", 0))
                size = float(p.get("size", 0))

                total_pnl += pnl
                total_size += size

            return {
                "pnl": total_pnl,
                "size": total_size
            }

        except Exception:
            return {
                "pnl": 0,
                "size": 0
            }


pnl_engine = PnLEngine()
