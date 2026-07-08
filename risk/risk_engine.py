import os
import threading

from dotenv import load_dotenv

load_dotenv()


class RiskEngine:
    """
    Risk Engine

    기능
    - 최대 거래횟수 관리
    - 거래 가능 여부 판단
    """

    def __init__(self):

        self.lock = threading.Lock()

        self.max_trades = int(
            os.getenv(
                "MAX_TRADES",
                "100"
            )
        )

        self.trade_count = 0


    # =====================================
    # 거래 가능 여부
    # =====================================

    def can_trade(self):

        with self.lock:

            return self.trade_count < self.max_trades


    # =====================================
    # 거래 기록
    # =====================================

    def register_trade(self):

        with self.lock:

            self.trade_count += 1


    # =====================================
    # 리셋
    # =====================================

    def reset(self):

        with self.lock:

            self.trade_count = 0


    # =====================================
    # 상태
    # =====================================

    def status(self):

        with self.lock:

            return {

                "trade_count": self.trade_count,

                "max_trades": self.max_trades,

                "can_trade": self.trade_count < self.max_trades

            }


# singleton
risk_engine = RiskEngine()
