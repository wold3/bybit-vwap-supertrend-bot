# =====================================================
# market/market_data.py
# BYBIT MARKET DATA MANAGER
# =====================================================

import pandas as pd
import time


from api.bybit_api import bybit_api


from web.server import add_log





class MarketData:


    def __init__(self):

        self.last_data = None

        print(
            "[MARKET DATA READY]"
        )




    # =====================================================
    # GET CANDLE DATA
    # =====================================================

    def get_candles(

        self,

        interval="5",

        limit=200

    ):


        try:


            rows = bybit_api.get_kline(

                limit=limit

            )



            if not rows:


                return None




            df = pd.DataFrame(

                rows

            )



            if len(df.columns) == 7:


                df.columns = [

                    "timestamp",

                    "open",

                    "high",

                    "low",

                    "close",

                    "volume",

                    "turnover"

                ]



            else:


                add_log(

                    "INVALID KLINE FORMAT"

                )


                return None




            # 최신 캔들 기준 정렬

            df = df.iloc[::-1]




            numeric_columns = [

                "open",

                "high",

                "low",

                "close",

                "volume",

                "turnover"

            ]



            for col in numeric_columns:


                df[col] = pd.to_numeric(

                    df[col],

                    errors="coerce"

                )




            df["timestamp"] = pd.to_numeric(

                df["timestamp"],

                errors="coerce"

            )



            df.dropna(

                inplace=True

            )



            self.last_data = df



            return df




        except Exception as e:


            add_log(

                f"MARKET DATA ERROR {e}"

            )


            return None





    # =====================================================
    # CURRENT PRICE
    # =====================================================

    def price(self):


        try:


            return bybit_api.get_price()



        except Exception:


            return 0





    # =====================================================
    # WAIT
    # =====================================================

    def wait(

        self,

        sec=5

    ):


        time.sleep(

            sec

        )





# =====================================================
# INSTANCE
# =====================================================

market_data = MarketData()
