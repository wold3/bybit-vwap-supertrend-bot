import logging
from utils.telegram import telegram


class Monitor:

    def __init__(self):

        self.last_pnl = 0

    # ================================
    # TRADE EVENT
    # ================================
    def on_trade(self, symbol, side, price, pnl):

        msg = f"""
📊 TRADE EXECUTED
Symbol: {symbol}
Side: {side}
Price: {price}
PnL: {pnl}
        """

        telegram.send(msg)

    # ================================
    # PNL UPDATE
    # ================================
    def on_pnl(self, pnl):

        # 큰 변화만 알림
        if abs(pnl - self.last_pnl) > 10:

            telegram.send(f"📈 PnL UPDATE: {pnl}")

            self.last_pnl = pnl

    # ================================
    # ERROR ALERT
    # ================================
    def on_error(self, error):

        telegram.send(f"🚨 ERROR: {error}")


monitor = Monitor()
