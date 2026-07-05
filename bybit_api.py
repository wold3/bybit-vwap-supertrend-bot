def execute(signal, symbol, qty):

    print(f"[EXECUTE] {signal} | {symbol} | {qty}")

    # TODO: 여기 Bybit 실제 주문 붙이면 됨

    return {
        "status": "ok",
        "signal": signal,
        "symbol": symbol,
        "qty": qty
    }
