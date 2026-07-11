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

_server_thread = None


MAX_LOGS = 500



lock = threading.RLock()



logs = []



status = {


    "mode":
        "DEMO",


    "symbol":
        "BTCUSDT",


    "bot":
        "STOPPED",


    "position":
        "NONE",


    "position_size":
        0,


    "entry_price":
        0,


    "pnl":
        0,


    "price":
        0,


    "balance":
        0,


    "equity":
        0,


    "vwap":
        0,


    "trend":
        "NONE",


    "volume":
        0,


    "signal":
        "NONE",


    "watchdog":
        "OFF",


    "last_action":
        "SYSTEM READY"

}







# =====================================================
# LOG
# =====================================================

def add_log(message):


    text = (

        f"[{time.strftime('%H:%M:%S')}] "

        f"{message}"

    )


    print(text)



    with lock:


        logs.append(text)


        if len(logs) > MAX_LOGS:

            logs.pop(0)









# =====================================================
# STATUS
# =====================================================

def update_status(data):


    if not data:

        return



    with lock:

        status.update(data)







def get_status():


    with lock:

        return status.copy()









# =====================================================
# MODE / SYMBOL
# =====================================================

def get_trading_mode():


    with lock:

        return status.get(

            "mode",

            "DEMO"

        )







def get_trading_symbol():


    with lock:

        return status.get(

            "symbol",

            "BTCUSDT"

        )











# =====================================================
# BOT INSTANCE
# =====================================================

def set_bot_instance(bot):


    global bot_instance


    bot_instance = bot


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

            "status":
                status.copy(),


            "logs":
                logs[-100:]

        })









# =====================================================
# START
# =====================================================

@app.route(

    "/api/start",

    methods=["POST"]

)

def api_start():


    try:


        if bot_instance:


            bot_instance.start()



        update_status({

            "bot":
                "RUNNING",


            "last_action":
                "START CLICK"

        })



        add_log(

            "START BUTTON CLICK"

        )



        return jsonify({

            "success":
                True

        })



    except Exception as e:


        add_log(

            f"START ERROR {e}"

        )


        return jsonify({

            "success":
                False

        })











# =====================================================
# STOP
# =====================================================

@app.route(

    "/api/stop",

    methods=["POST"]

)

def api_stop():


    try:


        if bot_instance:


            bot_instance.stop()



        update_status({

            "bot":
                "STOPPED",


            "last_action":
                "STOP CLICK"

        })



        add_log(

            "STOP BUTTON CLICK"

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
                False

        })











# =====================================================
# MODE
# =====================================================

@app.route(

    "/api/mode",

    methods=["POST"]

)

def api_mode():


    data=request.get_json(

        silent=True

    ) or {}



    mode=data.get(

        "mode",

        "DEMO"

    ).upper()



    if mode not in [

        "DEMO",

        "LIVE"

    ]:


        return jsonify({

            "success":
                False

        })



    update_status({

        "mode":
            mode,


        "last_action":
            f"MODE {mode}"

    })



    add_log(

        f"MODE CHANGE {mode}"

    )



    try:


        from api.bybit_api import bybit_api


        bybit_api.create_session()



    except Exception as e:


        add_log(

            f"SESSION CHANGE ERROR {e}"

        )



    return jsonify({

        "success":
            True,

        "mode":
            mode

    })









# =====================================================
# SYMBOL
# =====================================================

@app.route(

    "/api/symbol",

    methods=["POST"]

)

def api_symbol():


    data=request.get_json(

        silent=True

    ) or {}



    symbol=data.get(

        "symbol",

        "BTCUSDT"

    ).upper()



    try:


        from api.bybit_api import bybit_api


        bybit_api.change_symbol(

            symbol

        )


    except Exception as e:


        add_log(

            f"SYMBOL ERROR {e}"

        )



    update_status({

        "symbol":
            symbol,


        "last_action":
            f"SYMBOL {symbol}"

    })



    add_log(

        f"SYMBOL CHANGE {symbol}"

    )



    return jsonify({

        "success":
            True,


        "symbol":
            symbol

    })











# =====================================================
# CLOSE
# =====================================================

@app.route(

    "/api/close",

    methods=["POST"]

)

def api_close():


    try:


        from order.order_manager import order_manager



        result = order_manager.close_position()



        update_status({

            "last_action":
                "CLOSE POSITION"

        })



        add_log(

            "CLOSE BUTTON CLICK"

        )



        return jsonify({

            "success":
                bool(result)

        })



    except Exception as e:


        add_log(

            f"CLOSE ERROR {e}"

        )


        return jsonify({

            "success":
                False

        })











# =====================================================
# SERVER
# =====================================================

def run_server():


    global server_started

    global _server_thread



    if server_started:

        return



    server_started=True





    def _run():


        app.run(

            host=WEB_HOST,

            port=WEB_PORT,

            debug=False,

            use_reloader=False,

            threaded=True

        )





    _server_thread=threading.Thread(

        target=_run,

        daemon=True,

        name="WebServer"

    )



    _server_thread.start()



    print(

        f"[WEB SERVER START] http://{WEB_HOST}:{WEB_PORT}"

    )



    add_log(

        "WEB SERVER STARTED"

    )











def stop_server():


    global server_started


    server_started=False


    add_log(

        "WEB SERVER STOP"

    )











# =====================================================
# EXPORT
# =====================================================

__all__=[


    "app",


    "run_server",


    "stop_server",


    "set_bot_instance",


    "update_status",


    "get_status",


    "get_trading_mode",


    "get_trading_symbol",


    "add_log"


]









if __name__=="__main__":


    run_server()


    while True:

        time.sleep(1)
