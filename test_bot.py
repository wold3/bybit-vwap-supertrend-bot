import time


from config import (
    DEFAULT_SYMBOL,
    BYBIT_BASE_URL,
    LIVE_TRADING
)



from portfolio.bybit_wallet import wallet


from execution.order_manager import order_manager


from position.position_manager import position_manager


from strategy.strategy_engine import strategy_engine






print("==============================")
print("BOT SYSTEM TEST")
print("==============================")


print(
    "BASE :",
    BYBIT_BASE_URL
)


print(
    "SYMBOL :",
    DEFAULT_SYMBOL
)


print(
    "LIVE :",
    LIVE_TRADING
)


print("==============================")







# ==================================
# WALLET TEST
# ==================================


print()

print(
    "[1] WALLET TEST"
)



try:


    equity = wallet.get_equity()



    print(
        "[EQUITY]",
        equity
    )


except Exception as e:


    print(
        "[WALLET ERROR]",
        e
    )









# ==================================
# POSITION TEST
# ==================================


print()

print(
    "[2] POSITION TEST"
)



try:


    pos = position_manager.sync()



    print(
        "[POSITION]",
        pos
    )


except Exception as e:


    print(
        "[POSITION ERROR]",
        e
    )









# ==================================
# STRATEGY TEST
# ==================================


print()

print(
    "[3] STRATEGY TEST"
)



fake_candle = {


    "symbol":

    DEFAULT_SYMBOL,


    "timestamp":

    int(time.time()*1000),


    "open":

    62800,


    "high":

    62900,


    "low":

    62750,


    "close":

    62850,


    "volume":

    10

}






try:


    signal = strategy_engine.on_candle(

        fake_candle

    )


    print(
        "[SIGNAL]",
        signal
    )



except Exception as e:


    print(
        "[STRATEGY ERROR]",
        e
    )









# ==================================
# ORDER TEST
# ==================================


print()

print(
    "[4] DEMO ORDER TEST"
)



if LIVE_TRADING is False:


    try:


        result = order_manager.create_order(


            side="Buy",


            qty="0.001"


        )



        print(
            "[ORDER RESULT]",
            result
        )



    except Exception as e:


        print(
            "[ORDER ERROR]",
            e
        )



else:


    print(
        "[SKIP] LIVE MODE"
    )








print()

print("==============================")
print("SYSTEM TEST COMPLETE")
print("==============================")
