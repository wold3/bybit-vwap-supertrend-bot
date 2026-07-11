# =====================================================
# web/server.py
# Flask Dashboard Server
# =====================================================

from flask import (
    Flask,
    jsonify,
    render_template
)


import threading
import time



from web.chart_data import (
    get_chart
)





app = Flask(

    __name__,

    template_folder="templates"

)





# =====================================================
# GLOBAL STATUS
# =====================================================


status = {


    "bot":

        "STARTING",


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


    "entry":

        0,


    "size":

        0,


    "pnl":

        0,


    "tp":

        0,


    "sl":

        0,


    "watchdog":

        "STARTING"

}





logs = []



lock = threading.Lock()







# =====================================================
# UPDATE STATUS
# =====================================================


def update_status(data):


    with lock:


        status.update(

            data

        )








# =====================================================
# ADD LOG
# =====================================================


def add_log(message):


    with lock:


        logs.append(

            f"{time.strftime('%H:%M:%S')}  {message}"

        )



        if len(logs) > 100:


            logs.pop(0)









# =====================================================
# DASHBOARD PAGE
# =====================================================


@app.route("/")

def dashboard():


    return render_template(

        "dashboard.html"

    )









# =====================================================
# STATUS API
# =====================================================


@app.route("/api/status")

def api_status():


    with lock:


        return jsonify({


            "status":

                status,


            "logs":

                logs[::-1]


        })









# =====================================================
# CHART API
# =====================================================


@app.route("/api/chart")

def api_chart():


    return jsonify(

        get_chart()

    )









# =====================================================
# HEALTH CHECK
# =====================================================


@app.route("/health")

def health():


    return jsonify({


        "status":

            "OK"


    })









# =====================================================
# SERVER START
# =====================================================


def start_dashboard():


    thread = threading.Thread(

        target=lambda:

            app.run(

                host="0.0.0.0",

                port=8000,

                debug=False,

                use_reloader=False

            ),


        daemon=True

    )


    thread.start()



    print(

        "[WEB SERVER START] 8000"

    )
