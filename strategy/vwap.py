import pandas as pd



def calculate_vwap(df):


    if len(df) == 0:

        return None



    pv = (
        df["close"]
        *
        df["volume"]
    )


    vwap = (
        pv.sum()
        /
        df["volume"].sum()
    )


    return float(vwap)
