from utils.telegram import telegram

class Monitor:

    def on_trade(self, symbol, side, price, pnl):
        telegram.send(f"TRADE {symbol} {side} {price} PnL={pnl}")

    def on_pnl(self, pnl):
        telegram.send(f"PnL UPDATE: {pnl}")

monitor = Monitor()
