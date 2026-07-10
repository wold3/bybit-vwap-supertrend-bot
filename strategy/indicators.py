import numpy as np


class Indicators:


    # =====================================================
    # VWAP
    # =====================================================

    def vwap(
        self,
        highs,
        lows,
        closes,
        volumes
    ):

        if len(closes) == 0:
            return None


        typical_prices = (

            (
                np.array(highs)
                +
                np.array(lows)
                +
                np.array(closes)
            )
            /
            3

        )


        volumes = np.array(volumes)


        volume_sum = np.sum(volumes)


        if volume_sum == 0:

            return None



        return float(

            np.sum(
                typical_prices * volumes
            )
            /
            volume_sum

        )



    # =====================================================
    # TRUE RANGE
    # =====================================================

    def true_range(
        self,
        highs,
        lows,
        closes
    ):


        tr = []


        for i in range(len(closes)):


            if i == 0:

                value = (

                    highs[i]
                    -
                    lows[i]

                )


            else:

                prev_close = closes[i-1]


                value = max(

                    highs[i] - lows[i],

                    abs(
                        highs[i]
                        -
                        prev_close
                    ),

                    abs(
                        lows[i]
                        -
                        prev_close
                    )

                )


            tr.append(value)



        return tr



    # =====================================================
    # ATR - WILDER
    # =====================================================

    def atr(
        self,
        highs,
        lows,
        closes,
        period=14
    ):


        if len(closes) < period + 1:

            return None



        tr = self.true_range(

            highs,
            lows,
            closes

        )



        atr = np.mean(

            tr[:period]

        )



        for value in tr[period:]:


            atr = (

                (atr * (period - 1))
                +
                value

            ) / period



        return float(atr)



    # =====================================================
    # SUPERTREND
    # =====================================================

    def supertrend(
        self,
        highs,
        lows,
        closes,
        period=10,
        multiplier=3
    ):


        if len(closes) < period + 2:

            return None



        tr = self.true_range(

            highs,
            lows,
            closes

        )


        atr_values = []

        atr = np.mean(

            tr[:period]

        )


        atr_values.append(atr)



        for value in tr[period:]:


            atr = (

                (atr * (period - 1))
                +
                value

            ) / period


            atr_values.append(atr)



        final_upper = None

        final_lower = None


        trend = 1


        previous_trend = trend



        for i in range(
            period,
            len(closes)
        ):


            hl2 = (

                highs[i]
                +
                lows[i]

            ) / 2



            atr_value = atr_values[
                i - period
            ]



            basic_upper = (

                hl2
                +
                multiplier
                *
                atr_value

            )


            basic_lower = (

                hl2
                -
                multiplier
                *
                atr_value

            )



            if final_upper is None:


                final_upper = basic_upper

                final_lower = basic_lower



            else:


                if (

                    basic_upper < final_upper

                    or

                    closes[i-1] > final_upper

                ):

                    final_upper = basic_upper



                if (

                    basic_lower > final_lower

                    or

                    closes[i-1] < final_lower

                ):

                    final_lower = basic_lower




            if closes[i] > final_upper:


                trend = 1



            elif closes[i] < final_lower:


                trend = -1



            else:


                trend = previous_trend



            previous_trend = trend




        changed = (

            trend != previous_trend

        )



        return {


            "trend":

                "UP"
                if trend == 1
                else "DOWN",


            "direction":

                trend,


            "value":

                final_lower
                if trend == 1
                else final_upper,


            "atr":

                float(atr_value),


            "changed":

                changed

        }



    # =====================================================
    # TREND STRENGTH
    # =====================================================

    def trend_strength(
        self,
        prices
    ):


        if len(prices) < 30:

            return 0.0



        short = np.mean(

            prices[-10:]

        )


        long = np.mean(

            prices[-30:]

        )



        if long == 0:

            return 0.0



        return abs(

            short - long

        ) / long




# singleton

indicators = Indicators()
