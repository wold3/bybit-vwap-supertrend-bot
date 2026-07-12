# =====================================================
# market/market_data.py
# BYBIT V5 MARKET DATA MANAGER
# AUTO TRADING VERSION
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


        self.last_timestamp = None



        print(

            "[MARKET DATA READY]"

        )









    # =====================================================
    # CANDLE
    # =====================================================

    def get_candles(


        self,


        interval="5",


        limit=200


    ):


        try:



            symbol = get_trading_symbol()





            # SYMBOL CHANGE

            if symbol != self.last_symbol:



                bybit_api.change_symbol(

                    symbol

                )


                self.last_symbol = symbol


                self.last_data=None



                add_log(

                    f"SYMBOL CHANGE {symbol}"

                )







            response = bybit_api.get_kline(


                interval,


                limit


            )





            if not response:


                return None





            rows = response.get(


                "result",{}

            ).get(


                "list",[]

            )






            if not rows:


                add_log(

                    "NO KLINE"

                )


                return None







            df=pd.DataFrame(


                rows

            )






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






            # BYBIT DESC -> ASC

            df=df.iloc[::-1]


            df=df.reset_index(

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









            if len(df)<100:


                add_log(

                    f"LOW DATA {len(df)}"

                )


                return None







            # 현재 진행중 봉 제거

            df=df.iloc[:-1]







            # 중복 데이터 체크


            last=df["timestamp"].iloc[-1]



            if last == self.last_timestamp:


                return self.last_data





            self.last_timestamp=last






            self.last_data=df






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
    # DELAY
    # =====================================================

    def wait(self,sec=5):


        time.sleep(sec)









# =====================================================
# INSTANCE
# =====================================================


market_data = MarketData()
