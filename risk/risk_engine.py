import time


class RiskEngine:

    def __init__(self):

        # 하루 기준 초기화
        self.start_balance = 10000
        self.current_balance = 10000

        self.daily_loss_limit = -5.0   # %
        self.max_drawdown = -10.0      # %

        self.trading_halted = False

    # =================================================
    # PnL 업데이트
    # =================================================
    def update_pnl(self, pnl):

        self.current_balance += pnl

    # =================================================
    # 리스크 체크
    # =================================================
    def check_risk(self):

        pnl_pct = (
            (self.current_balance - self.start_balance)
            / self.start_balance
        ) * 100

        # ============================================
        # 1. Daily Loss
        # ============================================
        if pnl_pct <= self.daily_loss_limit:
            self.trading_halted = True
            print("[RISK] DAILY LOSS LIMIT HIT → TRADING STOP")
            return False

        # ============================================
        # 2. Max Drawdown
        # ============================================
        if pnl_pct <= self.max_drawdown:
            self.trading_halted = True
            print("[RISK] MAX DRAWDOWN HIT → TRADING STOP")
            return False

        return True

    # =================================================
    # 트레이딩 가능 여부
    # =================================================
    def can_trade(self):

        return not self.trading_halted

    # =================================================
    # 리셋 (새날 시작)
    # =================================================
    def reset(self):

        self.start_balance = self.current_balance
        self.trading_halted = False


# 싱글톤
risk_engine = RiskEngine()
