# =====================================================
# web/server.py
# Flask Dashboard Server
# Demo / Live Mode Switch
# =====================================================

from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

import threading



from config import (
    WEB_HOST,
    WEB_PORT
)





# =====================================================
# FLASK
# =====================================================

app = Flask(__name__)





# =====================================================
# GLOBAL STATUS
# =====================================================

status = {


    "bot":

        "STOPPED",


    "price":

        0,


    "vwap":

        0,


    "trend":

        "-",


    "signal":

        "-",


    "position":

        "NONE",


    "entry":

        0,


    "size":

        0,


    "pnl":

        0,


    "watchdog":

        "OFF"

}





# =====================================================
# TRADING MODE
# =====================================================

trading_mode = {


    "mode":

        "DEMO"

}





# =====================================================
# LOG STORAGE
# =====================================================

logs = []


lock = threading.Lock()







# =====================================================
# STATUS UPDATE
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

            str(message)

        )



        if len(logs) > 200:


            logs.pop(0)









# =====================================================
# MODE CONTROL
# =====================================================

def set_trading_mode(mode):


    mode = str(mode).upper()



    if mode not in [

        "DEMO",

        "LIVE"

    ]:


        return False





    with lock:


        trading_mode["mode"] = mode



    add_log(

        f"TRADING MODE : {mode}"

    )



    return True










# =====================================================
# DASHBOARD PAGE
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


    with lock:


        return jsonify({


            "status":

                status.copy(),


            "mode":

                trading_mode["mode"],


            "logs":

                logs.copy()


        })









# =====================================================
# MODE API
# =====================================================

@app.route(
    "/api/mode",
    methods=["POST"]
)

def api_mode():


    data = request.json or {}


    mode = data.get(

        "mode",

        "DEMO"

    )



    result = set_trading_mode(

        mode

    )



    return jsonify({


        "success":

            result,


        "mode":

            trading_mode["mode"]


    })









# =====================================================
# CHART API
# =====================================================

@app.route("/api/chart")

def api_chart():


    try:


        from web.chart_data import (

            get_chart

        )


        return jsonify(

            get_chart()

        )



    except Exception as e:


        add_log(

            f"CHART ERROR : {e}"

        )


        return jsonify([])









# =====================================================
# MODE GET API
# =====================================================

@app.route("/api/mode")

def get_mode():


    return jsonify({


        "mode":

            trading_mode["mode"]


    })









# =====================================================
# SERVER START
# =====================================================

def run_server():


    print(

        "[WEB SERVER START]",

        WEB_PORT

    )



    app.run(

        host=WEB_HOST,


        port=WEB_PORT,


        debug=False,


        use_reloader=False

    )
