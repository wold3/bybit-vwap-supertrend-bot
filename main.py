import time


from app import (
    start_bot,
    stop_bot,
)


from core.bot_guard import (
    bot_guard
)


from utils.logger import (
    error_logger,
)





# ==========================================================
# MAIN
# ==========================================================

def main():


    try:


        start_bot()



        print(
            "[MAIN LOOP START]"
        )





        while bot_guard.is_running():


            time.sleep(1)






    except KeyboardInterrupt:


        print(
            "\n[KEYBOARD INTERRUPT]"
        )



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






    finally:


        print(
            "[MAIN EXIT]"
        )









if __name__ == "__main__":


    main()
