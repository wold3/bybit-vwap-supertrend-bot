import numpy as np


class MLFilter:

    def __init__(self):

        # 임시 가중치 (나중에 모델로 교체)
        self.weights = {
            "trend": 0.4,
            "volatility": 0.3,
            "momentum": 0.3
        }

    # =================================================
    # FEATURE ENGINE
    # =================================================
    def extract_features(self, market_data):

        close = market_data["close"]
        high = market_data["high"]
        low = market_data["low"]

        trend = (close - low) / (high - low + 1e-6)
        volatility = (high - low) / close
        momentum = np.tanh((close - market_data["open"]) / close)

        return {
            "trend": trend,
            "volatility": volatility,
            "momentum": momentum
        }

    # =================================================
    # SCORE CALC
    # =================================================
    def score(self, features):

        score = (
            features["trend"] * self.weights["trend"] +
            features["volatility"] * self.weights["volatility"] +
            features["momentum"] * self.weights["momentum"]
        )

        return score

    # =================================================
    # DECISION
    # =================================================
    def allow_trade(self, market_data):

        features = self.extract_features(market_data)
        score = self.score(features)

        print(f"[ML FILTER] SCORE = {score}")

        return score > 0.55


# SINGLETON
ml_filter = MLFilter()
