import time
import json
import hmac
import hashlib
import requests


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_BASE_URL,
    DEFAULT_SYMBOL
)



class PositionManager:


    def __init__(self):


        self.base = BYBIT_BASE_URL

        self.symbol = DEFAULT_SYMBOL


        self.current = {

            "side": None,

            "size": 0

        }



        print(
            "[POSITION MANAGER READY]"
        )





    # ============================
    # SIGN
    # ============================

    def _sign(
            self,
            timestamp,
            query
    ):


        recv = "5000"


        origin = (

            timestamp

            +

            BYBIT_API_KEY

            +

            recv

            +

            query

        )



        return hmac.new(

            BYBIT_API_SECRET.encode(),

            origin.encode(),

            hashlib.sha256

        ).hexdigest()





    # ============================
    # GET POSITION
    # ============================


    def sync(self):


        endpoint = (
            "/v5/position/list"
        )



        params = (

            "category=linear"

            "&symbol="

            +

            self.symbol

        )



        timestamp = str(

            int(

                time.time()*1000

            )

        )



        sign = self._sign(

            timestamp,

            params

        )



        headers = {


            "X-BAPI-API-KEY":

                BYBIT_API_KEY,


            "X-BAPI-SIGN":

                sign,


            "X-BAPI-TIMESTAMP":

                timestamp,


            "X-BAPI-RECV-WINDOW":

                "5000"

        }




        try:


            r = requests.get(

                self.base + endpoint,

                params={

                    "category":

                    "linear",

                    "symbol":

                    self.symbol

                },

                headers=headers,

                timeout=10

            )



            data = r.json()



            print(

                "[POSITION RESPONSE]",

                data

            )



            if data.get(
                "retCode"
            ) != 0:


                return None




            rows = data["result"]["list"]



            if rows:



                pos = rows[0]



                size = float(

                    pos.get(

                        "size",

                        0

                    )

                )



                side = pos.get(
                    "side"
                )



                if size == 0:


                    side = None




                self.current = {

                    "side":

                    side,


                    "size":

                    size

                }




            return self.current




        except Exception as e:


            print(

                "[POSITION ERROR]",

                e

            )


            return None






    # ============================
    # CHECK
    # ============================


    def has_position(self):


        return (

            self.current["size"]

            !=

            0

        )





    def side(self):


        return self.current["side"]




    def size(self):


        return self.current["size"]






position_manager = PositionManager()
