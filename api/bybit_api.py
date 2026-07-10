import time


from pybit.unified_trading import HTTP


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_TESTNET,
    BYBIT_DEMO,
    CATEGORY,
    DEFAULT_SYMBOL,
)



class BybitAPI:



    def __init__(self):


        self.session = HTTP(

            testnet=BYBIT_TESTNET,

            demo=BYBIT_DEMO,

            api_key=BYBIT_API_KEY,

            api_secret=BYBIT_API_SECRET,

            recv_window=10000

        )



    # =====================================
    # SAFE CALL
    # =====================================

    def safe_call(

        self,

        func,

        **kwargs

    ):



        for retry in range(3):


            try:


                response = func(

                    **kwargs

                )



                if response.get(

                    "retCode"

                ) == 0:


                    return response



                print(

                    "[API ERROR]",

                    response

                )



                return None



            except Exception as e:



                print(

                    "[API RETRY]",

                    retry,

                    e

                )


                time.sleep(2)



        return None
