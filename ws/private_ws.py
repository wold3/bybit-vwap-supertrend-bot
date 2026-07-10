import threading
import time


from pybit.unified_trading import WebSocket


from config import (
    BYBIT_TESTNET,
    BYBIT_DEMO,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    CATEGORY,
)


from execution.position_manager import position_manager
from execution.order_manager import order_manager





# ==========================================
# PRIVATE WS MANAGER
# ==========================================

class PrivateWS:


    def __init__(self):


        self.ws = None


        self.running = False


        self.thread = None



        self.order_data = None

        self.position_data = None

        self.wallet_data = None



        print("==============================")
        print("[PRIVATE WS INIT]")
        print("CATEGORY :", CATEGORY)
        print("==============================")





    # ======================================
    # MESSAGE HANDLER
    # ======================================

    def handle_message(self, message):


        try:


            topic = message.get(
                "topic",
                ""
            )



            # --------------------------
            # ORDER
            # --------------------------

            if topic == "order":


                self.order_data = message



                print(
                    "[ORDER UPDATE]"
                )


                self.sync_order(
                    message
                )





            # --------------------------
            # POSITION
            # --------------------------

            elif topic == "position":


                self.position_data = message



                print(
                    "[POSITION UPDATE]"
                )


                self.sync_position(
                    message
                )





            # --------------------------
            # WALLET
            # --------------------------

            elif topic == "wallet":


                self.wallet_data = message



                print(
                    "[WALLET UPDATE]"
                )





        except Exception as e:


            print(
                "[PRIVATE MESSAGE ERROR]",
                e
            )





    # ======================================
    # POSITION SYNC
    # ======================================

    def sync_position(self, message):


        try:


            data = message.get(
                "data",
                []
            )



            if not data:


                return





            pos = data[0]



            side = pos.get(
                "side",
                ""
            )


            size = float(

                pos.get(
                    "size",
                    0
                )

            )


            entry = float(

                pos.get(
                    "avgPrice",
                    0
                )

            )





            if size > 0 and side:



                position_manager.update_position(

                    side,

                    size,

                    entry

                )



                order_manager.update_position(

                    {

                        "side": side,

                        "size": size

                    }

                )





            else:


                position_manager.clear()



                order_manager.update_position(

                    {

                        "side": None,

                        "size": 0

                    }

                )





        except Exception as e:


            print(
                "[POSITION SYNC ERROR]",
                e
            )





    # ======================================
    # ORDER SYNC
    # ======================================

    def sync_order(self, message):


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



            print(

                "[ORDER STATUS]",

                status,

                side

            )




        except Exception as e:


            print(
                "[ORDER SYNC ERROR]",
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




        self.ws.order_stream(

            callback=self.handle_message

        )


        self.ws.position_stream(

            callback=self.handle_message

        )


        self.ws.wallet_stream(

            callback=self.handle_message

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
                    "[PRIVATE WS RECONNECT] 5 sec"
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





    # ======================================
    # GETTERS
    # ======================================

    def get_position(self):


        return self.position_data




    def get_order(self):


        return self.order_data




    def get_wallet(self):


        return self.wallet_data





# ==========================================
# SINGLETON
# ==========================================

private_ws = PrivateWS()
