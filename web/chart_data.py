# =====================================================
# web/chart_data.py
# Realtime Chart Data Manager
# =====================================================

import threading





# =====================================================
# STORAGE
# =====================================================


candles = []


MAX_CANDLES = 200



lock = threading.Lock()







# =====================================================
# ADD CANDLE
# =====================================================


def add_candle(
    candle
):


    try:


        with lock:


            candles.append(

                candle

            )



            if len(candles) > MAX_CANDLES:


                candles.pop(0)





    except Exception as e:


        print(

            "[CHART DATA ERROR]",

            e

        )









# =====================================================
# GET CHART DATA
# =====================================================


def get_chart():


    try:


        with lock:


            return list(

                candles

            )



    except Exception as e:


        print(

            "[CHART GET ERROR]",

            e

        )


        return []
