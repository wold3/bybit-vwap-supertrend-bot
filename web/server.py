# =====================================================
# web/server.py
# VWAP SUPERTREND BOT WEB SERVER
# =====================================================

from flask import Flask, jsonify, request, render_template

import threading
import time



app = Flask(
    __name__,
    template_folder="templates"
)





# =====================================================
# GLOBAL DATA
# =====================================================

lock = threading.Lock()


logs = []


trading_mode = "DEMO"


trading_symbol = "BTCUSDT"



status = {

    "bot": "STOPPED",

    "mode": "DEMO",

    "symbol": "BTCUSDT",

    "position": "NONE",

    "position_size": 0,

    "entry_price": 0,

    "mark_price": 0,

    "liq_price": 0,

    "pnl": 0,

    "last_action": "READY"

}



bot_instance = None





# =====================================================
# BOT INSTANCE
# =====================================================

def set_bot(bot):

    global bot_instance

    bot_instance = bot






# =====================================================
# LOG
# =====================================================

def add_log(message):

    now = time.strftime("%H:%M:%S")

    text = f"[{now}] {message}"


    print(text)



    with lock:

        logs.append(text)


        if len(logs) > 300:

            logs.pop(0)


        status["last_action"] = message







# =====================================================
# STATUS UPDATE
# =====================================================

def update_status(data):

    with lock:

        status.update(data)







# =====================================================
# GET SETTINGS
# =====================================================

def get_trading_mode():

    return trading_mode





def get_trading_symbol():

    return trading_symbol







# =====================================================
# HOME
# =====================================================

@app.route("/")

def home():

    return render_template(
        "index.html"
    )








# =====================================================
# STATUS API
# =====================================================

@app.route("/api/status")

def api_status():


    with lock:


        return jsonify({

            "status": status.copy(),

            "logs": logs.copy()

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

            "bot":"RUNNING"

        })


        add_log(

            "BUTTON START"

        )


        return jsonify({

            "ok":True

        })



    except Exception as e:


        add_log(

            f"START ERROR {e}"

        )


        return jsonify({

            "ok":False

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

            "bot":"STOPPED"

        })


        add_log(

            "BUTTON STOP"

        )


        return jsonify({

            "ok":True

        })



    except Exception as e:


        add_log(

            f"STOP ERROR {e}"

        )


        return jsonify({

            "ok":False

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



        add_log(

            "BUTTON CLOSE"

        )


        return jsonify({

            "ok":bool(result)

        })



    except Exception as e:


        add_log(

            f"CLOSE ERROR {e}"

        )


        return jsonify({

            "ok":False

        })









# =====================================================
# REVERSE
# =====================================================

@app.route(
    "/api/reverse",
    methods=["POST"]
)

def api_reverse():


    try:


        from order.order_manager import order_manager



        result = order_manager.reverse_position()



        add_log(

            "BUTTON REVERSE"

        )



        return jsonify({

            "ok":bool(result)

        })



    except Exception as e:


        add_log(

            f"REVERSE ERROR {e}"

        )


        return jsonify({

            "ok":False

        })









# =====================================================
# MODE
# =====================================================

@app.route(
    "/api/mode",
    methods=["POST"]
)

def api_mode():


    global trading_mode



    data=request.json or {}



    mode=data.get(

        "mode",

        "DEMO"

    )



    if mode not in [

        "DEMO",

        "LIVE"

    ]:


        return jsonify({

            "ok":False

        })



    trading_mode = mode



    update_status({

        "mode":mode

    })


    add_log(

        f"MODE SWITCH {mode}"

    )



    return jsonify({

        "ok":True

    })









# =====================================================
# SYMBOL
# =====================================================

@app.route(
    "/api/symbol",
    methods=["POST"]
)

def api_symbol():


    global trading_symbol



    data=request.json or {}



    symbol=data.get(

        "symbol",

        "BTCUSDT"

    ).upper()



    trading_symbol = symbol



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

        "symbol":symbol

    })



    add_log(

        f"MARKET SYMBOL SWITCH {symbol}"

    )



    return jsonify({

        "ok":True,

        "symbol":symbol

    })









# =====================================================
# SERVER
# =====================================================

def run_server():


    app.run(

        host="0.0.0.0",

        port=8000,

        debug=False,

        use_reloader=False

    )
