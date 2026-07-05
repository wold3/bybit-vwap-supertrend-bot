from feature_engine import get_feature_vector
from market_regime import get_market_score
from rl_agent import RLAgent

agent = RLAgent()


def build_state(price):
    """
    RL Agent 입력 상태 생성

    Returns
    -------
    list
    """

    features = get_feature_vector(price)

    market_score = get_market_score(price)

    state = features + [market_score]

    return state


def decide(price):
    """
    RL Agent 의사결정

    Returns
    -------
    0 : HOLD
    1 : BUY
    2 : SELL
    """

    state = build_state(price)

    return agent.act(state)


def get_state(price):
    """
    현재 상태 벡터 반환
    """

    return build_state(price)
