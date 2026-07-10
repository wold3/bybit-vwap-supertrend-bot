import time
import threading

from pybit.unified_trading import WebSocket

from config import (
    BYBIT_TESTNET,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    CATEGORY,
    DEMO,
)



# ==========================================
# BYBIT PRIVATE WEBSOCKET V5
# ==========================================


class PrivateWS:


    def __init__(self):

        self.ws = None

        self.running = False

        self.position = None

        self.orders = None


        print("==============================")
        print("[PRIVATE WS INIT]")
        print("CATEGORY :", CATEGORY)
        print("DEMO :", DEMO)
        print("==============================")





    # ======================================
    # MESSAGE HANDLER
    # ======================================

    def handle_position(self, message):

        self.position = message


        print("[POSITION UPDATE]")
        print(message)





    def handle_order(self, message):

        self.orders = message


        print("[ORDER UPDATE]")
        print(message)






    # ======================================
    # START
    # ======================================

    def start(self):


        if self.running:

            return



        self.running = True




        self.ws = WebSocket(

            testnet=BYBIT_TESTNET,

            demo=DEMO,

            channel_type="private",

            api_key=BYBIT_API_KEY,

            api_secret=BYBIT_API_SECRET

        )





        self.ws.position_stream(

            callback=self.handle_position

        )



        self.ws.order_stream(

            callback=self.handle_order

        )




        print(
            "[PRIVATE WS STARTED]"
        )




        while self.running:

            time.sleep(1)







    # ======================================
    # THREAD
    # ======================================

    def run_thread(self):


        thread = threading.Thread(

            target=self.start,

            daemon=True

        )


        thread.start()






    # ======================================
    # GET POSITION
    # ======================================

    def get_position(self):

        return self.position






    # ======================================
    # GET ORDER
    # ======================================

    def get_orders(self):

        return self.orders






    # ======================================
    # STOP
    # ======================================

    def stop(self):


        self.running = False


        try:

            if self.ws:

                self.ws.exit()

        except:

            pass



        print(
            "[PRIVATE WS STOP]"
        )







# ==========================================
# SINGLETON
# ==========================================

private_ws = PrivateWS()
