# =====================================================
# market/market_data.py
# BYBIT MARKET DATA MANAGER
# =====================================================

import pandas as pd
import time


from api.bybit_api import bybit_api


from web.server import (

    add_log,

    get_trading_symbol

)



class MarketData:


    def __init__(self):

        self.last_data = None

        self.last_symbol = None


        print(
            "[MARKET DATA READY]"
        )




    # =====================================================
    # GET CANDLES
    # =====================================================

    def get_candles(

        self,

        interval="5",

        limit=200

    ):


        try:


            symbol = get_trading_symbol()



            # ---------------------------------
            # SYMBOL CHANGE DETECT
            # ---------------------------------

            if symbol != self.last_symbol:


                self.last_data = None


                self.last_symbol = symbol


                add_log(

                    f"MARKET SYMBOL SWITCH {symbol}"

                )





            response = bybit_api.get_kline(

                interval=interval,

                limit=limit

            )



            if not response:

                return None





            rows=[]



            # ---------------------------------
            # BYBIT V5 NORMALIZE
            # ---------------------------------

            if isinstance(response,dict):


                result=response.get(

                    "result",

                    {}

                )


                if isinstance(result,dict):


                    rows=result.get(

                        "list",

                        []

                    )



            elif isinstance(response,list):


                rows=response





            if not rows:


                add_log(

                    "EMPTY KLINE"

                )


                return None





            df=pd.DataFrame(rows)





            if df.empty:

                return None





            if len(df.columns)<7:


                add_log(

                    "INVALID KLINE"

                )


                return None





            df=df.iloc[:,0:7]



            df.columns=[


                "timestamp",

                "open",

                "high",

                "low",

                "close",

                "volume",

                "turnover"


            ]






            # OLD -> NEW


            df=df.iloc[::-1].reset_index(

                drop=True

            )







            numeric=[


                "open",

                "high",

                "low",

                "close",

                "volume",

                "turnover"


            ]





            for col in numeric:


                df[col]=pd.to_numeric(

                    df[col],

                    errors="coerce"

                )





            df["timestamp"]=pd.to_numeric(

                df["timestamp"],

                errors="coerce"

            )





            df.dropna(

                inplace=True

            )






            if len(df)<50:


                add_log(

                    f"NOT ENOUGH DATA {len(df)}"

                )


                return None






            self.last_data=df



            return df





        except Exception as e:


            add_log(

                f"MARKET DATA ERROR {e}"

            )


            return None









    # =====================================================
    # PRICE
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
