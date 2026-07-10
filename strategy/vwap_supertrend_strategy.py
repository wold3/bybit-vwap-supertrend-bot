from config import (
    VWAP_LENGTH,
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER,
)


from indicators.indicator_engine import (
    indicator_engine
)





class VWAPSuperTrendStrategy:



    def __init__(self):

        print(
            "[VWAP SUPERTREND STRATEGY READY]"
        )





    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(
        self,
        candles
    ):


        try:


            if candles is None:

                return None




            # pandas DataFrame 대응

            if hasattr(
                candles,
                "to_dict"
            ):

                candles = candles.to_dict(
                    "records"
                )





            # candle normalize

            clean_candles = []



            for c in candles:



                clean_candles.append(


                    {


                    "open":

                        self.to_float(
                            c.get("open")
                        ),



                    "high":

                        self.to_float(
                            c.get("high")
                        ),



                    "low":

                        self.to_float(
                            c.get("low")
                        ),



                    "close":

                        self.to_float(
                            c.get("close")
                        ),



                    "volume":

                        self.to_float(
                            c.get("volume")
                        )


                    }


                )





            # indicator update

            market = None



            for candle in clean_candles:


                market = indicator_engine.update(
                    candle
                )





            if market is None:


                return None






            vwap = market.get(
                "vwap"
            )


            supertrend = market.get(
                "supertrend"
            )



            if vwap is None:


                return None



            if supertrend is None:


                return None





            close = clean_candles[-1][
                "close"
            ]





            print(

                "[MARKET]",

                "CLOSE:",
                close,

                "VWAP:",
                vwap,

                "TREND:",
                supertrend

            )







            # =====================================
            # BUY SIGNAL
            # =====================================


            if (

                close > vwap

                and

                supertrend == "UP"

            ):


                return {


                    "type":

                        "ENTRY",



                    "side":

                        "Buy",



                    "price":

                        close



                }







            # =====================================
            # SELL SIGNAL
            # =====================================


            if (

                close < vwap

                and

                supertrend == "DOWN"

            ):


                return {


                    "type":

                        "ENTRY",



                    "side":

                        "Sell",



                    "price":

                        close



                }







            return None





        except Exception as e:


            print(

                "[STRATEGY ERROR]",

                e

            )


            return None







    # =====================================================
    # SAFE FLOAT CONVERTER
    # =====================================================

    def to_float(
        self,
        value
    ):


        try:



            # pandas Series

            if hasattr(
                value,
                "iloc"
            ):


                value = value.iloc[-1]




            return float(
                value
            )



        except:


            return 0.0











vwap_supertrend_strategy = (

    VWAPSuperTrendStrategy()

)
