import time


class RiskManager:


    def __init__(self):

        print("==============================")
        print("[RISK MANAGER INIT]")
        print("==============================")


        # ==============================
        # EQUITY
        # ==============================

        self.initial_equity = 0.0

        self.current_equity = 0.0

        self.highest_equity = 0.0



        # ==============================
        # LOSS CONTROL
        # ==============================

        self.daily_loss = 0.0

        self.max_daily_loss = 5.0



        # ==============================
        # ORDER CONTROL
        # ==============================

        self.last_order_time = 0

        self.order_cooldown = 60



        # ==============================
        # POSITION CONTROL
        # ==============================

        self.max_position_qty = 0.01



        # ==============================
        # STATUS
        # ==============================

        self.trading_enabled = True

        self.start_time = None




    # ==================================================
    # INITIALIZE
    # ==================================================

    def initialize(self, equity):


        try:


            self.initial_equity = float(equity)

            self.current_equity = float(equity)

            self.highest_equity = float(equity)



            self.daily_loss = 0.0

            self.trading_enabled = True


            self.start_time = time.time()



            print("==============================")
            print("[RISK INITIALIZED]")
            print(
                "EQUITY :",
                self.initial_equity
            )
            print(
                "MAX DAILY LOSS :",
                self.max_daily_loss,
                "%"
            )
            print("==============================")


            return True



        except Exception as e:


            print(
                "[RISK INIT ERROR]",
                e
            )


            return False




    # ==================================================
    # UPDATE EQUITY
    # ==================================================

    def update_equity(self, equity):


        try:


            self.current_equity = float(equity)



            if self.current_equity > self.highest_equity:

                self.highest_equity = self.current_equity



            if self.initial_equity > 0:


                loss = (

                    self.initial_equity
                    -
                    self.current_equity

                )


                self.daily_loss = (

                    loss
                    /
                    self.initial_equity

                ) * 100



            print(
                "[DAILY LOSS]",
                round(
                    self.daily_loss,
                    4
                ),
                "%"
            )



            self.check_daily_loss()



            return self.daily_loss



        except Exception as e:


            print(
                "[EQUITY UPDATE ERROR]",
                e
            )


            return None




    # ==================================================
    # DAILY LOSS LIMIT
    # ==================================================

    def check_daily_loss(self):


        if self.daily_loss >= self.max_daily_loss:


            self.trading_enabled = False


            print("==============================")
            print("[RISK STOP]")
            print(
                "LOSS LIMIT:",
                self.daily_loss,
                "%"
            )
            print("==============================")


            return False



        return True




    # ==================================================
    # ORDER PERMISSION
    # ==================================================

    def order_allowed(self):


        if not self.trading_enabled:


            print(
                "[ORDER BLOCK] DAILY LOSS"
            )


            return False



        now = time.time()



        if now - self.last_order_time < self.order_cooldown:


            remain = (

                self.order_cooldown
                -
                (now - self.last_order_time)

            )


            print(
                "[ORDER COOLDOWN]",
                round(remain,1),
                "sec"
            )


            return False



        return True




    # ==================================================
    # POSITION SIZE CHECK
    # ==================================================

    def check_position_size(self, qty):


        try:


            qty = float(qty)



            if qty > self.max_position_qty:


                print(
                    "[POSITION SIZE BLOCK]",
                    qty
                )


                return False



            return True



        except Exception as e:


            print(
                "[SIZE CHECK ERROR]",
                e
            )


            return False




    # ==================================================
    # UPDATE ORDER TIME
    # ==================================================

    def update_order_time(self):


        self.last_order_time = time.time()


        print(
            "[ORDER TIME UPDATED]"
        )




    # ==================================================
    # POSITION RISK
    # ==================================================

    def calculate_position_size(

        self,

        balance,

        risk_percent,

        stop_loss_percent

    ):


        try:


            risk_amount = (

                float(balance)

                *

                float(risk_percent)

                /

                100

            )


            size = (

                risk_amount

                /

                (

                    float(stop_loss_percent)

                    /

                    100

                )

            )


            return round(
                size,
                6
            )



        except Exception as e:


            print(
                "[POSITION CALC ERROR]",
                e
            )


            return 0




    # ==================================================
    # RESET
    # ==================================================

    def reset_daily(self):


        self.initial_equity = self.current_equity

        self.daily_loss = 0.0

        self.trading_enabled = True


        print(
            "[RISK DAILY RESET]"
        )




    # ==================================================
    # STATUS
    # ==================================================

    def get_status(self):


        return {


            "initial_equity":
                self.initial_equity,


            "current_equity":
                self.current_equity,


            "highest_equity":
                self.highest_equity,


            "daily_loss":
                self.daily_loss,


            "trading_enabled":
                self.trading_enabled,


            "last_order_time":
                self.last_order_time


        }



# ==================================================
# SINGLETON
# ==================================================

risk_manager = RiskManager()
