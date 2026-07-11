# =====================================================
# web/chart_data.py
# Chart Data Manager
# =====================================================

import threading





# =====================================================
# MEMORY STORAGE
# =====================================================


candles = []


lock = threading.Lock()







# =====================================================
# UPDATE CANDLE
# =====================================================


def update_chart(
    data
):


    try:


        with lock:


            candles.append(


                {


                    "time":

                        int(

                            data["time"]

                        ),


                    "open":

                        float(

                            data["open"]

                        ),


                    "high":

                        float(

                            data["high"]

                        ),


                    "low":

                        float(

                            data["low"]

                        ),


                    "close":

                        float(

                            data["close"]

                        )


                }


            )





            # 최대 500개 유지


            if len(candles) > 500:


                candles.pop(0)







    except Exception as e:


        print(

            "[CHART UPDATE ERROR]",

            e

        )









# =====================================================
# GET CHART
# =====================================================


def get_chart():


    with lock:


        return candles.copy()







# =====================================================
# LOAD INITIAL DATA
# =====================================================


def load_initial(
    data
):


    try:


        with lock:


            candles.clear()



            for c in data:


                candles.append(


                    {


                        "time":

                            int(c["time"]),


                        "open":

                            float(c["open"]),


                        "high":

                            float(c["high"]),


                        "low":

                            float(c["low"]),


                        "close":

                            float(c["close"])


                    }


                )



    except Exception as e:


        print(

            "[CHART LOAD ERROR]",

            e

        )
