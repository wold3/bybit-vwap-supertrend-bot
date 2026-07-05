from config import TESTNET

def execute(signal, symbol, qty):

    print(f"[ORDER] {signal} {symbol} {qty}")

    return {"status": "ok"}
