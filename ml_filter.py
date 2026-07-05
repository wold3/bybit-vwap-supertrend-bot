from feature_engine import get_features


class MLModel:
    """
    간단한 Feature 기반 ML Filter
    """

    def __init__(self):

        self.threshold = 0.60

    def predict(self, features):

        score = 0.50

        # -------------------------
        # Trend
        # -------------------------
        trend = features["trend"]

        if trend > 0:
            score += min(abs(trend) * 2.0, 0.20)
        else:
            score -= min(abs(trend) * 2.0, 0.20)

        # -------------------------
        # Momentum
        # -------------------------
        momentum = features["momentum"]

        if momentum > 0:
            score += 0.10
        else:
            score -= 0.10

        # -------------------------
        # Volatility
        # -------------------------
        volatility = features["volatility"]

        if volatility > features["price"] * 0.03:
            score -= 0.10

        return max(
            0.0,
            min(score, 1.0)
        )


model = MLModel()


def should_enter_market(price):
    """
    진입 여부 판단

    Returns
    -------
    (allow, score)
    """

    features = get_features(price)

    score = model.predict(features)

    return (
        score >= model.threshold,
        round(score, 4),
    )


def get_score(price):
    """
    ML Score 반환
    """

    return should_enter_market(price)[1]


def get_threshold():
    """
    현재 Threshold
    """

    return model.threshold


def set_threshold(value):
    """
    Threshold 변경
    """

    model.threshold = float(value)
