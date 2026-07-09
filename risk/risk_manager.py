import time

from portfolio.bybit_wallet import wallet
from position.position_manager import position_manager


class RiskManager:

    def __init__(self):

        self.enabled = True

        # 최대 주문 수량
        self.max_position_size = 0.01

        # 주문 쿨다운
        self.cooldown_seconds = 30

        self.last_order_time = 0


        # ==========================
        # DAILY LOSS
        # ==========================

        self.daily_loss_limit = -100

        self.start_equity = None


        # ==========================
        # LOSS CHECK CONTROL
        # ==========================

        self.last_loss_check = 0

        self.loss_check_interval = 60


        # Demo/Test 보호
        self.demo_mode = True


        print("==============================")
        print("[RISK MANAGER READY]")
        print("==============================")


    # =====================================================
    # INITIALIZE
    # =====================================================

    def initialize(self):

        try:

            equity = wallet.get_equity()

            self.start_equity = float(equity)


            print(
                "[RISK INIT EQUITY]",
                self.start_equity
            )


        except Exception as e:

            print(
                "[RISK INIT ERROR]",
                e
            )


    # =====================================================
    # ORDER CHECK
    # =====================================================

    def allow_order(self, qty):


        if not self.enabled:

            print(
                "[RISK BLOCK] DISABLED"
            )

            return False



        try:

            qty = float(qty)


        except Exception:


            print(
                "[RISK BLOCK] INVALID QTY"
            )

            return False




        if qty <= 0:


            print(
                "[RISK BLOCK] INVALID SIZE"
            )

            return False




        if qty > self.max_position_size:


            print(
                "[RISK BLOCK] MAX SIZE"
            )

            return False




        # ==========================
        # POSITION CHECK
        # ==========================

        try:

            position_manager.sync()


            if position_manager.has_position():


                print(
                    "[RISK BLOCK] POSITION EXISTS"
                )


                return False



        except Exception as e:


            print(
                "[POSITION CHECK ERROR]",
                e
            )





        # ==========================
        # COOLDOWN
        # ==========================

        now = time.time()



        if now - self.last_order_time < self.cooldown_seconds:


            remain = round(

                self.cooldown_seconds
                -
                (now - self.last_order_time),

                1

            )


            print(
                "[RISK BLOCK] COOLDOWN",
                remain,
                "sec"
            )


            return False




        return True




    # =====================================================
    # RECORD ORDER
    # =====================================================

    def record_order(self):

        self.last_order_time = time.time()




    # =====================================================
    # DAILY LOSS CHECK
    # =====================================================

    def check_daily_loss(self):


        if self.start_equity is None:

            return True



        now = time.time()



        # API 과호출 방지

        if (
            now - self.last_loss_check
            <
            self.loss_check_interval
        ):

            return True



        self.last_loss_check = now



        try:


            current = float(
                wallet.get_equity()
            )



            pnl = (
                current
                -
                self.start_equity
            )



            print(
                "[DAILY PNL]",
                round(
                    pnl,
                    2
                )
            )



            if pnl <= self.daily_loss_limit:


                print(
                    "[RISK STOP] DAILY LOSS LIMIT",
                    pnl
                )


                self.enabled = False


                return False




        except Exception as e:


            print(
                "[LOSS CHECK ERROR]",
                e
            )



        return True




    # =====================================================
    # RESET DAILY
    # =====================================================

    def reset_daily(self):


        self.initialize()


        self.last_order_time = 0


        self.last_loss_check = 0


        self.enabled = True



        print(
            "[RISK RESET]"
        )




    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        current_pnl = None



        try:


            if self.start_equity is not None:


                current_pnl = (

                    float(
                        wallet.get_equity()
                    )

                    -

                    self.start_equity

                )



        except Exception:


            pass




        return {


            "enabled":
                self.enabled,


            "max_position":
                self.max_position_size,


            "cooldown":
                self.cooldown_seconds,


            "last_order":
                self.last_order_time,


            "start_equity":
                self.start_equity,


            "daily_loss_limit":
                self.daily_loss_limit,


            "current_pnl":
                current_pnl,


            "loss_check_interval":
                self.loss_check_interval,

        }



risk_manager = RiskManager()
