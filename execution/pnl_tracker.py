from storage.trade_db import trade_db


class PnLTracker:

    def record_trade(self, symbol, side, qty, price, pnl):

        trade_db.save(symbol, side, qty, price, pnl)

    def total_pnl(self):

        rows = trade_db.all()

        return sum(row[5] for row in rows)


pnl_tracker = PnLTracker()
