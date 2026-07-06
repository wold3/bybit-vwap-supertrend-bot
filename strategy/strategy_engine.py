from ml_filter import ml_filter


class StrategyEngine:

    def __init__(self, execution_engine):

        self.execution = execution_engine

        self.tp1_hit = {}
        self.be_moved = {}

    # =================================================
    # SIGNAL ENTRY (WITH ML FILTER)
    # =================================================
    def on_signal(self, symbol, side, price, qty, market_data=None):

        # ============================================
        # 1. ML FILTER GATE
        # ============================================
        if market_data:

            allow = ml_filter.allow_trade(market_data)

            if not allow:

                print(f"[STRATEGY] BLOCKED BY ML FILTER: {symbol}")

                return

        # ============================================
        # 2. EXECUTE TRADE
        # ============================================
        self.execution.execute(symbol, side, qty)

        # 상태 초기화
        self.tp1_hit[symbol] = False
        self.be_moved[symbol] = False

    # =================================================
    # PRICE UPDATE LOOP (SL / TP MANAGEMENT)
    # =================================================
    def on_price(self, symbol, price, position):

        if not position:
            return

        entry = position["entry_price"]
        side = position["side"]

        pnl_pct = self._calc_pnl(entry, price, side)

        # ============================================
        # TP1 (부분 익절)
        # ============================================
        if pnl_pct >= 0.5 and not self.tp1_hit.get(symbol):

            print(f"[TP1 HIT] {symbol}")

            self.tp1_hit[symbol] = True

            self.execution.partial_close(symbol, 0.5)

        # ============================================
        # BREAKEVEN MOVE
        # ============================================
        if pnl_pct >= 0.3 and not self.be_moved.get(symbol):

            print(f"[MOVE SL TO BE] {symbol}")

            self.be_moved[symbol] = True

            self.execution.move_sl_to_be(symbol)

        # ============================================
        # FINAL TAKE PROFIT
        # ============================================
        if pnl_pct >= 1.0:

            print(f"[FINAL TP] {symbol}")

            self.execution.close_position(symbol)

        # ============================================
        # STOP LOSS
        # ============================================
        if pnl_pct <= -0.5:

            print(f"[STOP LOSS] {symbol}")

            self.execution.close_position(symbol)

    # =================================================
    # PNL CALC
    # =================================================
    def _calc_pnl(self, entry, price, side):

        if side == "Buy":
            return (price - entry) / entry * 100
        else:
            return (entry - price) / entry * 100
