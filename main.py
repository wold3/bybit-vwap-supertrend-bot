import time
import threading
import signal


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


from strategy.strategy_engine import (
    strategy_engine,
)


from execution.order_manager import (
    order_manager,
)


from risk.risk_manager import (
    risk_manager,
)


from position.position_manager import (
    position_manager,
)


from portfolio.bybit_wallet import (
    wallet,
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



# =====================================================
# HEARTBEAT
# =====================================================

def heartbeat_loop():


    while bot_guard.is_running():

        try:

            bot_guard.heartbeat()


        except Exception as e:


            error_logger.error(
                str(e)
            )


        time.sleep(60)




# =====================================================
# CANDLE HANDLER
# =====================================================

def handle_candle(
    candle
):


    try:


        signal = strategy_engine.on_candle(
            candle
        )


        if signal is None:

            return



        print(
            "[STRATEGY SIGNAL]",
            signal
        )



        # main에서는 주문하지 않음
        # strategy → execution 분리



    except Exception as e:


        print(
            "[CANDLE ERROR]",
            e
        )


        error_logger.exception(
            str(e)
        )





# =====================================================
# POSITION MONITOR
# =====================================================

def position_loop():


    while bot_guard.is_running():


        try:

            position_manager.sync()


        except Exception as e:

            error_logger.error(
                str(e)
            )


        time.sleep(10)




# =====================================================
# RISK MONITOR
# =====================================================

def risk_loop():


    while bot_guard.is_running():


        try:


            if not risk_manager.check_daily_loss():


                print(
                    "[RISK STOP]"
                )


                bot_guard.stop()


                break



        except Exception as e:


            error_logger.error(
                str(e)
            )



        time.sleep(30)





# =====================================================
# START
# =====================================================

def start_bot():


    print("====================================")
    print("VWAP SUPERTREND BOT START")
    print("LIVE :", LIVE_TRADING)
    print("SYMBOL :", DEFAULT_SYMBOL)
    print("BASE :", BYBIT_BASE_URL)
    print("====================================")



    bot_logger.info(
        "BOT START"
    )



    # watchdog

    watchdog.start()



    # wallet

    equity = wallet.get_equity()


    print(
        "[ACCOUNT EQUITY]",
        equity
    )



    # risk

    risk_manager.initialize()



    # websocket callback

    ws_client.set_callback(
        handle_candle
    )



    # public websocket

    threading.Thread(

        target=ws_client.start,

        daemon=True

    ).start()



    # private websocket

    threading.Thread(

        target=private_ws_client.start,

        daemon=True

    ).start()



    # heartbeat

    threading.Thread(

        target=heartbeat_loop,

        daemon=True

    ).start()



    # position

    threading.Thread(

        target=position_loop,

        daemon=True

    ).start()



    # risk

    threading.Thread(

        target=risk_loop,

        daemon=True

    ).start()



    print(
        "[BOT RUNNING]"
    )


    bot_logger.info(
        "BOT RUNNING"
    )





# =====================================================
# STOP
# =====================================================

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

    except Exception:

        pass



    try:

        private_ws_client.stop()

    except Exception:

        pass



    try:

        watchdog.stop()

    except Exception:

        pass



    print(
        "[BOT STOPPED]"
    )


    bot_logger.info(
        "BOT STOPPED"
    )





# =====================================================
# SIGNAL
# =====================================================

def shutdown_handler(
    sig,
    frame
):

    stop_bot()





signal.signal(
    signal.SIGINT,
    shutdown_handler
)


signal.signal(
    signal.SIGTERM,
    shutdown_handler
)





# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":


    try:


        start_bot()



        while bot_guard.is_running():


            time.sleep(1)



    except Exception as e:


        print(
            "[MAIN ERROR]",
            e
        )


        error_logger.exception(
            str(e)
        )


        stop_bot()
