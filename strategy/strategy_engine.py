import os

from dotenv import load_dotenv


from risk.risk_engine import risk_engine

from risk.drawdown_guard import drawdown_guard

from ml.ml_filter import ml_filter

from position.position_manager import position_manager



load_dotenv()





class StrategyEngine:


    def __init__(self):


        self.default_qty = float(

            os.getenv(

                "DEFAULT_QTY",

                "0.001"

            )

        )





    # =====================================
    # MAIN CHECK
    # =====================================

    def check(
        self,
        market_data
    ):


        if not market_data:

            return None



        symbol = market_data.get(

            "symbol"

        )


        price = market_data.get(

            "close"

        )


        vwap = market_data.get(

            "vwap"

        )


        trend = market_data.get(

            "supertrend"

        )



        if not symbol or price is None:

            return None





        # =================================
        # EXIT FIRST
        # =================================

        if position_manager.has_position(

            symbol

        ):


            return self.check_exit(

                market_data

            )





        # =================================
        # INDICATOR CHECK
        # =================================

        if vwap is None:

            return None



        if trend in (

            None,

            "FLAT"

        ):

            return None





        # =================================
        # RISK CHECK
        # =================================

        if not risk_engine.can_trade():


            print(

                "[RISK BLOCK]"

            )


            return None





        if not drawdown_guard.can_trade():


            print(

                "[DRAWDOWN BLOCK]"

            )


            return None





        # =================================
        # ML FILTER
        # =================================

        if not ml_filter.allow_trade(

            market_data

        ):


            print(

                "[ML BLOCK]"

            )


            return None





        # =================================
        # LONG ENTRY
        # =================================

        if (

            price > vwap

            and

            trend == "UP"

        ):


            return {


                "type":

                    "ENTRY",


                "symbol":

                    symbol,


                "side":

                    "Buy",


                "qty":

                    self.default_qty


            }





        # =================================
        # SHORT ENTRY
        # =================================

        if (

            price < vwap

            and

            trend == "DOWN"

        ):


            return {


                "type":

                    "ENTRY",


                "symbol":

                    symbol,


                "side":

                    "Sell",


                "qty":

                    self.default_qty


            }



        return None





    # =====================================
    # EXIT CHECK
    # =====================================

    def check_exit(
        self,
        market_data
    ):


        symbol = market_data.get(

            "symbol"

        )


        trend = market_data.get(

            "supertrend"

        )



        position = position_manager.get_position(

            symbol

        )



        if not position:

            return None



        side = position.get(

            "side"

        )



        size = position.get(

            "size"

        )





        # LONG EXIT

        if (

            side == "Buy"

            and

            trend == "DOWN"

        ):


            return {


                "type":

                    "EXIT",


                "symbol":

                    symbol,


                "side":

                    "Sell",


                "qty":

                    size


            }





        # SHORT EXIT

        if (

            side == "Sell"

            and

            trend == "UP"

        ):


            return {


                "type":

                    "EXIT",


                "symbol":

                    symbol,


                "side":

                    "Buy",


                "qty":

                    size


            }





        return None





    # =====================================
    # STATUS
    # =====================================

    def status(
        self
    ):


        return {


            "default_qty":

                self.default_qty

        }





strategy_engine = StrategyEngine()
