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


            response = bybit_api.get_kline(

                interval=interval,

                limit=limit

            )



            if not response:


                return None




            rows = response.get(

                "result",

                {}

            ).get(

                "list",

                []

            )



            if not rows:


                add_log(

                    "EMPTY KLINE DATA"

                )

                return None





            df = pd.DataFrame(

                rows

            )




            if len(df.columns) != 7:


                add_log(

                    f"INVALID KLINE FORMAT {df.columns}"

                )


                return None





            df.columns = [


                "timestamp",

                "open",

                "high",

                "low",

                "close",

                "volume",

                "turnover"


            ]





            # Bybit 최신 → 과거 순서
            # 전략 계산용 과거 → 최신 변경

            df = df.iloc[::-1].reset_index(

                drop=True

            )





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





            if len(df) < 50:


                add_log(

                    "NOT ENOUGH CANDLE DATA"

                )


                return None





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


            price = bybit_api.get_price()


            if price:


                return price



            return 0



        except Exception as e:


            add_log(

                f"PRICE ERROR {e}"

            )


            return 0







    # =====================================================
    # LAST DATA
    # =====================================================


    def get_last_data(self):


        return self.last_data







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
