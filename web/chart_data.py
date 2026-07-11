# =====================================================
# web/chart_data.py
# Realtime Chart Data Manager
# =====================================================

import threading




class ChartData:


    def __init__(self):


        self.candles = []


        self.lock = threading.Lock()


        self.max_candles = 500



        print(
            "[CHART DATA READY]"
        )







    # =====================================================
    # ADD CANDLE
    # =====================================================


    def add(
        self,
        candle
    ):


        try:


            with self.lock:


                self.candles.append(

                    candle

                )



                if len(self.candles) > self.max_candles:


                    self.candles = (

                        self.candles[-self.max_candles:]

                    )



        except Exception as e:


            print(

                "[CHART ADD ERROR]",

                e

            )







    # =====================================================
    # GET DATA
    # =====================================================


    def get(self):


        try:


            with self.lock:


                return list(

                    self.candles

                )



        except:


            return []









# =====================================================
# INSTANCE
# =====================================================


chart_data = ChartData()






# =====================================================
# COMPATIBILITY FUNCTION
# =====================================================


def add_candle(
    candle
):


    chart_data.add(

        candle

    )
