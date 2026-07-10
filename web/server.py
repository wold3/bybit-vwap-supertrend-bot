# =====================================================
# web/server.py
# FastAPI Dashboard Server
# =====================================================

import threading
import time



from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn



from config import (
    WEB_HOST,
    WEB_PORT
)





app = FastAPI()





# =====================================================
# MEMORY STORE
# =====================================================


status = {


    "bot":
        "STOPPED",


    "symbol":
        "",


    "price":
        0,


    "vwap":
        0,


    "trend":
        "NONE",


    "volume":
        False,


    "signal":
        "NONE",


    "position":
        "NONE"


}







candles = []



logs = []









# =====================================================
# STATUS UPDATE
# =====================================================


def update_status(data):


    status.update(

        data

    )









# =====================================================
# LOG
# =====================================================


def add_log(message):


    logs.append(

        {

        "time":

            time.strftime(

                "%H:%M:%S"

            ),


        "message":

            str(message)

        }

    )


    if len(logs) > 200:


        logs.pop(0)









# =====================================================
# CANDLE
# =====================================================


def add_candle(candle):


    candles.append(

        candle

    )


    if len(candles) > 300:


        candles.pop(0)









# =====================================================
# DASHBOARD PAGE
# =====================================================


@app.get(

    "/",

    response_class=HTMLResponse

)

def index():


    try:


        with open(

            "web/dashboard.html",

            "r",

            encoding="utf-8"

        ) as f:


            return f.read()



    except Exception as e:


        return str(e)









# =====================================================
# API STATUS
# =====================================================


@app.get("/api/status")

def api_status():


    return status









# =====================================================
# API CHART
# =====================================================


@app.get("/api/chart")

def api_chart():


    return candles









# =====================================================
# API LOG
# =====================================================


@app.get("/api/logs")

def api_logs():


    return logs










# =====================================================
# SERVER START
# =====================================================


server_thread = None



def start_dashboard():


    global server_thread



    if server_thread:


        return




    def run():


        print(

            "[WEB SERVER START]",

            WEB_PORT

        )


        uvicorn.run(

            app,

            host=WEB_HOST,

            port=WEB_PORT,

            log_level="warning"

        )





    server_thread = threading.Thread(

        target=run,

        daemon=True

    )


    server_thread.start()
