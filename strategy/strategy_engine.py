import time


from execution.order_manager import order_manager



class StrategyEngine:


    def __init__(self):

        self.position = None

        self.last_signal = None

        self.cooldown = 30

        self.last_order_time = 0


        print("==============================")
        print("[STRATEGY ENGINE INIT]")
        print("==============================")




    # ==================================
    # SIGNAL CHECK
    # ==================================

    def process_signal(
        self,
        signal
    ):


        if signal is None:

            return



        signal = signal.upper()



        print(
            "[STRATEGY SIGNAL]",
            signal
        )



        # 중복 신호 방지

        if signal == self.last_signal:

            return




        # 주문 간격 제한

        now = time.time()


        if now - self.last_order_time < self.cooldown:

            print(
                "[ORDER COOLDOWN]"
            )

            return




        # ==================================
        # BUY
        # ==================================

        if signal == "BUY":


            if self.position is not None:


                print(
                    "[SKIP] POSITION EXISTS"
                )


                return



            result = order_manager.create_order(

                side="Buy",

                qty="0.001",

                order_type="Market"

            )


            print(
                "[BUY ORDER RESULT]",
                result
            )



            if result.get("retCode") == 0:


                self.position = "LONG"

                self.last_signal = signal

                self.last_order_time = now






        # ==================================
        # SELL
        # ==================================

        elif signal == "SELL":



            if self.position != "LONG":


                print(
                    "[SKIP] NO LONG POSITION"
                )


                return



            result = order_manager.create_order(

                side="Sell",

                qty="0.001",

                order_type="Market"

            )



            print(
                "[SELL ORDER RESULT]",
                result
            )



            if result.get("retCode") == 0:


                self.position = None

                self.last_signal = signal

                self.last_order_time = now







    # ==================================
    # CANDLE INPUT
    # ==================================

    def on_candle(
        self,
        candle
    ):


        """
        candle 예:

        {
            open,
            high,
            low,
            close,
            volume
        }

        """


        signal = self.calculate_signal(
            candle
        )


        self.process_signal(
            signal
        )






    # ==================================
    # VWAP + SUPERTREND PLACEHOLDER
    # ==================================

    def calculate_signal(
        self,
        candle
    ):


        """
        실제 VWAP / Supertrend 계산 위치

        반환:
            BUY
            SELL
            None

        """


        close = candle.get(
            "close"
        )


        if close is None:

            return None



        # ==========================
        # 테스트용
        # ==========================
        #
        # 실제 적용 시:
        #
        # vwap_signal
        # supertrend_signal
        #
        # 조합


        return None





strategy_engine = StrategyEngine()
