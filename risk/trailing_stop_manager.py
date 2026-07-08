import os
import threading

from dotenv import load_dotenv

load_dotenv()


class TrailingStopManager:
    """
    Trailing Stop Manager

    기능
    - 최고가/최저가 추적
    - Trailing Stop 계산
    - 상태 관리
    """

    def __init__(self):

        self.lock = threading.Lock()

        self.trailing_percent = float(
            os.getenv(
                "TRAILING_STOP_PERCENT",
                "1.0"
            )
        )

        self.positions = {}


    # =====================================
    # UPDATE
    # =====================================

    def update(
        self,
        symbol,
        side,
        price
    ):

        with self.lock:

            if symbol not in self.positions:

                self.positions[symbol] = {

                    "side": side,

                    "highest": price,

                    "lowest": price

                }

                return

            position = self.positions[symbol]

            if side == "Buy":

                if price > position["highest"]:

                    position["highest"] = price

            else:

                if price < position["lowest"]:

                    position["lowest"] = price


    # =====================================
    # CALCULATE STOP
    # =====================================

    def calculate_stop(
        self,
        symbol,
        side
    ):

        with self.lock:

            position = self.positions.get(symbol)

            if position is None:

                return None

            percent = self.trailing_percent / 100

            if side == "Buy":

                return round(
                    position["highest"] * (1 - percent),
                    4
                )

            return round(
                position["lowest"] * (1 + percent),
                4
            )


    # =====================================
    # RESET
    # =====================================

    def reset(
        self,
        symbol
    ):

        with self.lock:

            self.positions.pop(symbol, None)


    # =====================================
    # STATUS
    # =====================================

    def status(self):

        with self.lock:

            return {

                "symbols": list(self.positions.keys()),

                "count": len(self.positions),

                "trailing_percent": self.trailing_percent

            }


# singleton
trailing_stop_manager = TrailingStopManager()
