import threading
import time



from pybit.unified_trading import WebSocket



from config import (

    BYBIT_TESTNET,

    BYBIT_DEMO,

    CATEGORY,

    DEFAULT_SYMBOL,

    BYBIT_API_KEY,

    BYBIT_API_SECRET,

)



from execution.position_manager import position_manager





# ==========================================
# PRIVATE WS MANAGER
# ==========================================

class PrivateWS:



    def __init__(self):


        self.ws = None


        self.running = False


        self.thread = None



        print("==============================")
        print("[PRIVATE WS INIT]")
        print("CATEGORY :", CATEGORY)
        print("==============================")





    # ======================================
    # POSITION CALLBACK
    # ======================================

    def position_callback(self, message):


        try:


            data = message.get(

                "data",

                []

            )



            if not data:


                return





            position = data[0]



            symbol = position.get(

                "symbol"

            )



            if symbol != DEFAULT_SYMBOL:


                return





            side = position.get(

                "side"

            )



            size = float(

                position.get(

                    "size",

                    0

                )

            )



            entry = float(

                position.get(

                    "avgPrice",

                    0

                )

            )





            if size > 0:



                position_manager.update_position(


                    side,


                    size,


                    entry


                )



            else:


                position_manager.clear()





        except Exception as e:


            print(
                "[PRIVATE POSITION ERROR]",
                e
            )





    # ======================================
    # ORDER CALLBACK
    # ======================================

    def order_callback(self, message):


        try:


            data = message.get(

                "data",

                []

            )



            if not data:


                return





            order = data[0]



            status = order.get(

                "orderStatus"

            )



            side = order.get(

                "side"

            )



            print("==============================")
            print("[ORDER UPDATE]")
            print("SIDE :", side)
            print("STATUS :", status)
            print("==============================")





        except Exception as e:


            print(
                "[ORDER CALLBACK ERROR]",
                e
            )





    # ======================================
    # CONNECT
    # ======================================

    def connect(self):


        self.ws = WebSocket(


            testnet=BYBIT_TESTNET,


            demo=BYBIT_DEMO,


            channel_type="private",


            api_key=BYBIT_API_KEY,


            api_secret=BYBIT_API_SECRET


        )





        self.ws.position_stream(

            callback=self.position_callback

        )



        self.ws.order_stream(

            callback=self.order_callback

        )



        print(
            "[PRIVATE WS STARTED]"
        )





        while self.running:


            time.sleep(1)





    # ======================================
    # START LOOP
    # ======================================

    def start(self):


        self.running = True



        while self.running:


            try:


                self.connect()



            except Exception as e:


                print(
                    "[PRIVATE WS ERROR]",
                    e
                )


                print(
                    "[PRIVATE WS RECONNECT] 5 SEC"
                )



                time.sleep(5)





    # ======================================
    # THREAD
    # ======================================

    def run_thread(self):


        self.thread = threading.Thread(


            target=self.start,


            daemon=True

        )


        self.thread.start()





    # ======================================
    # STOP
    # ======================================

    def stop(self):


        self.running = False



        print(
            "[PRIVATE WS STOPPED]"
        )





# ==========================================
# SINGLETON
# ==========================================

private_ws = PrivateWS()
