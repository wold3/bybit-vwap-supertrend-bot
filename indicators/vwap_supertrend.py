from collections import deque






class SuperTrend:



    def __init__(
            self,
            period=10,
            multiplier=3
    ):


        self.period = period

        self.multiplier = multiplier



        self.highs = deque(
            maxlen=period + 2
        )

        self.lows = deque(
            maxlen=period + 2
        )

        self.closes = deque(
            maxlen=period + 2
        )



        self.direction = True


        self.upper_band = None

        self.lower_band = None



        print(
            "[SUPERTREND INIT]"
        )







    # =============================
    # ATR
    # =============================


    def atr(self):


        if len(self.closes) < 2:


            return 0





        trs = []



        for i in range(
            1,
            len(self.closes)
        ):


            high = self.highs[i]


            low = self.lows[i]


            prev_close = self.closes[i-1]



            tr = max(

                high - low,

                abs(
                    high - prev_close
                ),

                abs(
                    low - prev_close
                )

            )


            trs.append(tr)





        if len(trs) == 0:


            return 0





        return sum(trs) / len(trs)







    # =============================
    # UPDATE
    # =============================


    def update(
            self,
            high,
            low,
            close
    ):


        try:


            high = float(high)

            low = float(low)

            close = float(close)





            self.highs.append(high)

            self.lows.append(low)

            self.closes.append(close)






            atr = self.atr()





            if atr == 0:


                return self.direction






            hl2 = (

                high + low

            ) / 2





            basic_upper = (

                hl2

                +

                self.multiplier * atr

            )



            basic_lower = (

                hl2

                -

                self.multiplier * atr

            )






            if self.upper_band is None:


                self.upper_band = basic_upper


                self.lower_band = basic_lower





            else:



                self.upper_band = min(

                    basic_upper,

                    self.upper_band

                )


                self.lower_band = max(

                    basic_lower,

                    self.lower_band

                )







            # 상승 추세

            if close > self.upper_band:


                self.direction = True





            # 하락 추세

            elif close < self.lower_band:


                self.direction = False






            return self.direction






        except Exception as e:


            print(

                "[SUPERTREND ERROR]",

                e

            )



            return self.direction










supertrend = SuperTrend()
