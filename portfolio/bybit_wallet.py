from config import (
    ACCOUNT_TYPE,
    CATEGORY,
    SETTLE_COIN,
)

from api.bybit_client import bybit_client



class BybitWallet:


    def __init__(self):

        print("==============================")
        print("[WALLET INIT]")
        print("ACCOUNT :", ACCOUNT_TYPE)
        print("CATEGORY :", CATEGORY)
        print("SETTLE :", SETTLE_COIN)
        print("==============================")



    # =====================================================
    # ACCOUNT BALANCE
    # =====================================================

    def get_balance(self):

        params = {

            "accountType": ACCOUNT_TYPE,

        }


        try:

            result = bybit_client.get(

                "/v5/account/wallet-balance",

                params

            )


            print(
                "[BALANCE RESPONSE]",
                result
            )


            return result



        except Exception as e:


            print(
                "[BALANCE ERROR]",
                e
            )


            return None




    # =====================================================
    # EQUITY
    # =====================================================

    def get_equity(self):

        try:

            data = self.get_balance()


            if not data:

                return 0



            if data.get("retCode") != 0:

                print(
                    "[BALANCE API ERROR]",
                    data
                )

                return 0




            account = (

                data
                .get("result", {})
                .get("list", [])

            )


            if not account:

                return 0



            equity = account[0].get(
                "totalEquity",
                0
            )



            return float(equity)




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



            if not data:

                return 0



            account = (

                data
                .get("result", {})
                .get("list", [])

            )


            if not account:

                return 0



            balance = account[0].get(

                "totalAvailableBalance",

                0

            )



            return float(balance)



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

                ACCOUNT_TYPE,


            "equity":

                self.get_equity(),


            "available":

                self.get_available_balance(),


            "settle":

                SETTLE_COIN,

        }





wallet = BybitWallet()
