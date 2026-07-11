# =====================================================
# web/server.py
# VWAP SUPERTREND BOT WEB SERVER
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
# GLOBAL
# =====================================================

lock = threading.Lock()


CURRENT_MODE = "DEMO"


BOT_INSTANCE = None



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
# BOT CONNECT
# =====================================================

def set_bot_instance(bot):

    global BOT_INSTANCE

    BOT_INSTANCE = bot





# =====================================================
# STATUS
# =====================================================

def update_status(data):

    with lock:

        STATUS.update(data)









def add_log(message):

    with lock:

        LOGS.append(

            f"{time.strftime('%H:%M:%S')} {message}"

        )


        if len(LOGS) > 100:

            LOGS.pop(0)









def get_trading_mode():

    with lock:

        return CURRENT_MODE









# =====================================================
# MODE CHANGE
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





    # Bybit session 변경

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






    # Private WS 재연결

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

            f"WS ERROR : {e}"

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

@app.route("/api/status")

def api_status():


    with lock:


        return jsonify({

            "status":

                STATUS.copy(),


            "logs":

                LOGS[-50:]

        })









# =====================================================
# HEALTH
# =====================================================

@app.route("/api/health")

def health():


    return jsonify({

        "server":

            "OK",


        "mode":

            CURRENT_MODE

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



    result = change_mode(

        data.get("mode")

    )



    return jsonify({

        "success":

            result,


        "mode":

            CURRENT_MODE

    })









# =====================================================
# BOT STOP
# =====================================================

@app.route(

    "/api/stop",

    methods=["POST"]

)

def api_stop():


    try:


        if BOT_INSTANCE:


            BOT_INSTANCE.stop()



        update_status({

            "bot":

                "STOPPED"

        })



        add_log(

            "BOT STOP COMMAND"

        )



        return jsonify({

            "success":

                True

        })



    except Exception as e:


        add_log(

            f"STOP ERROR {e}"

        )


        return jsonify({

            "success":

                False,

            "error":

                str(e)

        })









# =====================================================
# BOT START
# =====================================================

@app.route(

    "/api/start",

    methods=["POST"]

)

def api_start():


    try:


        if BOT_INSTANCE:


            BOT_INSTANCE.start()



        update_status({

            "bot":

                "RUNNING"

        })



        add_log(

            "BOT START COMMAND"

        )



        return jsonify({

            "success":

                True

        })



    except Exception as e:


        return jsonify({

            "success":

                False,

            "error":

                str(e)

        })









# =====================================================
# CLOSE POSITION
# =====================================================

@app.route(

    "/api/close",

    methods=["POST"]

)

def api_close():


    try:


        from api.bybit_api import bybit_api



        result = bybit_api.close_position()



        add_log(

            "CLOSE POSITION COMMAND"

        )



        return jsonify({

            "success":

                True,


            "result":

                result

        })



    except Exception as e:


        add_log(

            f"CLOSE ERROR {e}"

        )


        return jsonify({

            "success":

                False,

            "error":

                str(e)

        })









# =====================================================
# SERVER
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
