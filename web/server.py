# =====================================================
# web/server.py
# VWAP SUPERTREND BOT DASHBOARD SERVER
# =====================================================

from flask import Flask, render_template, jsonify, request

import threading
import time


from config import WEB_HOST, WEB_PORT


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



status_lock = threading.Lock()

log_lock = threading.Lock()



# =====================================================
# STATUS
# =====================================================


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


    "vwap":

        0,


    "trend":

        "NONE",


    "signal":

        "NONE",


    "watchdog":

        "OFF",


    "last_action":

        "SYSTEM READY"

}



logs=[]




# =====================================================
# LOG
# =====================================================


def add_log(message):


    text = (

        f"[{time.strftime('%H:%M:%S')}] "

        f"{message}"

    )


    print(text)



    with log_lock:


        logs.append(text)



        if len(logs)>MAX_LOGS:


            logs.pop(0)









# =====================================================
# STATUS CONTROL
# =====================================================


def update_status(data):


    if not data:

        return



    with status_lock:


        status.update(data)






def get_status():


    with status_lock:


        return status.copy()







# =====================================================
# BOT INSTANCE
# =====================================================


def set_bot_instance(bot):


    global bot_instance


    bot_instance=bot



    add_log(

        "BOT INSTANCE CONNECTED"

    )









# =====================================================
# MODE
# =====================================================


def get_trading_mode():


    return status.get(

        "mode",

        "DEMO"

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
# STATUS API
# =====================================================


@app.route("/api/status")

def api_status():


    with log_lock:


        log_copy=logs[-100:]



    return jsonify({


        "status":

            get_status(),



        "logs":

            log_copy


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

                "START BUTTON CLICK"

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

                "STOP BUTTON CLICK"

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
# RESTART
# =====================================================


@app.route(

    "/api/restart",

    methods=["POST"]

)

def api_restart():


    try:


        if bot_instance:


            bot_instance.stop()


            time.sleep(1)


            bot_instance.start()



        update_status({

            "bot":

                "RUNNING",


            "last_action":

                "RESTART BUTTON CLICK"

        })



        add_log(

            "RESTART BUTTON CLICK"

        )



        return jsonify({

            "success":

                True

        })



    except Exception as e:


        add_log(

            f"RESTART ERROR {e}"

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

            f"MODE ERROR {e}"

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

        "symbol"

    )



    if not symbol:


        return jsonify({

            "success":

                False

        })





    symbol=symbol.upper()



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

            f"SYMBOL CHANGE {symbol}"

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
# CLOSE POSITION
# =====================================================


@app.route(

    "/api/close",

    methods=["POST"]

)

def api_close():


    try:


        from order.order_manager import order_manager



        result=order_manager.close_position()



        update_status({

            "last_action":

                "CLOSE BUTTON CLICK"

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
# LOG
# =====================================================


@app.route("/api/logs")

def api_logs():


    with log_lock:


        return jsonify({

            "logs":

                logs.copy()

        })









# =====================================================
# SERVER START
# =====================================================


def run_server():


    global server_started


    global _server_thread



    if server_started:

        return



    server_started=True





    def run():


        app.run(

            host=WEB_HOST,

            port=WEB_PORT,

            debug=False,

            use_reloader=False,

            threaded=True

        )





    _server_thread=threading.Thread(

        target=run,

        daemon=True

    )



    _server_thread.start()



    add_log(

        "WEB SERVER STARTED"

    )









# =====================================================
# EXPORT
# =====================================================


__all__=[


    "app",

    "run_server",

    "set_bot_instance",

    "update_status",

    "get_status",

    "add_log",

    "get_trading_mode"

]





if __name__=="__main__":


    run_server()


    while True:


        time.sleep(1)
