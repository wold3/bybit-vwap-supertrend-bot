import time



from indicators.vwap import calculate_vwap

from indicators.supertrend import supertrend






class StrategyEngine:



    def __init__(self):


        self.last_signal = None


        self.last_timestamp = None



        self.ready = False



        print(
            "[STRATEGY ENGINE READY]"
        )








    # ==================================
    # CANDLE INPUT
    # ==================================


    def on_candle(
            self,
            candle
    ):



        try:



            timestamp = candle["timestamp"]



            close = float(

                candle["close"]

            )



            high = float(

                candle["high"]

            )


            low = float(

                candle["low"]

            )


            volume = float(

                candle["volume"]

            )








            # 중복 캔들 방지

            if timestamp == self.last_timestamp:


                return None




            self.last_timestamp = timestamp








            # ==========================
            # VWAP
            # ==========================


            vwap = calculate_vwap(

                candle

            )







            # ==========================
            # SUPERTREND
            # ==========================


            trend = supertrend.update(


                high,


                low,


                close



            )








            print(

                "[INDICATOR]",

                "PRICE:",

                close,

                "VWAP:",

                vwap,

                "TREND:",

                trend

            )









            signal = "HOLD"








            # ==========================
            # LONG CONDITION
            # ==========================


            if (


                close > vwap

                and

                trend is True


            ):



                signal = "BUY"







            # ==========================
            # SHORT CONDITION
            # ==========================


            elif (


                close < vwap

                and

                trend is False


            ):



                signal = "SELL"







            else:


                signal = "HOLD"








            # 같은 신호 반복 방지

            if signal == self.last_signal:


                return None





            self.last_signal = signal





            if signal != "HOLD":


                print(

                    "[TRADE SIGNAL]",

                    signal

                )


                return signal





            return None






        except Exception as e:


            print(

                "[STRATEGY ERROR]",

                e

            )


            return None












strategy_engine = StrategyEngine()
