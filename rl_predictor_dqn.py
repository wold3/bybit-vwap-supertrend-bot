from dqn_agent import Agent
from feature_engine import get_feature_vector
from market_regime import get_market_score

agent = Agent()


def build_state(price):
    """
    DQN 입력 상태 생성

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
    DQN 의사결정

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


def decide_with_state(price):
    """
    디버깅용

    Returns
    -------
    (action, state)
    """

    state = build_state(price)

    action = agent.act(state)

    return action, state
