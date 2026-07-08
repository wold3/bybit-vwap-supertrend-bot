import threading



class PositionManager:
    """
    Position Manager

    기능:
    - 현재 포지션 저장
    - 포지션 조회
    - 포지션 삭제
    - ExecutionEngine 연동
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

                "size": float(size),

                "entry_price": float(entry_price)

            }


        return True



    # =====================================
    # OPEN POSITION
    # =====================================

    def open_position(
        self,
        symbol,
        side,
        size,
        entry_price=0
    ):

        return self.set_position(

            symbol,

            side,

            size,

            entry_price

        )



    # =====================================
    # GET POSITION
    # =====================================

    def get_position(
        self,
        symbol
    ):

        with self.lock:

            return self.positions.get(
                symbol
            )



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
    # REMOVE POSITION
    # =====================================

    def remove_position(
        self,
        symbol
    ):

        with self.lock:

            if symbol in self.positions:

                del self.positions[symbol]

                return True


        return False



    # =====================================
    # CLOSE POSITION
    # =====================================

    def close_position(
        self,
        symbol
    ):

        return self.remove_position(

            symbol

        )



    # =====================================
    # UPDATE SIZE
    # =====================================

    def update_size(
        self,
        symbol,
        size
    ):

        with self.lock:

            if symbol not in self.positions:

                return False


            self.positions[symbol]["size"] = float(
                size
            )


        return True



    # =====================================
    # UPDATE ENTRY PRICE
    # =====================================

    def update_entry_price(
        self,
        symbol,
        price
    ):

        with self.lock:

            if symbol not in self.positions:

                return False


            self.positions[symbol]["entry_price"] = float(
                price
            )


        return True



    # =====================================
    # ALL POSITIONS
    # =====================================

    def get_all_positions(
        self
    ):

        with self.lock:

            return list(
                self.positions.values()
            )



    # =====================================
    # CLEAR
    # =====================================

    def clear(
        self
    ):

        with self.lock:

            self.positions.clear()



    # =====================================
    # COUNT
    # =====================================

    def count(
        self
    ):

        with self.lock:

            return len(
                self.positions
            )



    # =====================================
    # STATUS
    # =====================================

    def status(
        self
    ):

        with self.lock:

            return {

                "count":
                    len(self.positions),

                "symbols":
                    list(self.positions.keys()),

                "positions":
                    list(self.positions.values())

            }



# =====================================
# SINGLETON
# =====================================

position_manager = PositionManager()
