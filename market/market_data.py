# =====================================================
# market/market_data.py
# BYBIT V5 MARKET DATA MANAGER
# =====================================================

import pandas as pd
import time


from api.bybit_api import bybit_api


from config import (

    CANDLE_INTERVAL,
    MAX_HISTORY

)


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

        interval=None,

        limit=None

    ):


        try:


            if interval is None:

                interval = CANDLE_INTERVAL



            if limit is None:

                limit = MAX_HISTORY




            response = bybit_api.get_kline(

                interval=interval,

                limit=limit

            )



            if not response:


                add_log(

                    "KLINE EMPTY RESPONSE"

                )


                return None




            # ---------------------------------
            # BYBIT V5 RESULT PARSE
            # ---------------------------------

            rows = (

                response

                .get(

                    "result",

                    {}

                )

                .get(

                    "list",

                    []

                )

            )




            if not rows:


                add_log(

                    "KLINE LIST EMPTY"

                )


                return None





            df = pd.DataFrame(

                rows

            )





            # ---------------------------------
            # COLUMN SET
            # ---------------------------------

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

                    f"INVALID KLINE COLUMN {len(df.columns)}"

                )


                return None





            # ---------------------------------
            # SORT OLD -> NEW
            # ---------------------------------

            df = df.iloc[::-1].reset_index(

                drop=True

            )





            # ---------------------------------
            # NUMERIC CONVERT
            # ---------------------------------

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





            if len(df) < 10:


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



            if price is None:

                return 0



            return price




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
