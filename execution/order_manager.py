import time
import hmac
import hashlib
import json
import requests


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_BASE_URL,
    DEFAULT_SYMBOL,
    LIVE_TRADING
)



class OrderManager:


    def __init__(self):

        self.base = BYBIT_BASE_URL
        self.symbol = DEFAULT_SYMBOL

        print("==============================")
        print("[ORDER MANAGER INIT]")
        print("BASE :", self.base)
        print("LIVE :", LIVE_TRADING)
        print("SYMBOL :", self.symbol)
        print("==============================")




    # =================================
    # SIGN
    # =================================

    def sign(
        self,
        timestamp,
        body
    ):


        recv_window = "5000"


        origin = (
            timestamp
            +
            BYBIT_API_KEY
            +
            recv_window
            +
            body
        )


        return hmac.new(
            BYBIT_API_SECRET.encode(),
            origin.encode(),
            hashlib.sha256
        ).hexdigest()





    # =================================
    # CREATE ORDER
    # =================================

    def create_order(
            self,
            side,
            qty,
            take_profit=None,
            stop_loss=None
    ):


        url = (
            self.base
            +
            "/v5/order/create"
        )



        data = {

            "category":
                "linear",

            "symbol":
                self.symbol,

            "side":
                side,

            "positionIdx":
                0,

            "orderType":
                "Market",

            "qty":
                str(qty)

        }



        # ==========================
        # TP / SL 자동 설정
        # ==========================

        if take_profit:


            data["takeProfit"] = str(
                take_profit
            )



        if stop_loss:


            data["stopLoss"] = str(
                stop_loss
            )





        body = json.dumps(
            data
        )



        print("==============================")
        print("[ORDER REQUEST]")
        print(url)
        print(data)
        print("==============================")





        # ==========================
        # DEMO MODE
        # ==========================

        if not LIVE_TRADING:


            print(
                "[DEMO ORDER MODE]"
            )





        timestamp = str(
            int(
                time.time()*1000
            )
        )



        signature = self.sign(

            timestamp,

            body

        )



        headers = {


            "X-BAPI-API-KEY":
                BYBIT_API_KEY,


            "X-BAPI-SIGN":
                signature,


            "X-BAPI-TIMESTAMP":
                timestamp,


            "X-BAPI-RECV-WINDOW":
                "5000",


            "Content-Type":
                "application/json"

        }





        try:


            r = requests.post(

                url,

                headers=headers,

                data=body,

                timeout=10

            )


            result = r.json()



            print(
                "[ORDER RESPONSE]",
                result
            )



            return result



        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )


            return None







    # =================================
    # MARKET CLOSE
    # =================================

    def close_position(
            self,
            side,
            qty
    ):


        close_side = (
            "Sell"
            if side=="Buy"
            else
            "Buy"
        )



        return self.create_order(

            side=close_side,

            qty=qty

        )






order_manager = OrderManager()
