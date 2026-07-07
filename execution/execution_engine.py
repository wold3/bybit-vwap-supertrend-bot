# =====================================
# ACCOUNT EQUITY API
# =====================================

def get_account_equity(
    self
):

    endpoint = (
        "/v5/account/wallet-balance"
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



    params = {

        "accountType":

            "UNIFIED"

    }



    # GET 요청용 sign

    sign_payload = (

        timestamp

        +

        self.api_key

        +

        "5000"

        +

        ""

    )



    signature = hmac.new(

        self.api_secret.encode(),

        sign_payload.encode(),

        hashlib.sha256

    ).hexdigest()



    headers = {


        "X-BAPI-API-KEY":

            self.api_key,


        "X-BAPI-SIGN":

            signature,


        "X-BAPI-TIMESTAMP":

            timestamp,


        "X-BAPI-RECV-WINDOW":

            "5000"

    }



    try:


        response = requests.get(

            url,

            params=params,

            headers=headers,

            timeout=5

        )



        result = response.json()



        if result.get("retCode") != 0:


            print(

                "EQUITY API ERROR",

                result

            )


            return 0





        account_list = (

            result

            .get("result", {})

            .get("list", [])

        )



        if not account_list:


            return 0



        equity = (

            account_list[0]

            .get(

                "totalEquity",

                "0"

            )

        )



        return float(equity)




    except Exception as e:


        print(

            "GET EQUITY ERROR",

            e

        )


        return 0
