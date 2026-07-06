import logging

logger = logging.getLogger(__name__)


class RiskEngine:

    def __init__(self):

        self.max_drawdown = -50
        self.daily_pnl = 0
        self.trade_count = 0
        self.max_trades_per_day = 200

    # =====================================================
    # 거래 허용 여부
    # =====================================================
    def allow_trade(self):

        if self.daily_pnl <= self.max_drawdown:
            logger.warning("RISK BLOCK: max drawdown reached")
            return False

        if self.trade_count >= self.max_trades_per_day:
            logger.warning("RISK BLOCK: max trade count reached")
            return False

        return True

    # =====================================================
    # pnl 업데이트
    # =====================================================
    def update(self, pnl):

        self.daily_pnl += pnl
        self.trade_count += 1

    # =====================================================
    # 상태
    # =====================================================
    def status(self):

        return {
            "daily_pnl": self.daily_pnl,
            "trade_count": self.trade_count
        }


risk_engine = RiskEngine()
