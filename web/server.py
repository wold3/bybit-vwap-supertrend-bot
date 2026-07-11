# =====================================================
# web/server.py
# VWAP SUPERTREND BOT DASHBOARD SERVER
# =====================================================

from flask import Flask, render_template, jsonify, request

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
# GLOBAL
# =====================================================

bot_instance = None

server_started = False


logs = []


MAX_LOGS = 300


status = {

    "mode":"DEMO",

    "bot":"STOPPED",

    "symbol":"BTCUSDT",

    "position":"NONE",

    "position_size":0,

    "entry_price":0,

    "pnl":0,

    "last_action":"NONE"

}



lock = threading.Lock()



# =====================================================
# LOG
# =====================================================

def add_log(msg):

    t=time.strftime("%H:%M:%S")

    text=f"[{t}] {msg}"

    print(text)


    with lock:

        logs.append(text)

        if len(logs)>MAX_LOGS:

            logs.pop(0)



def update_status(data):

    with lock:

        status.update(data)



def get_status():

    with lock:

        return status.copy()



# =====================================================
# BOT CONNECT
# =====================================================

def set_bot_instance(bot):

    global bot_instance

    bot_instance=bot

    add_log(
        "BOT INSTANCE CONNECTED"
    )





# =====================================================
# HOME
# =====================================================

@app.route("/")

def index():

    return render_template(
        "index.html"
    )





# =====================================================
# STATUS
# =====================================================

@app.route("/api/status")

def api_status():

    with lock:

        return jsonify({

            "status":status.copy(),

            "logs":logs[-100:]

        })





# =====================================================
# START
# =====================================================

@app.route(
    "/api/start",
    methods=["POST"]
)

def start_bot():

    try:

        if bot_instance:

            bot_instance.start()


        update_status({

            "bot":"RUNNING",

            "last_action":
            "START BUTTON"

        })


        add_log(
            "START BUTTON CLICK"
        )


        return jsonify(
            success=True
        )


    except Exception as e:


        add_log(
            f"START ERROR {e}"
        )


        return jsonify(
            success=False
        )





# =====================================================
# STOP
# =====================================================

@app.route(
    "/api/stop",
    methods=["POST"]
)

def stop_bot():


    try:


        if bot_instance:

            bot_instance.stop()



        update_status({

            "bot":"STOPPED",

            "last_action":
            "STOP BUTTON"

        })



        add_log(
            "STOP BUTTON CLICK"
        )


        return jsonify(
            success=True
        )



    except Exception as e:


        add_log(
            f"STOP ERROR {e}"
        )


        return jsonify(
            success=False
        )






# =====================================================
# MODE
# =====================================================

@app.route(
    "/api/mode",
    methods=["POST"]
)

def mode():

    data=request.json or {}

    mode=data.get(
        "mode",
        "DEMO"
    )


    update_status({

        "mode":mode,

        "last_action":
        f"{mode} MODE BUTTON"

    })


    add_log(
        f"MODE CHANGE {mode}"
    )


    return jsonify(
        success=True
    )






# =====================================================
# SYMBOL
# =====================================================

@app.route(
    "/api/symbol",
    methods=["POST"]
)

def symbol():


    data=request.json or {}


    sym=data.get(
        "symbol",
        "BTCUSDT"
    )


    try:

        from api.bybit_api import bybit_api


        bybit_api.change_symbol(
            sym
        )


        update_status({

            "symbol":sym,

            "last_action":
            f"SYMBOL {sym}"

        })


        add_log(
            f"SYMBOL CHANGE {sym}"
        )


        return jsonify(
            success=True
        )


    except Exception as e:


        add_log(
            f"SYMBOL ERROR {e}"
        )


        return jsonify(
            success=False
        )







# =====================================================
# CLOSE
# =====================================================

@app.route(
    "/api/close",
    methods=["POST"]
)

def close():


    try:


        from order.order_manager import order_manager


        order_manager.close_position()



        update_status({

            "last_action":
            "CLOSE POSITION BUTTON"

        })


        add_log(
            "CLOSE BUTTON CLICK"
        )


        return jsonify(
            success=True
        )


    except Exception as e:


        add_log(
            f"CLOSE ERROR {e}"
        )


        return jsonify(
            success=False
        )







# =====================================================
# SERVER
# =====================================================

def run_server():


    global server_started


    if server_started:

        return


    server_started=True



    th=threading.Thread(

        target=lambda:
        app.run(

            host=WEB_HOST,

            port=WEB_PORT,

            debug=False,

            use_reloader=False

        ),

        daemon=True

    )


    th.start()


    print(
        f"[WEB] http://{WEB_HOST}:{WEB_PORT}"
    )





__all__=[

"app",

"run_server",

"set_bot_instance",

"update_status",

"get_status",

"add_log"

]



if __name__=="__main__":

    run_server()

    while True:

        time.sleep(1)
