import time
import json
import uuid
import hmac
import hashlib
import requests


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_BASE_URL,
    DEFAULT_SYMBOL
)



class OrderManager:


    def __init__(self):

        self.base = BYBIT_BASE_URL
        self.symbol = DEFAULT_SYMBOL


        print("==============================")
        print("[ORDER MANAGER READY]")
        print("BASE :", self.base)
        print("SYMBOL :", self.symbol)
        print("==============================")





    # ===================================
    # SIGN
    # ===================================

    def _sign(self, timestamp, body):


        recv_window = "5000"


        payload = (

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

            payload.encode(),

            hashlib.sha256

        ).hexdigest()






    # ===================================
    # REQUEST
    # ===================================

    def _request(self, path, data):


        url = self.base + path


        body = json.dumps(
            data,
            separators=(",", ":")
        )


        timestamp = str(
            int(time.time()*1000)
        )



        sign = self._sign(

            timestamp,

            body

        )



        headers = {

            "X-BAPI-API-KEY":
                BYBIT_API_KEY,


            "X-BAPI-SIGN":
                sign,


            "X-BAPI-TIMESTAMP":
                timestamp,


            "X-BAPI-RECV-WINDOW":
                "5000",


            "Content-Type":
                "application/json"

        }





        for retry in range(3):


            try:


                r = requests.post(

                    url,

                    headers=headers,

                    data=body,

                    timeout=10

                )


                result = r.json()



                print(
                    "[BYBIT RESPONSE]",
                    result
                )



                return result




            except Exception as e:


                print(
                    "[ORDER RETRY]",
                    retry + 1,
                    e
                )


                time.sleep(1)



        return None






    # ===================================
    # CREATE MARKET ORDER
    # ===================================

    def create_order(

            self,

            side,

            qty,

            take_profit=None,

            stop_loss=None


    ):



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

                str(qty),



            "orderLinkId":

                "vwap-" + uuid.uuid4().hex[:12]

        }





        if take_profit:


            data["takeProfit"] = str(
                take_profit
            )



        if stop_loss:


            data["stopLoss"] = str(
                stop_loss
            )





        print("==============================")
        print("[ORDER CREATE]")
        print(data)
        print("==============================")



        return self._request(

            "/v5/order/create",

            data

        )






    # ===================================
    # CLOSE POSITION
    # ===================================

    def close_position(

            self,

            side,

            qty


    ):



        close_side = (

            "Sell"

            if side == "Buy"

            else

            "Buy"

        )




        data = {


            "category":

                "linear",


            "symbol":

                self.symbol,


            "side":

                close_side,


            "positionIdx":

                0,


            "orderType":

                "Market",


            "qty":

                str(qty),



            "reduceOnly":

                True,


            "orderLinkId":

                "close-" + uuid.uuid4().hex[:12]

        }




        print(
            "[POSITION CLOSE]"
        )



        return self._request(

            "/v5/order/create",

            data

        )







order_manager = OrderManager()
