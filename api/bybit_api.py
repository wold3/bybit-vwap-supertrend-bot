import time
from pprint import pprint

from pybit.unified_trading import HTTP


class BybitAPI:


    def __init__(self, config):

        self.session = HTTP(

            testnet=config.BYBIT_TESTNET,

            demo=config.BYBIT_DEMO,

            api_key=config.BYBIT_API_KEY,

            api_secret=config.BYBIT_API_SECRET,

            recv_window=10000

        )


        self.retry_count = 3



    # =====================================================
    # SAFE API CALL
    # =====================================================

    def _safe_call(

        self,

        func,

        *args,

        **kwargs

    ):


        for attempt in range(

            self.retry_count

        ):


            try:


                response = func(

                    *args,

                    **kwargs

                )


                if response.get(

                    "retCode",

                    -1

                ) == 0:


                    return response



                error = response.get(

                    "retMsg",

                    "UNKNOWN"

                )


                print(

                    "[BYBIT ERROR]",

                    error

                )


                # rate limit

                if "rate" in error.lower():


                    time.sleep(3)



            except Exception as e:


                print(

                    "[API RETRY]",

                    attempt + 1,

                    e

                )


                time.sleep(2)



        return None



    # =====================================================
    # WALLET
    # =====================================================

    def get_wallet_balance(self):


        response = self._safe_call(

            self.session.get_wallet_balance,

            accountType="UNIFIED"

        )


        if not response:

            return None



        try:


            account = (

                response
                ["result"]
                ["list"][0]

            )


            return {


                "equity":

                    float(

                        account
                        ["totalEquity"]

                    ),


                "available":

                    float(

                        account
                        ["totalAvailableBalance"]

                    )

            }



        except Exception:


            return None



    # =====================================================
    # POSITION
    # =====================================================

    def get_position(self, symbol):


        response = self._safe_call(

            self.session.get_positions,

            category="linear",

            symbol=symbol

        )


        if not response:

            return None



        try:


            pos = (

                response
                ["result"]
                ["list"][0]

            )


            size = float(

                pos["size"]

            )


            if size <= 0:

                return None



            return {


                "side":

                    pos["side"],


                "size":

                    size,


                "entry_price":

                    float(

                        pos["avgPrice"]

                    ),


                "pnl":

                    float(

                        pos["unrealisedPnl"]

                    )

            }



        except Exception:


            return None



    # =====================================================
    # PRICE
    # =====================================================

    def get_price(self, symbol):


        response = self._safe_call(

            self.session.get_tickers,

            category="linear",

            symbol=symbol

        )


        if not response:

            return None



        return float(

            response
            ["result"]
            ["list"][0]
            ["lastPrice"]

        )



    # =====================================================
    # CREATE ORDER
    # =====================================================

    def create_order(

        self,

        symbol,

        side,

        qty,

        tp=None,

        sl=None,

        reduce_only=False

    ):


        params = {


            "category":

                "linear",


            "symbol":

                symbol,


            "side":

                side,


            "orderType":

                "Market",


            "qty":

                str(qty),


        }



        if reduce_only:


            params["reduceOnly"] = True



        if tp:


            params["takeProfit"] = str(tp)



        if sl:


            params["stopLoss"] = str(sl)



        print(

            "[ORDER]",

            params

        )



        return self._safe_call(

            self.session.place_order,

            **params

        )



    # =====================================================
    # CANCEL
    # =====================================================

    def cancel_all_orders(self, symbol):


        return self._safe_call(

            self.session.cancel_all_orders,

            category="linear",

            symbol=symbol

        )



    # =====================================================
    # ORDER STATUS
    # =====================================================

    def get_order_history(self, symbol):


        return self._safe_call(

            self.session.get_order_history,

            category="linear",

            symbol=symbol

        )
