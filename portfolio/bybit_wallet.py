from config import (
    ACCOUNT_TYPE,
)

from api.bybit_client import (
    bybit_client,
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

                    self.account_type,


            }




            response = bybit_client.get(

                "/v5/account/wallet-balance",

                params

            )





            if not response:


                return None






            if response.get(
                "retCode"
            ) != 0:


                print(
                    "[WALLET ERROR]",
                    response
                )


                return None






            return response["result"]["list"][0]







        except Exception as e:


            print(

                "[WALLET GET ERROR]",

                e

            )


            return None










    # =====================================================
    # EQUITY
    # =====================================================

    def get_equity(self):


        try:



            account = self.get_balance()



            if not account:


                return 0






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



            account = self.get_balance()



            if not account:


                return 0






            balance = float(

                account.get(

                    "totalAvailableBalance",

                    0

                )

            )





            return balance







        except Exception as e:


            print(

                "[AVAILABLE ERROR]",

                e

            )


            return 0











    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        account = self.get_balance()



        if not account:


            return {}



        return {


            "equity":

                account.get(
                    "totalEquity"
                ),


            "available":

                account.get(
                    "totalAvailableBalance"
                ),


            "wallet":

                account.get(
                    "totalWalletBalance"
                ),


        }











wallet = BybitWallet()
