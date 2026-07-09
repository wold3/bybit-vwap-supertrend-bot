from indicators.indicator_engine import indicator_engine

from position.position_manager import position_manager

from config import DEFAULT_QTY




class StrategyEngine:


    def __init__(self):


        self.last_signal = None

        self.last_timestamp = None


        print(
            "[STRATEGY ENGINE READY]"
        )




    # =====================================================
    # CANDLE EVENT
    # =====================================================


    def on_candle(
        self,
        candle
    ):


        try:



            # ---------------------------------
            # 완성 캔들만 처리
            # ---------------------------------

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





            # ---------------------------------
            # Indicator Update
            # ---------------------------------


            indicator_engine.update(
                candle
            )



            market = indicator_engine.get_market_data(
                candle
            )



            if market is None:


                return None





            close = float(
                candle["close"]
            )



            vwap = market["vwap"]


            trend = market["supertrend"]


            atr = market["atr"]




            print(

                "[MARKET]",

                "PRICE:",
                close,

                "VWAP:",
                vwap,

                "TREND:",
                trend

            )






            # ---------------------------------
            # POSITION CHECK
            # ---------------------------------


            position_manager.sync()



            if position_manager.has_position():


                print(
                    "[STRATEGY BLOCK] POSITION EXISTS"
                )


                return None






            # ---------------------------------
            # SIGNAL
            # ---------------------------------


            signal = None




            if close > vwap and trend == "UP":


                signal = "BUY"





            elif close < vwap and trend == "DOWN":


                signal = "SELL"







            if signal is None:


                return None





            # ---------------------------------
            # DUPLICATE SIGNAL
            # ---------------------------------


            if signal == self.last_signal:


                print(
                    "[SIGNAL DUPLICATE]"
                )


                return None





            self.last_signal = signal





            # ---------------------------------
            # TP / SL
            # ---------------------------------


            tp = None

            sl = None




            if atr:


                atr = float(
                    atr
                )



                if signal == "BUY":


                    tp = close + (
                        atr * 2
                    )


                    sl = close - (
                        atr * 1.5
                    )




                elif signal == "SELL":


                    tp = close - (
                        atr * 2
                    )


                    sl = close + (
                        atr * 1.5
                    )





            result = {


                "signal":

                    signal,


                "qty":

                    DEFAULT_QTY,


                "take_profit":

                    round(tp,2)
                    if tp
                    else None,


                "stop_loss":

                    round(sl,2)
                    if sl
                    else None,

            }





            print(

                "[TRADE SIGNAL]",

                result

            )




            return result





        except Exception as e:


            print(

                "[STRATEGY ERROR]",

                e

            )


            return None





    # =====================================================
    # RESET
    # =====================================================


    def reset(self):


        self.last_signal = None

        self.last_timestamp = None



        print(
            "[STRATEGY RESET]"
        )






strategy_engine = StrategyEngine()
