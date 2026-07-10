import time
import threading


from api.bybit_api import bybit_api

from risk.risk_manager import risk_manager

from strategy.vwap_supertrend_strategy import (
    vwap_supertrend_strategy
)

from execution.order_manager import (
    order_manager
)

from portfolio.position_manager import (
    position_manager
)

from services.private_ws import (
    private_ws
)

from services.watchdog import (
    watchdog
)



class TradingApp:


    def __init__(self):


        self.running = False


        self.market_thread = None



    # =====================================
    # START
    # =====================================

    def start(self):


        print("====================")
        print("[BOT START]")
        print("====================")



        # 1. API TEST

        if not bybit_api.ping():

            raise Exception(
                "BYBIT CONNECTION FAILED"
            )



        # 2. WALLET


        wallet = (

            bybit_api
            .get_wallet_balance()

        )


        if wallet is None:

            raise Exception(
                "WALLET ERROR"
            )



        equity = (

            self.parse_equity(
                wallet
            )

        )



        # 3. POSITION SYNC


        position_manager.sync()



        # 4. RISK INIT


        risk_manager.initialize(

            equity

        )



        # 5. LEVERAGE


        bybit_api.set_leverage()



        # 6. PRIVATE WS


        private_ws.start()



        # 7. WATCHDOG


        watchdog.start()



        # 8. MARKET DATA


        self.start_market_stream()



        self.running = True



        print(

            "[BOT READY]"

        )



    # =====================================
    # MARKET EVENT
    # =====================================

    def on_candle(
        self,
        candles
    ):



        if not self.running:

            return



        signal = (

            vwap_supertrend_strategy
            .analyze(
                candles
            )

        )



        if signal is None:

            return



        print(

            "[SIGNAL]",

            signal

        )



        # EXIT

        if signal["type"] == "EXIT":


            order_manager.close_position()



            return



        # ENTRY


        if not risk_manager.can_trade():

            print(
                "[BLOCKED BY RISK]"
            )

            return



        order_manager.execute(

            signal

        )



    # =====================================
    # MARKET STREAM
    # =====================================

    def start_market_stream(self):


        def run():


            while True:


                candles = (
                    bybit_api
                    .get_kline()
                )


                if candles:


                    self.on_candle(
                        candles
                    )


                time.sleep(60)



        self.market_thread = threading.Thread(

            target=run

        )


        self.market_thread.daemon = True


        self.market_thread.start()



    # =====================================
    # EQUITY PARSER
    # =====================================

    def parse_equity(
        self,
        wallet
    ):


        try:


            return float(

                wallet
                ["result"]
                ["list"][0]
                ["totalEquity"]

            )


        except:


            return 0



    # =====================================
    # STOP
    # =====================================

    def stop(self):


        print(
            "[BOT STOP]"
        )


        self.running = False



        try:

            private_ws.stop()

            watchdog.stop()

        except:

            pass
