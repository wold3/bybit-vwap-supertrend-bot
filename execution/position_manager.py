import time


from api.bybit_api import bybit_api


from config import (
    CATEGORY,
    DEFAULT_SYMBOL,
)



class PositionManager:


    def __init__(self):

        self.position = None

        print("==============================")
        print("[POSITION MANAGER INIT]")
        print("==============================")



    # ==========================================
    # POSITION 조회
    # ==========================================

    def get_position(self):


        try:


            result = bybit_api.get_position()



            if result is None:

                return None



            positions = result["result"]["list"]



            for p in positions:


                size = float(

                    p.get(
                        "size",
                        0
                    )

                )


                if size > 0:


                    self.position = p

                    return p



            self.position = None

            return None



        except Exception as e:


            print(
                "[POSITION ERROR]",
                e
            )


            return None




    # ==========================================
    # 현재 방향
    # ==========================================

    def get_side(self):


        position = self.get_position()



        if position:


            return position.get(
                "side"
            )


        return None




    # ==========================================
    # ATR TP/SL 계산
    # ==========================================

    def calc_atr_levels(

        self,

        prices,

        multiplier=2.0

    ):


        if len(prices) < 20:


            return None, None



        high = max(

            prices[-20:]

        )


        low = min(

            prices[-20:]

        )



        atr = (

            high - low

        ) / 20



        tp = atr * multiplier

        sl = atr * multiplier



        return tp, sl




    # ==========================================
    # 손절 판단
    # ==========================================

    def should_stop_loss(

        self,

        entry_price,

        current_price,

        side,

        sl

    ):



        if side == "Buy":


            return (

                current_price

                <=

                entry_price - sl

            )



        if side == "Sell":


            return (

                current_price

                >=

                entry_price + sl

            )



        return False




    # ==========================================
    # 익절 판단
    # ==========================================

    def should_take_profit(

        self,

        entry_price,

        current_price,

        side,

        tp

    ):



        if side == "Buy":


            return (

                current_price

                >=

                entry_price + tp

            )



        if side == "Sell":


            return (

                current_price

                <=

                entry_price - tp

            )



        return False




    # ==========================================
    # EXIT 판단
    # ==========================================

    def evaluate_exit(

        self,

        prices

    ):


        position = self.get_position()



        if position is None:


            return None



        entry_price = float(

            position["avgPrice"]

        )



        side = position["side"]



        current_price = float(

            prices[-1]

        )



        tp, sl = self.calc_atr_levels(

            prices

        )



        if tp is None:


            return None




        if self.should_stop_loss(

            entry_price,

            current_price,

            side,

            sl

        ):


            return "STOP_LOSS"




        if self.should_take_profit(

            entry_price,

            current_price,

            side,

            tp

        ):


            return "TAKE_PROFIT"



        return None




    # ==========================================
    # CLOSE POSITION
    # ==========================================

    def close_position(self):


        try:


            position = self.get_position()



            if position is None:


                return None



            side = position["side"]



            qty = position["size"]



            close_side = (

                "Sell"

                if side == "Buy"

                else

                "Buy"

            )



            result = bybit_api.create_order(

                side=close_side,

                qty=qty

            )



            print(
                "[POSITION CLOSED]",
                result
            )


            return result



        except Exception as e:


            print(
                "[CLOSE ERROR]",
                e
            )


            return None




# singleton

position_manager = PositionManager()
