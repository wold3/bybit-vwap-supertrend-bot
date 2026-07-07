# =====================================
# CLOSE POSITION
# =====================================

def close_position(
    self,
    symbol,
    side,
    qty
):


    """
    현재 포지션 강제 종료

    Buy 포지션 → Sell reduceOnly
    Sell 포지션 → Buy reduceOnly
    """



    if side.lower() == "buy":


        close_side = "Sell"


    else:


        close_side = "Buy"




    endpoint = (

        "/v5/order/create"

    )


    url = (

        self.base_url

        +

        endpoint

    )



    timestamp = str(

        int(

            time.time()

            *

            1000

        )

    )



    body = {


        "category":

            "linear",


        "symbol":

            symbol,


        "side":

            close_side,


        "orderType":

            "Market",


        "qty":

            str(qty),


        "reduceOnly":

            True

    }





    headers = {


        "X-BAPI-API-KEY":

            self.api_key,


        "X-BAPI-SIGN":

            self._sign(

                timestamp,

                body

            ),


        "X-BAPI-TIMESTAMP":

            timestamp,


        "X-BAPI-RECV-WINDOW":

            "5000"

    }




    try:


        response = requests.post(

            url,

            json=body,

            headers=headers,

            timeout=5

        )



        result = response.json()



        print(

            "CLOSE POSITION RESULT",

            result

        )



        return result




    except Exception as e:


        print(

            "CLOSE POSITION ERROR",

            e

        )


        return None
