import subprocess
import time
import os
import sys



PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)



PYTHON = sys.executable



RESTART_DELAY = 10






def start_bot():


    print(
        "=============================="
    )

    print(
        "[AUTO START BOT]"
    )

    print(
        "DIR:",
        PROJECT_DIR
    )

    print(
        "=============================="
    )





    process = subprocess.Popen(

        [
            PYTHON,
            "main.py"
        ],

        cwd=PROJECT_DIR

    )



    return process







def monitor():


    while True:


        try:


            process = start_bot()



            code = process.wait()



            print(

                "[BOT EXIT]",

                code

            )



            print(

                "[RESTART AFTER]",

                RESTART_DELAY,

                "SEC"

            )



            time.sleep(

                RESTART_DELAY

            )





        except KeyboardInterrupt:


            print(
                "[AUTO STOP]"
            )


            break





        except Exception as e:


            print(

                "[AUTO ERROR]",

                e

            )


            time.sleep(

                RESTART_DELAY

            )








if __name__ == "__main__":


    monitor()
