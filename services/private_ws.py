import time
import threading

from pybit.unified_trading import WebSocket



class PrivateWebSocket:


    def __init__(

        self,

        api_key,

        api_secret,

        position_manager=None

    ):


        self.position_manager = (
            position_manager
        )


        self.running = False


        self.ws = WebSocket(

            testnet=True,

            channel_type="private",

            api_key=api_key,

            api_secret=api_secret

        )


        self.last_message_time = 0



    # =====================================================
    # START
    # =====================================================

    def start(self):


        if self.running:

            return


        self.running = True



        self.ws.order_stream(

            callback=self.order_callback

        )


        self.ws.position_stream(

            callback=self.position_callback

        )


        self.ws.wallet_stream(

            callback=self.wallet_callback

        )



        thread = threading.Thread(

            target=self.monitor

        )


        thread.daemon = True

        thread.start()



        print(

            "[PRIVATE WS STARTED]"

        )



    # =====================================================
    # ORDER EVENT
    # =====================================================

    def order_callback(self, message):


        self.last_message_time = time.time()



        data = message.get(

            "data",

            []

        )


        for order in data:


            status = order.get(

                "orderStatus"

            )


            print(

                "[ORDER EVENT]",

                status

            )


            if status == "Filled":


                print(

                    "[FILLED]",

                    order.get("orderId")

                )



    # =====================================================
    # POSITION EVENT
    # =====================================================

    def position_callback(self,message):


        self.last_message_time = time.time()



        print(

            "[POSITION UPDATE]"

        )


        if self.position_manager:


            self.position_manager.sync()



    # =====================================================
    # WALLET EVENT
    # =====================================================

    def wallet_callback(self,message):


        self.last_message_time = time.time()



        print(

            "[WALLET UPDATE]"

        )



    # =====================================================
    # MONITOR
    # =====================================================

    def monitor(self):


        while self.running:


            time.sleep(10)



            if (

                time.time()
                -
                self.last_message_time

                >

                60

            ):


                print(

                    "[WS WARNING] NO MESSAGE"

                )



    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        self.running = False


        print(

            "[PRIVATE WS STOP]"

        )
