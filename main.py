import signal
import sys
import time

from app import TradingApp


app = TradingApp()



def shutdown_handler(sig, frame):

    print("[SYSTEM] SHUTDOWN")

    app.stop()

    sys.exit(0)



signal.signal(
    signal.SIGINT,
    shutdown_handler
)


signal.signal(
    signal.SIGTERM,
    shutdown_handler
)



if __name__ == "__main__":


    try:

        app.start()


        while True:

            time.sleep(1)



    except Exception as e:

        print(
            "[MAIN ERROR]",
            e
        )

        app.stop()
