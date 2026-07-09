import pandas as pd
import time


from strategy.vwap import calculate_vwap
from strategy.supertrend import calculate_supertrend

from execution.order_manager import order_manager




class StrategyEngine:


    def __init__(self):

        self.candles = []

        self.position = None

        self.last_order_time = 0



        print(
            "[STRATEGY ENGINE READY]"
        )




    def on_candle(
        self,
        candle
    ):


        self.candles.append(
            candle
        )


        if len(self.candles) > 200:

            self.candles.pop(0)



        if len(self.candles) < 20:

            return





        df = pd.DataFrame(
            self.candles
        )



        vwap = calculate_vwap(
            df
        )


        trend = calculate_supertrend(
            df
        )



        close = candle["close"]



        print(
            "[INDICATOR]",
            "PRICE:",
            close,
            "VWAP:",
            vwap,
            "TREND:",
            trend
        )



        signal = None



        if trend and close > vwap:


            signal = "BUY"



        elif trend is False and close < vwap:


            signal = "SELL"





        if signal:


            self.execute(
                signal
            )







    def execute(
        self,
        signal
    ):


        now=time.time()



        if now-self.last_order_time < 60:

            return



        print(
            "[SIGNAL]",
            signal
        )



        if signal=="BUY":


            result = order_manager.create_order(

                "Buy",

                "0.001"

            )



            print(
                result
            )



        elif signal=="SELL":


            result = order_manager.create_order(

                "Sell",

                "0.001"

            )


            print(
                result
            )



        self.last_order_time=now





strategy_engine = StrategyEngine()
