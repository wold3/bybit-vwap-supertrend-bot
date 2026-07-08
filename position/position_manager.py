import threading


class PositionManager:
    """
    Position Manager

    기능
    - 현재 포지션 저장
    - 포지션 조회
    - 포지션 삭제
    """

    def __init__(self):

        self.lock = threading.Lock()

        self.positions = {}



    # =====================================
    # ADD / UPDATE
    # =====================================

    def set_position(
        self,
        symbol,
        side,
        size,
        entry_price=0
    ):

        with self.lock:

            self.positions[symbol] = {

                "symbol": symbol,

                "side": side,

                "size": size,

                "entry_price": entry_price

            }

        return True



    # =====================================
    # GET
    # =====================================

    def get_position(
        self,
        symbol
    ):

        with self.lock:

            return self.positions.get(symbol)



    # =====================================
    # HAS POSITION
    # =====================================

    def has_position(
        self,
        symbol
    ):

        with self.lock:

            return symbol in self.positions



    # =====================================
    # REMOVE
    # =====================================

    def remove_position(
        self,
        symbol
    ):

        with self.lock:

            if symbol in self.positions:

                del self.positions[symbol]



    # =====================================
    # ALL POSITIONS
    # =====================================

    def get_all_positions(self):

        with self.lock:

            return list(self.positions.values())



    # =====================================
    # CLEAR
    # =====================================

    def clear(self):

        with self.lock:

            self.positions.clear()



    # =====================================
    # STATUS
    # =====================================

    def status(self):

        with self.lock:

            return {

                "count": len(self.positions),

                "symbols": list(self.positions.keys())

            }


# singleton
position_manager = PositionManager()
