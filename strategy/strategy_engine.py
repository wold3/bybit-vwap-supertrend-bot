from indicators.vwap import VWAP
from indicators.supertrend import SuperTrend


class StrategyEngine:


    def __init__(self):


        self.vwap = VWAP()


        self.supertrend = SuperTrend()


        self.last_signal = None


        self.last_candle_time = None



        print(
            "[STRATEGY ENGINE READY]"
        )





    # ==================================
    # CANDLE PROCESS
    # ==================================


    def on_candle(self, candle):


        timestamp = candle["timestamp"]



        # -------------------------------
        # 같은 봉 중복 제거
        # -------------------------------

        if timestamp == self.last_candle_time:

            return None



        self.last_candle_time = timestamp





        close = candle["close"]


        high = candle["high"]


        low = candle["low"]


        volume = candle["volume"]




        # -------------------------------
        # INDICATORS
        # -------------------------------


        vwap_value = self.vwap.update(

            price=close,

            volume=volume

        )



        trend = self.supertrend.update(

            high,

            low,

            close

        )





        print(
            "[INDICATOR]",
            "PRICE:",
            close,
            "VWAP:",
            vwap_value,
            "TREND:",
            trend
        )






        # -------------------------------
        # SIGNAL LOGIC
        # -------------------------------


        signal = None




        # LONG

        if (

            close > vwap_value

            and trend is True

        ):


            signal = "BUY"





        # SHORT

        elif (

            close < vwap_value

            and trend is False

        ):


            signal = "SELL"






        # -------------------------------
        # duplicate signal block
        # -------------------------------


        if signal == self.last_signal:


            return None





        if signal:


            print(
                "[NEW SIGNAL]",
                signal
            )


            self.last_signal = signal



            return signal





        return None






strategy_engine = StrategyEngine()
