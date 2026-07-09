import pandas as pd
import numpy as np




def calculate_supertrend(
    df,
    period=10,
    multiplier=3
):


    if len(df) < period + 2:

        return None



    high = df["high"]

    low = df["low"]

    close = df["close"]



    tr = pd.concat(

        [

            high-low,

            abs(high-close.shift()),

            abs(low-close.shift())

        ],

        axis=1

    ).max(axis=1)



    atr = (
        tr.rolling(period)
        .mean()
    )



    hl2 = (
        high+low
    )/2



    upper = (
        hl2
        +
        multiplier
        *
        atr
    )


    lower = (
        hl2
        -
        multiplier
        *
        atr
    )



    trend = True



    if close.iloc[-1] > upper.iloc[-2]:

        trend = True


    elif close.iloc[-1] < lower.iloc[-2]:

        trend = False



    return trend
