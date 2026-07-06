
from ml_filter import ml_filter
from position_sizer import position_sizer


class StrategyEngine:

    def __init__(self, execution_engine):

        self.execution = execution_engine

        self.tp1_hit = {}
        self.be_moved = {}

    # =================================================
    # SIGNAL ENTRY (ML + SIZING + EXECUTION)
    # =================================================
    def on_signal(self, symbol, side, price, market_data=None):

        # ============================================
        # 1. ML FILTER GATE
        # ============================================
        if market_data:

            if not ml_filter.allow_trade(market_data):

                print(f"[STRATEGY] BLOCKED BY ML FILTER: {symbol}")

                return

        # ============================================
        # 2. STOP LOSS 기준 설정
        # ============================================
        stop_loss_price = price * 0.995  # -0.5% 고정 예시

        # ============================================
        # 3. ACCOUNT BALANCE (임시 or API 연결 가능)
        # ============================================
        balance = 10000  # TODO: Bybit wallet balance API 연결

        # ============================================
        # 4. POSITION SIZE 계산 (핵심)
        # ============================================
        qty = position_sizer.calculate(
            balance=balance,
            entry_price=price,
            stop_loss_price=stop_loss_price
        )

        if qty <= 0:
            print("[STRATEGY] INVALID QTY")
            return

        # ============================================
        # 5. EXECUTE TRADE
        # ============================================
        self.execution.execute(symbol, side, qty)

        # 상태 초기화
        self.tp1_hit[symbol] = False
        self.be_moved[symbol] = False

    # =================================================
    # PRICE UPDATE LOOP (TP / SL / BE MANAGEMENT)
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

            print(f"[TP1] {symbol}")

            self.tp1_hit[symbol] = True

            self.execution.partial_close(symbol, 0.5)

        # ============================================
        # BREAKEVEN MOVE
        # ============================================
        if pnl_pct >= 0.3 and not self.be_moved.get(symbol):

            print(f"[BE MOVE] {symbol}")

            self.be_moved[symbol] = True

            self.execution.move_sl_to_be(symbol)

        # ============================================
        # FINAL TAKE PROFIT
        # ============================================
        if pnl_pct >= 1.0:

            print(f"[TP2 EXIT] {symbol}")

            self.execution.close_position(symbol)

        # ============================================
        # STOP LOSS
        # ============================================
        if pnl_pct <= -0.5:

            print(f"[STOP LOSS] {symbol}")

            self.execution.close_position(symbol)

    # =================================================
    # PNL CALCULATION
    # =================================================
    def _calc_pnl(self, entry, price, side):

        if side == "Buy":
            return (price - entry) / entry * 100
        else:
            return (entry - price) / entry * 100
