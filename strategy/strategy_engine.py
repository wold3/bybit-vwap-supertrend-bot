import time


from indicators.indicator_engine import (
    indicator_engine
)


from position.position_manager import (
    position_manager
)


from config import (
    DEFAULT_SYMBOL
)




class StrategyEngine:


    def __init__(self):


        self.symbol = DEFAULT_SYMBOL


        self.last_signal = None

        self.last_timestamp = None


        self.min_vwap_distance = 0.0015


        print(
            "[STRATEGY ENGINE READY]"
        )




    # =====================================================
    # CANDLE PROCESS
    # =====================================================

    def on_candle(
        self,
        candle
    ):


        try:



            # 완성봉만 처리

            if not candle.get(
                "confirm",
                False
            ):

                return None





            timestamp = int(
                candle["timestamp"]
            )



            if timestamp == self.last_timestamp:

                return None



            self.last_timestamp = timestamp





            # indicator update


            indicator_engine.update(
                candle
            )



            market = (
                indicator_engine.get_market_data(
                    candle
                )
            )



            if market is None:

                return None





            close = float(
                candle["close"]
            )


            vwap = market["vwap"]


            trend = market["supertrend"]





            print(
                "[INDICATOR]",
                "PRICE=",
                close,
                "VWAP=",
                vwap,
                "TREND=",
                trend
            )





            # =================================================
            # POSITION CHECK
            # =================================================


            try:


                position_manager.sync()



                if position_manager.has_position():

                    print(
                        "[STRATEGY BLOCK] POSITION EXISTS"
                    )


                    return None



            except Exception as e:


                print(
                    "[POSITION CHECK ERROR]",
                    e
                )






            # =================================================
            # VWAP DISTANCE FILTER
            # =================================================


            distance = abs(
                close - vwap
            ) / vwap



            if distance < self.min_vwap_distance:


                print(
                    "[STRATEGY BLOCK] VWAP TOO CLOSE",
                    distance
                )


                return None






            signal = None





            # =================================================
            # ENTRY RULE
            # =================================================


            if (

                close > vwap

                and

                trend == "UP"

            ):


                signal = "BUY"





            elif (

                close < vwap

                and

                trend == "DOWN"

            ):


                signal = "SELL"








            if signal is None:


                return None






            # =================================================
            # DUPLICATE SIGNAL
            # =================================================


            if signal == self.last_signal:


                print(
                    "[SIGNAL BLOCK] DUPLICATE",
                    signal
                )


                return None





            self.last_signal = signal





            print(
                "[TRADE SIGNAL]",
                signal
            )



            return signal





        except Exception as e:


            print(
                "[STRATEGY ERROR]",
                e
            )


            return None






strategy_engine = StrategyEngine()
