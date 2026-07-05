from feature_engine import get_feature_vector
from market_regime import get_market_score


class TradingEnv:
    """
    Reinforcement Learning Trading Environment
    """

    def __init__(self):

        self.initial_balance = 1000.0

        self.balance = self.initial_balance

        self.position = 0

        self.entry_price = 0.0

        self.current_price = 0.0

    # ---------------------------------------------

    def reset(self):

        self.balance = self.initial_balance

        self.position = 0

        self.entry_price = 0.0

        self.current_price = 0.0

        return self.state()

    # ---------------------------------------------

    def state(self):
        """
        DQN 입력 State

        price
        sma
        momentum
        volatility
        trend
        market_score
        """

        features = get_feature_vector(
            self.current_price
        )

        market_score = get_market_score(
            self.current_price
        )

        return features + [market_score]

    # ---------------------------------------------

    def step(
        self,
        action,
        price,
    ):

        self.current_price = float(price)

        reward = 0.0

        # BUY
        if action == 1:

            if self.position == 0:

                self.position = 1

                self.entry_price = price

        # SELL
        elif action == 2:

            if self.position == 1:

                reward = (
                    price
                    - self.entry_price
                )

                self.balance += reward

                self.position = 0

                self.entry_price = 0.0

        # HOLD
        else:

            reward = -0.01

        done = self.balance <= 0

        return (
            self.state(),
            reward,
            done,
        )

    # ---------------------------------------------

    def info(self):

        return {

            "balance": round(self.balance, 2),

            "position": self.position,

            "entry_price": self.entry_price,

            "current_price": self.current_price,

        }
