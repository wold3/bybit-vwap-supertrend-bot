# =====================================================
# web/server.py
# VWAP SUPERTREND BOT DASHBOARD SERVER
# =====================================================

from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

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



status_lock = threading.Lock()

log_lock = threading.Lock()



status = {


    "mode":"DEMO",

    "bot":"STOPPED",

    "position":"NONE",

    "position_size":0,

    "entry_price":0,

    "pnl":0,

    "price":0,

    "balance":0,

    "signal":"NONE",

    "watchdog":"OFF"

}




logs=[]







# =====================================================
# LOG
# =====================================================

def add_log(message):


    text = (

        "[" +

        time.strftime("%H:%M:%S")

        +

        "] "

        +

        str(message)

    )


    print(text)



    with log_lock:


        logs.append(text)



        if len(logs)>MAX_LOGS:


            logs.pop(0)








# =====================================================
# STATUS
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









def get_trading_mode():


    with status_lock:


        return status["mode"]







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


        data_logs = logs[-100:]



    return jsonify({


        "status":

            get_status(),


        "logs":

            data_logs


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


        if bot_instance is None:


            return jsonify({

                "success":False,

                "message":

                    "BOT NOT READY"

            })




        bot_instance.start()



        update_status({

            "bot":

            "RUNNING"

        })



        add_log(

            "BOT START"

        )



        return jsonify({

            "success":True

        })




    except Exception as e:


        add_log(

            f"START ERROR {e}"

        )


        return jsonify({

            "success":False

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

            "STOPPED"

        })



        add_log(

            "BOT STOP"

        )



        return jsonify({

            "success":True

        })



    except Exception as e:


        add_log(

            f"STOP ERROR {e}"

        )


        return jsonify({

            "success":False

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

            "success":False

        })





    update_status({

        "mode":

        mode

    })




    add_log(

        f"MODE CHANGE {mode}"

    )




    try:


        from api.bybit_api import bybit_api

        from services.private_ws import private_ws



        bybit_api.change_session(

            mode

        )



        if private_ws.running:


            private_ws.restart()



    except Exception as e:


        add_log(

            f"MODE ERROR {e}"

        )





    return jsonify({

        "success":True,

        "mode":mode

    })









# =====================================================
# MANUAL ORDER
# =====================================================

@app.route(

    "/api/order",

    methods=["POST"]

)

def api_order():


    try:



        data=request.get_json(

            silent=True

        ) or {}



        side=data.get(

            "side",

            ""

        )




        if side not in [

            "Buy",

            "Sell"

        ]:


            return jsonify({

                "success":False,

                "message":

                "INVALID SIDE"

            })





        from order.order_manager import order_manager



        result = order_manager.open_position(

            side,

            None

        )



        if result:


            add_log(

                f"MANUAL ORDER {side}"

            )


            return jsonify({

                "success":True,

                "message":

                "ORDER SUCCESS"

            })




        return jsonify({

            "success":False,

            "message":

            "ORDER FAILED"

        })





    except Exception as e:


        add_log(

            f"ORDER API ERROR {e}"

        )


        return jsonify({

            "success":False

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



        return jsonify({

            "success":

            bool(result)

        })



    except Exception as e:


        add_log(

            f"CLOSE ERROR {e}"

        )



        return jsonify({

            "success":False

        })









# =====================================================
# RESET
# =====================================================

@app.route(

    "/api/reset",

    methods=["POST"]

)

def api_reset():


    update_status({

        "position":"NONE",

        "position_size":0,

        "entry_price":0,

        "pnl":0,

        "signal":"NONE"

    })



    add_log(

        "STATUS RESET"

    )



    return jsonify({

        "success":True

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



        return jsonify({

            "success":True

        })



    except Exception as e:


        add_log(

            f"RESTART ERROR {e}"

        )


        return jsonify({

            "success":False

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

        daemon=True,

        name="WebServer"

    )


    _server_thread.start()



    add_log(

        "WEB SERVER READY"

    )









# =====================================================
# EXPORT
# =====================================================

__all__=[


    "app",

    "run_server",

    "set_bot_instance",

    "add_log",

    "update_status",

    "get_status",

    "get_trading_mode"

]
