import time
import signal
import sys


from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL,
    BYBIT_BASE_URL,
)


from core.bot_guard import bot_guard


from utils.logger import (
    bot_logger,
    error_logger,
)


from app import (
    start_bot,
    stop_bot,
)





# ==========================================================
# SIGNAL HANDLER
# ==========================================================


def shutdown_handler(
    sig,
    frame
):

    print()

    print("==============================")
    print("[SYSTEM SIGNAL]")
    print(sig)
    print("==============================")


    stop_bot()

    sys.exit(0)






# ==========================================================
# START INFO
# ==========================================================


def print_banner():


    print()

    print("====================================")
    print(" BYBIT VWAP SUPERTREND BOT ")
    print("====================================")

    print(
        "LIVE :",
        LIVE_TRADING
    )

    print(
        "SYMBOL :",
        DEFAULT_SYMBOL
    )

    print(
        "BASE :",
        BYBIT_BASE_URL
    )

    print("====================================")

    print()







# ==========================================================
# MAIN LOOP
# ==========================================================


def main():


    print_banner()


    bot_logger.info(
        "MAIN START"
    )



    try:


        # --------------------------
        # START BOT
        # --------------------------

        start_bot()



        print(
            "[MAIN LOOP RUNNING]"
        )



        while bot_guard.is_running():


            time.sleep(1)



    except KeyboardInterrupt:


        print(
            "[CTRL+C]"
        )



    except Exception as e:


        print(
            "[MAIN ERROR]",
            e
        )


        error_logger.exception(
            str(e)
        )



    finally:


        stop_bot()


        bot_logger.info(
            "MAIN STOP"
        )


        print(
            "[SYSTEM EXIT]"
        )








# ==========================================================
# ENTRY
# ==========================================================


if __name__ == "__main__":


    signal.signal(
        signal.SIGINT,
        shutdown_handler
    )


    signal.signal(
        signal.SIGTERM,
        shutdown_handler
    )


    main()
