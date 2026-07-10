import signal
import sys
import time


from app import TradingApp



app = TradingApp()



running = True



def shutdown_handler(sig, frame):

    global running


    print("[SYSTEM] SHUTDOWN")


    running = False


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



        while running:


            # Health Check

            if hasattr(app, "health_check"):

                app.health_check()



            time.sleep(5)



    except Exception as e:


        print(
            "[MAIN ERROR]",
            e
        )


        app.stop()
