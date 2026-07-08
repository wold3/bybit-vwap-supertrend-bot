import threading
import time


from watchdog.watchdog import watchdog

from market.candle_builder import candle_builder



class WSClient:
    """
    Public WebSocket Client

    역할:
    - Bybit Tick 수신
    - Candle Builder 전달
    - 최신 Candle 제공
    """



    def __init__(self):

        self.running = False

        self.connected = False

        self.thread = None


        self.latest_candle = None

        self.last_update = 0




    # =====================================
    # START
    # =====================================

    def start(self):


        if self.running:

            return



        self.running = True



        self.thread = threading.Thread(

            target=self._run,

            daemon=True

        )


        self.thread.start()



        print("[WS] started")





    # =====================================
    # LOOP
    # =====================================

    def _run(self):


        self.connected = True



        while self.running:


            try:


                watchdog.heartbeat()



                # =================================
                # 실제 Bybit WS 연결 위치
                # =================================
                #
                # tick 수신 예:
                #
                # {
                #   symbol:"BTCUSDT",
                #   price:109600,
                #   volume:0.25
                # }
                #
                #
                # self.on_tick(data)
                #



                time.sleep(1)



            except Exception as e:


                print(

                    "[WS ERROR]",

                    e

                )


                time.sleep(5)



        self.connected = False





    # =====================================
    # TICK RECEIVER
    # =====================================

    def on_tick(
        self,
        data
    ):


        symbol = data["symbol"]

        price = data["price"]

        volume = data.get(

            "volume",

            0

        )



        candle_builder.update(

            symbol,

            price,

            volume

        )



        if candle_builder.is_closed(

            symbol

        ):


            candle = candle_builder.close_candle(

                symbol

            )


            self.latest_candle = candle


            self.last_update = time.time()





    # =====================================
    # STOP
    # =====================================

    def stop(self):


        self.running = False

        self.connected = False


        print("[WS] stopped")





    # =====================================
    # GET CANDLE
    # =====================================

    def get_latest_candle(
        self
    ):


        candle = self.latest_candle


        self.latest_candle = None


        return candle





    # =====================================
    # STATUS
    # =====================================

    def is_connected(
        self
    ):

        return self.connected





    def status(
        self
    ):


        return {


            "running":

                self.running,


            "connected":

                self.connected,


            "has_candle":

                self.latest_candle is not None,


            "last_update":

                self.last_update

        }





# singleton

ws_client = WSClient()
