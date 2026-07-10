from config import (
    ACCOUNT_TYPE,
    CATEGORY,
)


from api.bybit_client import (
    bybit_client
)





class BybitWallet:



    def __init__(self):


        self.account_type = ACCOUNT_TYPE


        print("==============================")
        print("[WALLET INIT]")
        print("ACCOUNT :", self.account_type)
        print("==============================")







    # =====================================================
    # GET BALANCE
    # =====================================================

    def get_balance(self):


        try:


            params = {


                "accountType":

                    self.account_type


            }




            result = bybit_client.get(

                "/v5/account/wallet-balance",

                params

            )





            if not result:


                return None






            if result.get(
                "retCode"
            ) != 0:



                print(
                    "[WALLET ERROR]",
                    result
                )


                return None





            return result["result"]






        except Exception as e:


            print(
                "[WALLET EXCEPTION]",
                e
            )


            return None







    # =====================================================
    # EQUITY
    # =====================================================

    def get_equity(self):


        try:


            data = self.get_balance()



            if data is None:


                return 0





            account = data["list"][0]





            equity = float(

                account.get(

                    "totalEquity",

                    0

                )

            )





            return equity






        except Exception as e:


            print(
                "[EQUITY ERROR]",
                e
            )


            return 0







    # =====================================================
    # AVAILABLE BALANCE
    # =====================================================

    def get_available_balance(self):


        try:


            data = self.get_balance()



            if data is None:


                return 0





            account = data["list"][0]





            return float(

                account.get(

                    "totalAvailableBalance",

                    0

                )

            )





        except Exception as e:


            print(
                "[AVAILABLE BALANCE ERROR]",
                e
            )


            return 0







    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "account":

                self.account_type,


            "equity":

                self.get_equity(),


            "available":

                self.get_available_balance(),


        }





wallet = BybitWallet()
