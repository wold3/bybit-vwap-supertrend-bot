# =====================================================
# market/market_data.py
# BYBIT MARKET DATA MANAGER
# =====================================================

import pandas as pd
import time



from api.bybit_api import (

    bybit_api

)



from config import (

    SYMBOL,

    CATEGORY

)



from web.server import (

    add_log

)







class MarketData:



    def __init__(self):


        self.last_data = None



        print(

            "[MARKET DATA READY]"

        )









    # =====================================================
    # GET KLINE
    # =====================================================

    def get_candles(

        self,

        interval="5",

        limit=200

    ):


        try:



            result = bybit_api.get_kline(

                interval,

                limit

            )



            if not result:


                return None





            rows = (

                result

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


                return None







            df = pd.DataFrame(

                rows

            )





            # Bybit V5 format

            df.columns = [

                "timestamp",

                "open",

                "high",

                "low",

                "close",

                "volume",

                "turnover"

            ]





            # reverse

            df = df.iloc[::-1]





            numeric = [

                "open",

                "high",

                "low",

                "close",

                "volume",

                "turnover"

            ]





            for col in numeric:


                df[col] = pd.to_numeric(

                    df[col],

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
    # LAST PRICE
    # =====================================================

    def price(self):


        try:


            return bybit_api.get_price()



        except:


            return 0









    # =====================================================
    # WAIT NEW CANDLE
    # =====================================================

    def wait(self, sec=5):


        time.sleep(

            sec

        )









# =====================================================
# INSTANCE
# =====================================================

market_data = MarketData()
