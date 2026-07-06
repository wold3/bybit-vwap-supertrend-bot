class StrategyEngine:

    def __init__(self, execution_engine):

        self.execution = execution_engine

        self.tp1_hit = {}
        self.be_moved = {}

    # =================================================
    # SIGNAL ENTRY
    # =================================================
    def on_signal(self, symbol, side, price, qty):

        self.execution.execute(symbol, side, qty)

        self.tp1_hit[symbol] = False
        self.be_moved[symbol] = False

    # =================================================
    # PRICE UPDATE LOOP
    # =================================================
    def on_price(self, symbol, price, position):

        if not position:
            return

        entry = position["entry_price"]
        side = position["side"]

        pnl_pct = self._calc_pnl(entry, price, side)

        # ============================
        # TP1 (부분 익절)
        # ============================
        if pnl_pct >= 0.5 and not self.tp1_hit.get(symbol):

            self.tp1_hit[symbol] = True

            self.execution.partial_close(symbol, 0.5)

        # ============================
        # BREAKEVEN MOVE
        # ============================
        if pnl_pct >= 0.3 and not self.be_moved.get(symbol):

            self.be_moved[symbol] = True

            self.execution.move_sl_to_be(symbol)

        # ============================
        # FINAL TP / TRAILING EXIT
        # ============================
        if pnl_pct >= 1.0:

            self.execution.close_position(symbol)

        # ============================
        # STOP LOSS
        # ============================
        if pnl_pct <= -0.5:

            self.execution.close_position(symbol)

    # =================================================
    # PNL CALC
    # =================================================
    def _calc_pnl(self, entry, price, side):

        if side == "Buy":
            return (price - entry) / entry * 100
        else:
            return (entry - price) / entry * 100
