# =====================================================
# web/server.py
# Browser Dashboard Server
# =====================================================

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import threading
import uvicorn
import time


app = FastAPI()



STATUS = {

    "bot":"STOPPED",

    "symbol":"BTCUSDT",

    "price":0,

    "vwap":0,

    "trend":"",

    "position":"NONE"

}



@app.get(
    "/",
    response_class=HTMLResponse
)
def home():


    return open(

        "web/dashboard.html",

        encoding="utf-8"

    ).read()







@app.get("/api/status")
def status():


    return STATUS







def update_status(data):


    STATUS.update(

        data

    )









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
