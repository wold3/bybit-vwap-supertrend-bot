# =====================================================
# web/chart_data.py
# Chart Data Manager
# =====================================================


import threading





# 최근 캔들 저장

CANDLES = []



MAX_CANDLES = 200



LOCK = threading.Lock()







# =====================================================
# ADD CANDLE
# =====================================================


def add_candle(candle):


    with LOCK:


        CANDLES.append(

            candle

        )



        if len(CANDLES) > MAX_CANDLES:


            CANDLES.pop(0)







# =====================================================
# GET CANDLES
# =====================================================


def get_candles():


    with LOCK:


        return list(

            CANDLES

        )







# =====================================================
# CLEAR
# =====================================================


def clear_chart():


    with LOCK:


        CANDLES.clear()
