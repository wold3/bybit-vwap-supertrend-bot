# =====================================================
# test_order.py
# Bybit Demo Manual Order Test
# =====================================================

import time



from api.bybit_api import (
    bybit_api
)


from risk.risk_manager import (
    risk_manager
)


from config import (
    DEFAULT_SYMBOL
)





def main():


    print("====================")

    print("[TEST ORDER START]")

    print("====================")





    # =====================================
    # 현재 가격 확인
    # =====================================


    candles = (

        bybit_api

        .get_kline()

    )



    if not candles:


        print(

            "[NO MARKET DATA]"

        )

        return





    price = float(

        candles[-1][4]

    )



    print(

        "[PRICE]",

        price

    )









    # =====================================
    # 테스트 Equity 설정
    # =====================================


    risk_manager.update_equity(

        10000

    )









    # =====================================
    # 수량 계산
    # =====================================


    risk = (

        risk_manager

        .check(

            price

        )

    )



    if not risk:


        print(

            "[RISK BLOCK]"

        )


        return







    qty = risk["qty"]





    print(

        "[QTY]",

        qty

    )









    # =====================================
    # BUY TEST
    # =====================================


    print(

        "[SEND BUY]"

    )




    result = (

        bybit_api

        .place_order(

            "Buy",

            qty

        )

    )





    print(

        result

    )









    time.sleep(3)







    # =====================================
    # TP SL TEST
    # =====================================


    tp_sl = (

        risk_manager

        .calculate_tp_sl(

            "Buy",

            price

        )

    )





    print(

        "[TP]",

        tp_sl["tp"]

    )


    print(

        "[SL]",

        tp_sl["sl"]

    )





    stop = (

        bybit_api

        .set_trading_stop(

            tp_sl["tp"],

            tp_sl["sl"]

        )

    )





    print(

        stop

    )





    print("====================")

    print("[TEST COMPLETE]")

    print("====================")









if __name__ == "__main__":


    main()
