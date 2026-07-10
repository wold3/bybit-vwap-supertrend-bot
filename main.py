import time


from app import app



if __name__ == "__main__":


    try:

        app.start()


        while True:

            time.sleep(1)



    except KeyboardInterrupt:


        print(
            "\n[MAIN SHUTDOWN]"
        )


        app.stop()
