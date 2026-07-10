import numpy as np
import pandas as pd

from config import (
    VWAP_LENGTH,
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER,
)


# ==================================================
# VWAP + SUPERTREND SIGNAL ENGINE
# ==================================================

class VWAPSupertrend:

    def __init__(self):

        print("==============================")
        print("[SIGNAL INIT]")
        print("VWAP :", VWAP_LENGTH)
        print(
            "SUPERTREND :",
            SUPERTREND_PERIOD,
            SUPERTREND_MULTIPLIER,
        )
        print("==============================")

    # ==================================================
    # VWAP
    # ==================================================

    def calculate_vwap(
        self,
        close,
        volume,
    ):

        close = np.asarray(close, dtype=float)
        volume = np.asarray(volume, dtype=float)

        if volume.sum() == 0:
            return float(close[-1])

        return float((close * volume).sum() / volume.sum())

    # ==================================================
    # SUPERTREND
    # ==================================================

    def calculate_supertrend(
        self,
        high,
        low,
        close,
    ):

        df = pd.DataFrame({
            "high": high,
            "low": low,
            "close": close,
        })

        tr1 = df["high"] - df["low"]

        tr2 = (
            df["high"]
            - df["close"].shift(1)
        ).abs()

        tr3 = (
            df["low"]
            - df["close"].shift(1)
        ).abs()

        tr = pd.concat(
            [tr1, tr2, tr3],
            axis=1
        ).max(axis=1)

        atr = tr.rolling(
            SUPERTREND_PERIOD
        ).mean()

        hl2 = (
            df["high"]
            + df["low"]
        ) / 2

        upper = (
            hl2
            + atr * SUPERTREND_MULTIPLIER
        )

        lower = (
            hl2
            - atr * SUPERTREND_MULTIPLIER
        )

        final_upper = upper.copy()

        final_lower = lower.copy()

        trend = np.ones(len(df))

        # ==============================================
        # FINAL BAND 계산
        # ==============================================

        for i in range(1, len(df)):

            if (
                upper.iloc[i] < final_upper.iloc[i - 1]
                or df["close"].iloc[i - 1] > final_upper.iloc[i - 1]
            ):
                final_upper.iloc[i] = upper.iloc[i]
            else:
                final_upper.iloc[i] = final_upper.iloc[i - 1]

            if (
                lower.iloc[i] > final_lower.iloc[i - 1]
                or df["close"].iloc[i - 1] < final_lower.iloc[i - 1]
            ):
                final_lower.iloc[i] = lower.iloc[i]
            else:
                final_lower.iloc[i] = final_lower.iloc[i - 1]

        # ==============================================
        # TREND 계산
        # ==============================================

        trend[0] = 1

        for i in range(1, len(df)):

            if df["close"].iloc[i] > final_upper.iloc[i - 1]:

                trend[i] = 1

            elif df["close"].iloc[i] < final_lower.iloc[i - 1]:

                trend[i] = -1

            else:

                trend[i] = trend[i - 1]

                if (
                    trend[i] == 1
                    and final_lower.iloc[i] < final_lower.iloc[i - 1]
                ):
                    final_lower.iloc[i] = final_lower.iloc[i - 1]

                elif (
                    trend[i] == -1
                    and final_upper.iloc[i] > final_upper.iloc[i - 1]
                ):
                    final_upper.iloc[i] = final_upper.iloc[i - 1]

        return int(trend[-1])

    # ==================================================
    # SIGNAL
    # ==================================================

    def check_signal(
        self,
        close,
        volume,
        high,
        low,
    ):

        try:

            if len(close) < max(
                VWAP_LENGTH,
                SUPERTREND_PERIOD + 5,
            ):

                print(
                    "[SIGNAL WAIT]",
                    len(close),
                )

                return None

            price = float(close[-1])

            vwap = self.calculate_vwap(
                close,
                volume,
            )

            trend = self.calculate_supertrend(
                high,
                low,
                close,
            )

            print("==============================")
            print("[SIGNAL CHECK]")
            print("PRICE :", round(price, 2))
            print("VWAP :", round(vwap, 2))
            print("SUPERTREND :", trend)
            print("==============================")

            # LONG

            if price > vwap and trend == 1:

                return "Buy"

            # SHORT

            if price < vwap and trend == -1:

                return "Sell"

            return None

        except Exception as e:

            print("[SIGNAL ERROR]", e)

            return None


# ==================================================
# SINGLETON
# ==================================================

signal_engine = VWAPSupertrend()
