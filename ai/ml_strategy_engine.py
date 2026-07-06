import numpy as np
from collections import deque
from sklearn.ensemble import RandomForestClassifier

from strategy.strategy_router import trend_direction, volatility


class MLStrategyEngine:

    def __init__(self):

        self.X = deque(maxlen=2000)
        self.y = deque(maxlen=2000)

        self.model = RandomForestClassifier(
            n_estimators=50,
            max_depth=6,
            random_state=42
        )

        self.is_trained = False

    # =====================================================
    # feature 생성
    # =====================================================

    def extract_features(self, price):

        trend = trend_direction()
        vol = volatility()

        return [
            price % 100,          # normalized price pattern
            vol,
            1 if trend == "TREND_UP" else 0,
            1 if trend == "TREND_DOWN" else 0
        ]

    # =====================================================
    # 데이터 추가 (학습 데이터)
    # =====================================================

    def add_sample(self, price, label):

        x = self.extract_features(price)

        self.X.append(x)
        self.y.append(label)

    # =====================================================
    # 모델 학습
    # =====================================================

    def train(self):

        if len(self.X) < 50:
            return False

        self.model.fit(list(self.X), list(self.y))

        self.is_trained = True

        return True

    # =====================================================
    # 예측
    # =====================================================

    def predict(self, price):

        if not self.is_trained:
            return "trend"

        x = np.array(self.extract_features(price)).reshape(1, -1)

        pred = self.model.predict(x)[0]

        return pred

    # =====================================================
    # 온라인 업데이트
    # =====================================================

    def update(self, price, pnl):

        # pnl 기반 label 생성
        if pnl > 0:
            label = 1
        else:
            label = 0

        self.add_sample(price, label)

        if len(self.X) % 50 == 0:
            self.train()


# =====================================================
# SINGLETON
# =====================================================

ml_engine = MLStrategyEngine()
