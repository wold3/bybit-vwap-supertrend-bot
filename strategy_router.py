from strategy_engine import select_strategy
from portfolio_engine import portfolio


def route(signal, price):
    """
    시장 상황에 맞는 전략 선택

    Args:
        signal (str): TradingView 신호 (BUY, SELL, SHORT, EXIT)
        price (float): 현재 가격

    Returns:
        dict
    """

    allow, strategy, regime = select_strategy(
        signal,
        price,
    )

    if not allow:
        return {
            "allow": False,
            "strategy": strategy,
            "regime": regime,
        }

    allocation = portfolio.allocate(regime)

    return {
        "allow": True,
        "strategy": allocation,
        "regime": regime,
    }
