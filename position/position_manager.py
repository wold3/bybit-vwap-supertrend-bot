# position/position_manager.py

import threading



class PositionManager:
    """
    Position Manager

    기능:
    - 현재 보유 포지션 관리
    - Entry/Exit 상태 저장
    - Private WS 동기화
    """



    def __init__(self):

        self.lock = threading.Lock()

        self.positions = {}





    # =====================================
    # SET POSITION
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


                "symbol":

                    symbol,


                "side":

                    side,


                "size":

                    float(size),


                "entry_price":

                    float(entry_price)


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


            position = self.positions.get(

                symbol

            )


            if position:

                return position.copy()


            return None





    # =====================================
    # CHECK POSITION
    # =====================================

    def has_position(
        self,
        symbol
    ):


        with self.lock:


            return symbol in self.positions





    # =====================================
    # UPDATE SIZE
    # =====================================

    def update_size(
        self,
        symbol,
        size
    ):


        with self.lock:


            if symbol in self.positions:


                self.positions[symbol]["size"] = float(size)


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
    # REMOVE
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
    # ALL POSITIONS
    # =====================================

    def get_all_positions(
        self
    ):


        with self.lock:


            return [

                pos.copy()

                for pos in self.positions.values()

            ]





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
    # CLEAR
    # =====================================

    def clear(
        self
    ):


        with self.lock:


            self.positions.clear()





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


                "positions":

                    list(

                        self.positions.values()

                    )


            }





# singleton

position_manager = PositionManager()
