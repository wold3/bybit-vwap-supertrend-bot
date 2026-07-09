import time
import threading


from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL,
    BYBIT_BASE_URL,
)


from market.websocket_client import (
    ws_client,
)


from services.private_ws_client import (
    private_ws_client,
)


from portfolio.bybit_wallet import (
    wallet,
)


from execution.order_manager import (
    order_manager,
)


from strategy.strategy_engine import (
    strategy_engine,
)


from risk.risk_manager import (
    risk_manager,
)


from position.position_manager import (
    position_manager,
)


from watchdog.watchdog import (
    watchdog,
)


from core.bot_guard import (
    bot_guard,
)


from utils.logger import (
    bot_logger,
    error_logger,
)



# ==========================================================
# HEARTBEAT LOOP
# ==========================================================

def heartbeat_loop():

    print("[HEARTBEAT LOOP START]")

    while bot_guard.is_running():

        try:

            bot_guard.heartbeat()

        except Exception as e:

            print(
                "[HEARTBEAT ERROR]",
                e
            )

            error_logger.exception(
                str(e)
            )

        time.sleep(60)



# ==========================================================
# CANDLE HANDLER
# ==========================================================

def handle_candle(candle):

    try:

        signal = strategy_engine.on_candle(
            candle
        )


        if signal is None:

            return



        print(
            "[SIGNAL]",
            signal
        )



        qty = 0.001



        if not risk_manager.allow_order(
            qty
        ):

            print(
                "[ORDER BLOCKED BY RISK]"
            )

            return




        if signal == "BUY":


            result = order_manager.create_order(

                side="Buy",

                qty=qty

            )


        elif signal == "SELL":


            result = order_manager.create_order(

                side="Sell",

                qty=qty

            )


        else:

            return




        if result is None:

            return



        if result.get(
            "retCode"
        ) == 0:


            print(
                "[ORDER SUCCESS]"
            )


            bot_logger.info(
                f"ORDER SUCCESS {signal}"
            )


            risk_manager.record_order()


            position_manager.sync()



        else:


            print(
                "[ORDER FAILED]",
                result
            )


            bot_logger.warning(
                str(result)
            )



    except Exception as e:


        print(
            "[HANDLE CANDLE ERROR]",
            e
        )


        error_logger.exception(
            str(e)
        )




# ==========================================================
# STRATEGY MONITOR LOOP
# ==========================================================

def strategy_loop():


    print(
        "[STRATEGY LOOP START]"
    )


    while bot_guard.is_running():


        try:


            if not risk_manager.check_daily_loss():


                print(
                    "[BOT STOP] DAILY LOSS"
                )


                bot_logger.warning(
                    "DAILY LOSS LIMIT"
                )


                bot_guard.stop()


                break



            time.sleep(5)



        except Exception as e:


            print(
                "[STRATEGY LOOP ERROR]",
                e
            )


            error_logger.exception(
                str(e)
            )


            time.sleep(5)




# ==========================================================
# START BOT
# ==========================================================

def start_bot():


    print("==============================")
    print("VWAP SUPERTREND BOT START")
    print("LIVE :", LIVE_TRADING)
    print("SYMBOL :", DEFAULT_SYMBOL)
    print("BASE :", BYBIT_BASE_URL)
    print("==============================")



    bot_logger.info(
        "BOT START"
    )



    # -------------------------
    # WATCHDOG
    # -------------------------

    watchdog.start()



    # -------------------------
    # ACCOUNT
    # -------------------------

    try:

        equity = wallet.get_equity()


        print(
            "[ACCOUNT EQUITY]",
            equity
        )


    except Exception as e:


        print(
            "[WALLET ERROR]",
            e
        )




    # -------------------------
    # RISK INIT
    # -------------------------

    risk_manager.initialize()



    # -------------------------
    # POSITION SYNC
    # -------------------------

    position_manager.sync()



    # -------------------------
    # PUBLIC WS CALLBACK
    # -------------------------

    ws_client.set_callback(
        handle_candle
    )



    # -------------------------
    # PUBLIC WS
    # -------------------------

    public_thread = threading.Thread(

        target=ws_client.start,

        daemon=True

    )

    public_thread.start()




    # -------------------------
    # PRIVATE WS
    # -------------------------

    private_thread = threading.Thread(

        target=private_ws_client.start,

        daemon=True

    )

    private_thread.start()




    # -------------------------
    # STRATEGY
    # -------------------------

    strategy_thread = threading.Thread(

        target=strategy_loop,

        daemon=True

    )


    strategy_thread.start()




    # -------------------------
    # HEARTBEAT
    # -------------------------

    heartbeat_thread = threading.Thread(

        target=heartbeat_loop,

        daemon=True

    )


    heartbeat_thread.start()



    print(
        "[BOT RUNNING]"
    )


    bot_logger.info(
        "BOT RUNNING"
    )




# ==========================================================
# STOP BOT
# ==========================================================

def stop_bot():


    print(
        "[BOT STOPPING]"
    )


    bot_logger.info(
        "BOT STOPPING"
    )



    bot_guard.stop()



    try:

        ws_client.stop()

    except Exception as e:

        error_logger.exception(
            str(e)
        )



    try:

        private_ws_client.stop()

    except Exception as e:

        error_logger.exception(
            str(e)
        )



    try:

        watchdog.stop()

    except Exception as e:

        error_logger.exception(
            str(e)
        )



    print(
        "[BOT STOPPED]"
    )


    bot_logger.info(
        "BOT STOPPED"
    )




# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    try:


        start_bot()



        while bot_guard.is_running():


            time.sleep(1)



    except KeyboardInterrupt:


        stop_bot()



    except Exception as e:


        print(
            "[MAIN ERROR]",
            e
        )


        error_logger.exception(
            str(e)
        )


        stop_bot()
