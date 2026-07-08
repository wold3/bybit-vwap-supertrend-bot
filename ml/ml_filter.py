import os
import threading

from dotenv import load_dotenv

load_dotenv()


class MLFilter:
    """
    ML Trade Filter

    기능
    - ML 사용 여부
    - 신호 필터링
    """

    def __init__(self):

        self.lock = threading.Lock()

        self.enabled = (

            os.getenv(
                "USE_ML_FILTER",
                "false"
            ).lower() == "true"

        )


    # =====================================
    # TRADE FILTER
    # =====================================

    def allow_trade(
        self,
        market_data
    ):

        if not self.enabled:

            return True

        if market_data is None:

            return False

        # ============================
        # TODO
        # 실제 ML 모델 예측 추가
        # ============================

        return True


    # =====================================
    # ENABLE
    # =====================================

    def enable(self):

        with self.lock:

            self.enabled = True


    # =====================================
    # DISABLE
    # =====================================

    def disable(self):

        with self.lock:

            self.enabled = False


    # =====================================
    # STATUS
    # =====================================

    def status(self):

        with self.lock:

            return {

                "enabled": self.enabled

            }


# singleton
ml_filter = MLFilter()
