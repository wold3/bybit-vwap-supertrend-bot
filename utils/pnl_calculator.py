class PnLCalculator:

    def __init__(
        self,
        fee_rate=0.0006,      # Bybit taker fee 기본값
        slippage=0.0005       # 평균 슬리피지
    ):

        self.fee_rate = fee_rate
        self.slippage = slippage

    # =====================================================
    # Realized PnL
    # =====================================================
    def realized_pnl(
        self,
        entry_price,
        exit_price,
        qty,
        side,
        leverage=1
    ):

        if side == "BUY":
            raw_pnl = (exit_price - entry_price) * qty
        else:
            raw_pnl = (entry_price - exit_price) * qty

        # 수수료 (진입 + 청산)
        fee = (entry_price + exit_price) * qty * self.fee_rate

        # 슬리피지
        slip = (entry_price + exit_price) * qty * self.slippage

        return (raw_pnl - fee - slip) * leverage

    # =====================================================
    # Unrealized PnL
    # =====================================================
    def unrealized_pnl(
        self,
        entry_price,
        current_price,
        qty,
        side,
        leverage=1
    ):

        if side == "BUY":
            raw_pnl = (current_price - entry_price) * qty
        else:
            raw_pnl = (entry_price - current_price) * qty

        return raw_pnl * leverage

    # =====================================================
    # ROI
    # =====================================================
    def roi(
        self,
        pnl,
        entry_price,
        qty
    ):

        if entry_price * qty == 0:
            return 0.0

        return (pnl / (entry_price * qty)) * 100


# =====================================================
# Singleton
# =====================================================
pnl_calculator = PnLCalculator()
