# services/private_ws.py


import threading
import time


from pybit.unified_trading import WebSocket


from config import (
    BYBIT_TESTNET,
    CATEGORY,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
)



from portfolio.position_manager import (
    position_manager
)




class PrivateWS:



    def __init__(self):


        self.ws = None


        self.running = False


        self.thread = None


        self.last_message_time = 0





    # =====================================
    # START
    # =====================================

    def start(self):


        if self.running:


            return



        self.running = True



        self.thread = threading.Thread(

            target=self.run,

            daemon=True

        )



        self.thread.start()



        print(

            "[PRIVATE WS START]"

        )






    # =====================================
    # CONNECT LOOP
    # =====================================

    def run(self):


        while self.running:



            try:



                self.connect()



            except Exception as e:



                print(

                    "[PRIVATE WS ERROR]",

                    e

                )



            time.sleep(5)







    # =====================================
    # CONNECT
    # =====================================

    def connect(self):



        self.ws = WebSocket(

            testnet=BYBIT_TESTNET,

            channel_type="private",

            api_key=BYBIT_API_KEY,

            api_secret=BYBIT_API_SECRET

        )



        self.ws.order_stream(

            callback=self.on_order

        )


        self.ws.position_stream(

            callback=self.on_position

        )



        print(

            "[PRIVATE WS CONNECTED]"

        )



        while self.running:


            self.last_message_time = time.time()


            time.sleep(1)






    # =====================================
    # ORDER EVENT
    # =====================================

    def on_order(
        self,
        message
    ):



        try:



            print(

                "[ORDER UPDATE]",

                message

            )



            data = message.get(

                "data",

                []

            )



            for order in data:



                status = order.get(

                    "orderStatus"

                )



                if status == "Filled":



                    print(

                        "[ORDER FILLED]",

                        order

                    )



                    position_manager.sync()






        except Exception as e:



            print(

                "[ORDER WS ERROR]",

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



            print(

                "[POSITION UPDATE]",

                message

            )



            position_manager.sync()




        except Exception as e:



            print(

                "[POSITION WS ERROR]",

                e

            )






    # =====================================
    # HEALTH
    # =====================================

    def heartbeat(self):


        return (

            time.time()

            -

            self.last_message_time

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



        except Exception:


            pass






private_ws = PrivateWS()
