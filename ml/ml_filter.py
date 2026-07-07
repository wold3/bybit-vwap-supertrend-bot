import os
import numpy as np

from dotenv import load_dotenv


load_dotenv()



class MLFilter:


    def __init__(self):


        self.enabled = (

            os.getenv(

                "ML_FILTER_ENABLE",

                "true"

            ).lower()

            ==

            "true"

        )


        self.threshold = float(

            os.getenv(

                "ML_THRESHOLD",

                "0.65"

            )

        )





    # =====================================
    # FEATURE 생성
    # =====================================

    def create_features(
        self,
        data
    ):


        close = float(

            data.get(

                "close",

                0

            )

        )


        volume = float(

            data.get(

                "volume",

                0

            )

        )


        vwap = float(

            data.get(

                "vwap",

                close

            )

        )



        trend = data.get(

            "supertrend",

            "DOWN"

        )



        trend_value = 1 if trend == "UP" else 0



        return np.array([


            close,


            volume,


            vwap,


            trend_value


        ])





    # =====================================
    # Predict
    # =====================================

    def predict(
        self,
        data
    ):


        if not self.enabled:


            return 1.0





        features = self.create_features(

            data

        )



        probability = self.simple_model(

            features

        )



        return round(

            probability,

            3

        )





    # =====================================
    # 기본 ML 모델 자리
    # =====================================

    def simple_model(
        self,
        features
    ):


        close = features[0]

        vwap = features[2]

        trend = features[3]



        score = 0.5



        # 가격 위치

        if close > vwap:


            score += 0.2



        else:


            score -= 0.2





        # Supertrend

        if trend == 1:


            score += 0.2



        else:


            score -= 0.2





        # 범위 제한

        score = max(

            0.01,

            min(

                0.99,

                score

            )

        )



        return score





    # =====================================
    # 거래 가능 여부
    # =====================================

    def allow_trade(
        self,
        data
    ):


        probability = self.predict(

            data

        )


        print(

            "ML PROBABILITY",

            probability

        )



        return (

            probability

            >=

            self.threshold

        )





ml_filter = MLFilter()
