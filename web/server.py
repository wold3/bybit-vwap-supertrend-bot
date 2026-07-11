# =====================================================
# web/server.py
# WEB DASHBOARD SERVER
# =====================================================

from flask import (
    Flask,
    render_template,
    jsonify,
    request
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

bot_instance = None



trading_mode = "DEMO"



status = {


    "mode":

        "DEMO",


    "bot":

        "STOPPED",


    "position":

        "NONE",


    "position_size":

        0,


    "entry_price":

        0,


    "pnl":

        0


}



logs = []



server_started = False









# =====================================================
# LOG
# =====================================================

def add_log(message):


    now = time.strftime(

        "%H:%M:%S"

    )


    text = (

        f"[{now}] {message}"

    )


    print(text)



    logs.append(text)



    if len(logs) > 200:

        logs.pop(0)









# =====================================================
# STATUS UPDATE
# =====================================================

def update_status(data):


    status.update(

        data

    )








# =====================================================
# BOT INSTANCE
# =====================================================

def set_bot_instance(bot):


    global bot_instance


    bot_instance = bot









# =====================================================
# MODE
# =====================================================

def get_trading_mode():


    return trading_mode







# =====================================================
# HOME
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


    return jsonify({


        "status":

            status,


        "logs":

            logs[-100:]


    })









# =====================================================
# MODE CHANGE
# =====================================================

@app.route(

    "/api/mode",

    methods=["POST"]

)

def api_mode():


    global trading_mode



    data = request.json



    mode = data.get(

        "mode",

        "DEMO"

    ).upper()





    if mode not in [

        "DEMO",

        "LIVE"

    ]:


        return jsonify({

            "error":

                "invalid mode"

        })






    trading_mode = mode



    status["mode"] = mode





    add_log(

        f"MODE CHANGE : {mode}"

    )






    # Bybit Session 변경

    try:


        from api.bybit_api import bybit_api


        bybit_api.change_session(

            mode

        )



    except Exception as e:


        add_log(

            f"MODE API ERROR {e}"

        )





    return jsonify({

        "success":

            True,


        "mode":

            mode

    })











# =====================================================
# START
# =====================================================

@app.route(

    "/api/start",

    methods=["POST"]

)

def api_start():


    global bot_instance



    try:


        if bot_instance:


            bot_instance.start()



            add_log(

                "BOT START"

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


    global bot_instance



    try:


        if bot_instance:


            bot_instance.stop()



            add_log(

                "BOT STOP"

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
# CLOSE POSITION
# =====================================================

@app.route(

    "/api/close",

    methods=["POST"]

)

def api_close():


    try:


        from order.order_manager import order_manager



        result = order_manager.close_position()



        add_log(

            "MANUAL CLOSE"

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
# SERVER THREAD
# =====================================================

def run_server():


    global server_started



    if server_started:


        return



    server_started = True



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
