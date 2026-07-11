# =====================================================
# web/server.py
# Flask Dashboard Server
# =====================================================

from flask import (
    Flask,
    jsonify,
    request,
    render_template
)

import threading
import time



app = Flask(
    __name__,
    template_folder="templates"
)



# =====================================================
# GLOBAL STATE
# =====================================================

lock = threading.Lock()



CURRENT_MODE = "DEMO"



STATUS = {

    "bot": "STOPPED",

    "mode": "DEMO",

    "position": "NONE",

    "position_size": 0,

    "entry_price": 0,

    "pnl": 0,

    "signal": "WAIT",

    "watchdog": "OFF"

}



LOGS = []









# =====================================================
# STATUS UPDATE
# =====================================================

def update_status(data):


    with lock:

        STATUS.update(

            data

        )









# =====================================================
# LOG SYSTEM
# =====================================================

def add_log(message):


    with lock:


        LOGS.append(

            f"{time.strftime('%H:%M:%S')} "

            +

            str(message)

        )



        if len(LOGS) > 100:


            LOGS.pop(0)









# =====================================================
# GET MODE
# =====================================================

def get_trading_mode():


    with lock:


        return CURRENT_MODE










# =====================================================
# CHANGE MODE
# =====================================================

def change_mode(mode):


    global CURRENT_MODE



    mode = str(mode).upper()



    if mode not in [

        "DEMO",

        "LIVE"

    ]:


        return False





    with lock:


        CURRENT_MODE = mode


        STATUS["mode"] = mode





    add_log(

        f"MODE CHANGE : {mode}"

    )





    # -----------------------------
    # BYBIT SESSION CHANGE
    # -----------------------------

    try:


        from api.bybit_api import bybit_api



        bybit_api.change_session(

            mode

        )



        add_log(

            f"BYBIT SESSION : {mode}"

        )



    except Exception as e:


        add_log(

            f"SESSION ERROR : {e}"

        )







    # -----------------------------
    # PRIVATE WS RESTART
    # -----------------------------

    try:


        from services.private_ws import private_ws



        private_ws.stop()


        time.sleep(1)


        private_ws.start()



        add_log(

            "PRIVATE WS RESTART"

        )



    except Exception as e:


        add_log(

            f"WS RESTART ERROR : {e}"

        )






    return True










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

@app.route(

    "/api/status"

)

def api_status():


    with lock:


        return jsonify({


            "status":

                STATUS.copy(),


            "logs":

                LOGS[-50:]

        })









# =====================================================
# MODE API
# =====================================================

@app.route(

    "/api/mode",

    methods=["POST"]

)

def api_mode():


    data = request.get_json(

        silent=True

    ) or {}



    mode = data.get(

        "mode"

    )



    result = change_mode(

        mode

    )



    return jsonify({


        "success":

            result,


        "mode":

            get_trading_mode()


    })









# =====================================================
# HEALTH CHECK
# =====================================================

@app.route(

    "/api/health"

)

def health():


    return jsonify({


        "server":

            "OK",


        "mode":

            get_trading_mode()


    })









# =====================================================
# BOT STATUS
# =====================================================

def bot_running():


    update_status({

        "bot":

            "RUNNING"

    })









def bot_stopped():


    update_status({

        "bot":

            "STOPPED"

    })









# =====================================================
# SERVER START
# =====================================================

def start_server():


    print(

        "[WEB SERVER START] 8000"

    )


    app.run(

        host="0.0.0.0",

        port=8000,

        debug=False,

        use_reloader=False

    )









def run_server():


    thread = threading.Thread(

        target=start_server,

        daemon=True

    )


    thread.start()
