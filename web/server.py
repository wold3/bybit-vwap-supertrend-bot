# =====================================================
# web/server.py
# Browser Dashboard Server
# =====================================================


from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import threading
import uvicorn
import os
import time



from web.chart_data import (
    get_candles
)





app = FastAPI(
    title="VWAP SuperTrend BOT Dashboard"
)





# =====================================================
# GLOBAL STATUS
# =====================================================


STATUS = {


    "bot":

        "STOPPED",


    "symbol":

        "BTCUSDT",


    "price":

        0,


    "vwap":

        0,


    "trend":

        "NONE",


    "position":

        "NONE",


    "signal":

        "NONE",


    "time":

        0


}





LOGS = []



LOCK = threading.Lock()







# =====================================================
# HOME
# =====================================================


@app.get(
    "/",
    response_class=HTMLResponse
)
def home():


    path = os.path.join(

        "web",

        "dashboard.html"

    )



    try:


        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:


            return f.read()



    except Exception as e:


        return f"""

        <h1>
        Dashboard Error
        </h1>

        <p>
        {e}
        </p>

        """









# =====================================================
# STATUS API
# =====================================================


@app.get(
    "/api/status"
)
def status():


    with LOCK:


        return STATUS







# =====================================================
# CHART API
# =====================================================


@app.get(
    "/api/chart"
)
def chart():


    return get_candles()







# =====================================================
# LOG API
# =====================================================


@app.get(
    "/api/logs"
)
def logs():


    with LOCK:


        return LOGS[-100:]









# =====================================================
# UPDATE STATUS
# =====================================================


def update_status(
    data
):


    with LOCK:


        STATUS.update(

            data

        )


        STATUS["time"] = int(

            time.time()

        )







# =====================================================
# ADD LOG
# =====================================================


def add_log(
    message
):


    with LOCK:


        LOGS.append(

            {

            "time":

                time.strftime(

                    "%H:%M:%S"

                ),


            "message":

                str(message)

            }

        )



        if len(LOGS) > 200:


            LOGS.pop(0)









# =====================================================
# DASHBOARD START
# =====================================================


def start_dashboard():


    thread = threading.Thread(

        target=lambda:

            uvicorn.run(

                app,

                host="0.0.0.0",

                port=8000,

                log_level="warning"

            ),


        daemon=True

    )



    thread.start()



    print(

        "[WEB DASHBOARD READY]"

    )
