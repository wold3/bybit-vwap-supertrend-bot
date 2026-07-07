import os
from dotenv import load_dotenv


from risk.drawdown_guard import drawdown_guard


from risk.risk_engine import risk_engine


from ml.ml_filter import ml_filter


load_dotenv()





class StrategyEngine:


    def __init__(self):


        self.vwap_enable = (

            os.getenv(
                "VWAP_ENABLE",
                "true"
            ).lower()
            ==
            "true"

        )


        self.supertrend_enable = (

            os.getenv(
                "SUPERTREND_ENABLE",
                "true"
            ).lower()
            ==
            "true"

        )


        self.ml_enable = (

            os.getenv(
                "ML_FILTER_ENABLE",
                "true"
            ).lower()
            ==
            "true"

        )


        self.ml_threshold = float(

            os.getenv(
                "ML_THRESHOLD",
                "0.65"
            )

        )



        self.position = {}





    # =====================================
    # MAIN CHECK
    # =====================================

    def check(
        self,
        market_data
    ):


        symbol = market_data.get(
            "symbol"
        )


        price = market_data.get(
            "close"
        )



        if not symbol:

            return None



        # ==========================
        # Risk Check
        # ==========================


        if not risk_engine.can_trade():

            return None



        if not drawdown_guard.can_trade():

            print(
                "DRAW DOWN BLOCK"
            )

            return None





        # ==========================
        # Indicator
        # ==========================


        vwap = market_data.get(
            "vwap"
        )


        supertrend = market_data.get(
            "supertrend"
        )



        signal = None





        # ==========================
        # LONG 조건
        # ==========================


        if (

            self.vwap_enable

            and

            price > vwap

        ):


            signal = "Buy"





        # ==========================
        # SHORT 조건
        # ==========================


        elif (

            self.vwap_enable

            and

            price < vwap

        ):


            signal = "Sell"





        # ==========================
        # Supertrend Filter
        # ==========================


        if self.supertrend_enable:


            if supertrend == "UP":


                if signal != "Buy":

                    return None



            elif supertrend == "DOWN":


                if signal != "Sell":

                    return None



            else:

                return None





        # ==========================
        # ML FILTER
        # ==========================


        if self.ml_enable:


            probability = ml_filter.predict(

                market_data

            )



            print(

                "ML SCORE",

                probability

            )



            if probability < self.ml_threshold:


                print(

                    "ML BLOCK"

                )


                return None





        # ==========================
        # POSITION CHECK
        # ==========================


        if symbol in self.position:


            return self.check_exit(

                market_data

            )





        # ==========================
        # ENTRY SIGNAL
        # ==========================


        self.position[symbol] = signal



        return {


            "type":

                "ENTRY",


            "symbol":

                symbol,


            "side":

                signal,


            "qty":

                float(

                    os.getenv(

                        "DEFAULT_QTY",

                        "0.001"

                    )

                )

        }





    # =====================================
    # EXIT CHECK
    # =====================================

    def check_exit(
        self,
        data
    ):


        symbol = data.get(
            "symbol"
        )


        current = self.position.get(
            symbol
        )


        trend = data.get(
            "supertrend"
        )



        # LONG 종료

        if (

            current == "Buy"

            and

            trend == "DOWN"

        ):


            del self.position[symbol]


            return {


                "type":

                    "EXIT",


                "symbol":

                    symbol,


                "side":

                    "Sell"

            }




        # SHORT 종료

        if (

            current == "Sell"

            and

            trend == "UP"

        ):


            del self.position[symbol]


            return {


                "type":

                    "EXIT",


                "symbol":

                    symbol,


                "side":

                    "Buy"

            }




        return None





strategy_engine = StrategyEngine()
