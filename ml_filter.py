import numpy as np


class MLFilter:

    def __init__(self):

        # 기본 임계값 (실전에서는 학습 모델로 교체)
        self.threshold = 0.55

    # =================================================
    # FEATURE ENGINEERING
    # =================================================
    def build_features(self, prices, volumes):

        prices = np.array(prices)
        volumes = np.array(volumes)

        returns = np.diff(prices)

        features = {
            "return_mean": float(np.mean(returns)),
            "return_std": float(np.std(returns)),
            "vol_mean": float(np.mean(volumes)),
            "momentum": float(prices[-1] - prices[0]),
        }

        return features

    # =================================================
    # MOCK MODEL PREDICTION
    # =================================================
    def predict(self, features):

        # 👉 실제 ML 모델 자리 (sklearn / pytorch 교체 가능)

        score = (
            0.3 * features["return_mean"] +
            0.2 * features["momentum"] +
            0.1 * features["vol_mean"] -
            0.1 * features["return_std"]
        )

        # sigmoid-like scaling
        prob = 1 / (1 + np.exp(-score))

        return float(prob)

    # =================================================
    # FILTER
    # =================================================
    def allow_trade(self, prices, volumes):

        features = self.build_features(prices, volumes)
        prob = self.predict(features)

        return prob > self.threshold, prob


# SINGLETON
ml_filter = MLFilter()
