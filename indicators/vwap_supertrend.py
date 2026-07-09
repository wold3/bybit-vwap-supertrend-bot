from collections import deque





class VWAP:



    def __init__(self, max_length=500):


        self.prices = deque(

            maxlen=max_length

        )


        self.volumes = deque(

            maxlen=max_length

        )



        self.vwap = 0



        print(
            "[VWAP INIT]"
        )







    # =============================
    # UPDATE
    # =============================


    def update(
            self,
            price,
            volume
    ):


        try:


            price = float(price)

            volume = float(volume)





            self.prices.append(
                price
            )


            self.volumes.append(
                volume
            )





            total_volume = sum(

                self.volumes

            )





            if total_volume <= 0:


                return price






            total_value = sum(

                p * v

                for p, v

                in zip(

                    self.prices,

                    self.volumes

                )

            )






            self.vwap = (

                total_value

                /

                total_volume

            )



            return self.vwap






        except Exception as e:


            print(
                "[VWAP ERROR]",
                e
            )


            return 0







    def value(self):


        return self.vwap








vwap = VWAP()







# =================================
# Strategy 호환 함수
# =================================


def calculate_vwap(candle):


    return vwap.update(

        candle["close"],

        candle["volume"]

    )
