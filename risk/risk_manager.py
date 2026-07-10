import time


class RiskManager:


    def __init__(self):

        print("==============================")
        print("[RISK MANAGER INIT]")
        print("==============================")


        # 초기 자산
        self.initial_equity = 0.0

        # 현재 자산
        self.current_equity = 0.0


        # 최고 자산
        self.highest_equity = 0.0


        # 손실률
        self.daily_loss = 0.0


        # 최대 일일 손실 %
        self.max_daily_loss = 5.0


        # 거래 가능 여부
        self.trading_enabled = True


        # 초기화 시간
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
                "MAX LOSS :",
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
                "[RISK UPDATE ERROR]",
                e
            )


            return None




    # ==================================================
    # DAILY LOSS CHECK
    # ==================================================

    def check_daily_loss(self):


        if self.daily_loss >= self.max_daily_loss:


            self.trading_enabled = False


            print("==============================")
            print("[RISK STOP]")
            print(
                "DAILY LOSS LIMIT:",
                self.daily_loss,
                "%"
            )
            print("==============================")


            return False



        return True




    # ==================================================
    # TRADE PERMISSION
    # ==================================================

    def allow_trade(self):


        if not self.trading_enabled:


            print(
                "[TRADE BLOCKED] Risk limit"
            )


            return False



        return True




    # ==================================================
    # POSITION SIZE CONTROL
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
                "[SIZE ERROR]",
                e
            )


            return 0



    # ==================================================
    # RESET DAILY
    # ==================================================

    def reset_daily(self):


        self.initial_equity = self.current_equity

        self.daily_loss = 0.0

        self.trading_enabled = True


        print(
            "[RISK RESET]"
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


            "max_daily_loss":
                self.max_daily_loss,


            "trading_enabled":
                self.trading_enabled


        }
