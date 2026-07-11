# =====================================================
# close_position.py
# Bybit Demo Position Close Test
# =====================================================

from api.bybit_api import (
    bybit_api
)


from config import (
    DEFAULT_SYMBOL,
    CATEGORY
)





def main():


    print("====================")

    print("[CLOSE POSITION START]")

    print("====================")






    # =====================================
    # 현재 포지션 조회
    # =====================================


    position = (

        bybit_api

        .get_position()

    )



    if not position:


        print(

            "[POSITION ERROR]"

        )

        return







    try:


        data = (

            position

            ["result"]

            ["list"]

        )



        if not data:


            print(

                "[NO POSITION]"

            )


            return





        pos = data[0]





        size = float(

            pos.get(

                "size",

                0

            )

        )





        side = pos.get(

            "side"

        )







        if size == 0:


            print(

                "[NO POSITION]"

            )


            return







        print(

            "[CURRENT]",

            side,

            size

        )









        # =====================================
        # 반대 주문으로 종료
        # =====================================


        close_side = (

            "Sell"

            if side == "Buy"

            else

            "Buy"

        )





        print(

            "[CLOSE SIDE]",

            close_side

        )









        result = (

            bybit_api

            .place_order(

                close_side,

                size

            )

        )





        print(

            result

        )







        print("====================")

        print("[POSITION CLOSED]")

        print("====================")









    except Exception as e:


        print(

            "[CLOSE ERROR]",

            e

        )









if __name__ == "__main__":


    main()
