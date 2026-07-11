# =====================================================
# web/server.py
# Dashboard Web Server
# =====================================================

from flask import Flask, jsonify, render_template
import threading
import time



from config import (
    WEB_HOST,
    WEB_PORT
)





app = Flask(
    __name__,
    template_folder="templates"
)





# =====================================================
# STATUS STORAGE
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

        "NONE",


    "size":

        0,


    "entry":

        0,


    "pnl":

        0,


    "order":

        "NONE",


    "tp":

        0,


    "sl":

        0

}






logs = []






# =====================================================
# CHART DATA
# =====================================================


chart_data = []







def add_candle(data):


    global chart_data


    chart_data.append(

        data

    )


    if len(chart_data) > 200:


        chart_data.pop(0)









# =====================================================
# UPDATE STATUS
# =====================================================


def update_status(data):


    status.update(

        data

    )







# =====================================================
# ADD LOG
# =====================================================


def add_log(message):


    timestamp = time.strftime(

        "%H:%M:%S"

    )


    logs.append(

        f"[{timestamp}] {message}"

    )


    if len(logs) > 100:


        logs.pop(0)








# =====================================================
# PAGE
# =====================================================


@app.route("/")

def index():

    return render_template(

        "dashboard.html"

    )







# =====================================================
# STATUS API
# =====================================================


@app.route("/api/status")

def api_status():


    return jsonify({


        "status":

            status,


        "logs":

            logs


    })









# =====================================================
# CHART API
# =====================================================


@app.route("/api/chart")

def api_chart():


    return jsonify(

        chart_data

    )









# =====================================================
# SERVER START
# =====================================================


def run_server():


    app.run(

        host=WEB_HOST,

        port=WEB_PORT,

        debug=False,

        use_reloader=False

    )








def start_dashboard():


    thread = threading.Thread(

        target=run_server,

        daemon=True

    )


    thread.start()



    print(

        "[WEB SERVER START]",

        WEB_PORT

    )









# =====================================================
# TEST
# =====================================================


if __name__ == "__main__":


    start_dashboard()


    while True:


        time.sleep(1)
