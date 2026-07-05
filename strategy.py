def filter_signal(signal):

    # 기본 risk filter
    if signal not in ["HOLD", "BUY", "SELL"]:
        return False

    return True
