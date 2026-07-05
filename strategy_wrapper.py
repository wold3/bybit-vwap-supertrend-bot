def execute_strategy(strategy, signal):

    if strategy in ["trend", "range"]:
        return signal == "BUY"

    return False
