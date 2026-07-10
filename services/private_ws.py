# services/private_ws.py


import threading
import time


from pybit.unified_trading import WebSocket


from config import (

    BYBIT_TESTNET,

    CATEGORY

)


from portfolio.position_manager import (

    position_manager

)



class PrivateWS:



    def __init__(self):


        self.ws = None


        self.running = False


        self.thread = None




    # =====================================
    # START
    # =====================================

    def start(self):


        if self.running:

            return



        print(
            "[PRIVATE WS START]"
        )


        self.running = True



        self.ws = WebSocket(

            testnet=BYBIT_TESTNET,

            channel_type="private"

        )



        self.subscribe()



        self.thread = threading.Thread(

            target=self.keep_alive,

            daemon=True

        )


        self.thread.start()




    # =====================================
    # SUBSCRIBE
    # =====================================

    def subscribe(self):


        try:


            self.ws.position_stream(

                callback=self.on_position

            )


            self.ws.order_stream(

                callback=self.on_order

            )


            self.ws.wallet_stream(

                callback=self.on_wallet

            )



            print(

                "[PRIVATE WS SUBSCRIBED]"

            )



        except Exception as e:


            print(

                "[WS SUB ERROR]",

                e

            )




    # =====================================
    # POSITION EVENT
    # =====================================

    def on_position(
        self,
        message
    ):


        try:


            data = (

                message
                .get("data")

            )


            if not data:

                return



            pos = data[0]



            size = float(

                pos.get(
                    "size",
                    0
                )

            )



            if size <= 0:


                position_manager.clear()



            else:


                position_manager.update({

                    "symbol":

                        pos["symbol"],


                    "side":

                        pos["side"],


                    "size":

                        size,


                    "entry_price":

                        float(
                            pos["entryPrice"]
                        ),


                    "unrealized_pnl":

                        float(
                            pos["unrealisedPnl"]
                        )

                })



            print(

                "[POSITION UPDATE]",

                position_manager.status()

            )



        except Exception as e:


            print(

                "[POSITION EVENT ERROR]",

                e

            )




    # =====================================
    # ORDER EVENT
    # =====================================

    def on_order(
        self,
        message
    ):


        try:


            print(

                "[ORDER EVENT]",

                message

            )


        except Exception:


            pass




    # =====================================
    # WALLET EVENT
    # =====================================

    def on_wallet(
        self,
        message
    ):


        try:


            print(

                "[WALLET EVENT]",

                message

            )


        except Exception:


            pass




    # =====================================
    # KEEP ALIVE
    # =====================================

    def keep_alive(self):


        while self.running:


            try:


                time.sleep(30)



            except Exception as e:


                print(

                    "[WS ERROR]",

                    e

                )



    # =====================================
    # STOP
    # =====================================

    def stop(self):


        print(

            "[PRIVATE WS STOP]"

        )


        self.running = False



        try:


            if self.ws:


                self.ws.exit()



        except Exception as e:


            print(

                "[WS STOP ERROR]",

                e

            )




private_ws = PrivateWS()
