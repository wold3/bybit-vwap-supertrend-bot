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



            # =================================================
            # BYBIT V5 RESPONSE NORMALIZE
            # =================================================

            rows = []



            # response = dict

            if isinstance(response, dict):


                result = response.get(

                    "result",

                    {}

                )


                if isinstance(result, dict):


                    rows = result.get(

                        "list",

                        []

                    )



                elif isinstance(result, list):


                    rows = result





            # response = list

            elif isinstance(response, list):


                rows = response




            if not rows:


                add_log(

                    "EMPTY KLINE"

                )


                return None





            # =================================================
            # DATAFRAME
            # =================================================

            df = pd.DataFrame(rows)



            if df.empty:


                return None





            # =================================================
            # COLUMN CHECK
            # =================================================

            if len(df.columns) < 7:


                add_log(

                    f"INVALID KLINE COLUMNS {df.columns}"

                )


                return None




            df = df.iloc[:,0:7]



            df.columns = [

                "timestamp",

                "open",

                "high",

                "low",

                "close",

                "volume",

                "turnover"

            ]





            # =================================================
            # SORT OLD -> NEW
            # =================================================

            df = df.iloc[::-1].reset_index(

                drop=True

            )





            # =================================================
            # NUMERIC
            # =================================================

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

                    f"NOT ENOUGH CANDLE {len(df)}"

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


            return bybit_api.get_price()



        except Exception as e:


            add_log(

                f"PRICE ERROR {e}"

            )


            return 0





    # =====================================================
    # WAIT
    # =====================================================

    def wait(

        self,

        sec=5

    ):


        time.sleep(sec)




# =====================================================
# INSTANCE
# =====================================================

market_data = MarketData()
