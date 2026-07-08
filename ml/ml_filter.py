import os
import threading

from dotenv import load_dotenv


load_dotenv()



class MLFilter:
    """
    ML Trade Filter

    기능:
    - ML 사용 여부 관리
    - confidence 기반 거래 승인
    - 모델 연결 준비
    """



    def __init__(self):

        self.lock = threading.Lock()



        self.enabled = (

            os.getenv(
                "USE_ML_FILTER",
                "false"
            ).lower() == "true"

        )



        self.min_confidence = float(

            os.getenv(

                "ML_MIN_CONFIDENCE",

                "0.7"

            )

        )



        self.last_prediction = None





    # =====================================
    # TRADE FILTER
    # =====================================

    def allow_trade(
        self,
        market_data
    ):


        if market_data is None:

            return False



        if not self.enabled:

            return True



        prediction = self.predict(

            market_data

        )



        if prediction is None:

            return False



        confidence = prediction.get(

            "confidence",

            0

        )



        return (

            confidence >= self.min_confidence

        )





    # =====================================
    # PREDICT
    # =====================================

    def predict(
        self,
        market_data
    ):


        """
        실제 ML 모델 연결 위치

        반환 예:

        {
            "signal":"BUY",
            "confidence":0.85
        }

        """



        # TODO:
        # sklearn
        # tensorflow
        # pytorch
        # 모델 연결



        result = {


            "signal":

                "BUY",


            "confidence":

                1.0

        }



        self.last_prediction = result



        return result





    # =====================================
    # ENABLE
    # =====================================

    def enable(
        self
    ):

        with self.lock:

            self.enabled = True





    # =====================================
    # DISABLE
    # =====================================

    def disable(
        self
    ):

        with self.lock:

            self.enabled = False





    # =====================================
    # STATUS
    # =====================================

    def status(
        self
    ):

        with self.lock:

            return {


                "enabled":

                    self.enabled,


                "min_confidence":

                    self.min_confidence,


                "last_prediction":

                    self.last_prediction

            }





# singleton

ml_filter = MLFilter()
