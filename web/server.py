# =====================================================
# web/server.py
# VWAP SUPERTREND BOT V3
# FLASK WEB SERVER
# =====================================================


from flask import (
    Flask,
    jsonify,
    request,
    render_template
)

import threading


from config import SYMBOL





# =====================================================
# APP
# =====================================================


app = Flask(

    __name__

)






# =====================================================
# GLOBAL
# =====================================================


_bot = None



_logs = []



_status = {


    "bot":"STOPPED",

    "symbol":SYMBOL,

    "position":"NONE",

    "position_size":0,

    "mark_price":0,

    "entry_price":0,

    "pnl":0,

    "last_action":"READY"

}



_settings = {


    "symbol":SYMBOL,

    "leverage":100,

    "stop_loss":2,

    "take_profit":5

}









# =====================================================
# LOG
# =====================================================


def add_log(message):


    from datetime import datetime


    text = (

        datetime.now()

        .strftime("%H:%M:%S")

        +

        " "

        +

        str(message)

    )



    print(text)



    _logs.append(text)



    if len(_logs)>300:


        del _logs[0]








# =====================================================
# STATUS UPDATE
# =====================================================


def update_status(data):


    _status.update(data)








# =====================================================
# BOT CONNECT
# =====================================================


def set_bot(bot):


    global _bot


    _bot = bot







def get_bot():


    return _bot







# =====================================================
# SYMBOL
# =====================================================


def get_trading_symbol():


    return _settings.get(

        "symbol",

        SYMBOL

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


    return jsonify({


        "logs":

        _logs[-100:],



        "status":

        _status



    })









# =====================================================
# CANDLE API
# =====================================================


@app.route("/api/candles")

def api_candles():


    try:


        if _bot:


            data = _bot.market_data.get_candles()



            return jsonify(data.to_dict())





        return jsonify({})



    except Exception as e:


        add_log(

            f"CANDLE ERROR {e}"

        )


        return jsonify({})









# =====================================================
# START
# =====================================================


@app.route(

    "/api/start",

    methods=["POST"]

)

def api_start():


    try:


        if _bot:


            result = _bot.start()


            return jsonify({

                "result":

                result

            })



        return jsonify({

            "error":

            "BOT NONE"

        })



    except Exception as e:


        return jsonify({

            "error":

            str(e)

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


        if _bot:


            result=_bot.stop()


            return jsonify({

                "result":

                result

            })



        return jsonify({

            "error":

            "BOT NONE"

        })



    except Exception as e:


        return jsonify({

            "error":

            str(e)

        })









# =====================================================
# ORDER
# =====================================================


@app.route(

    "/api/order",

    methods=["POST"]

)

def api_order():


    try:


        data=request.json



        side=data.get(

            "side"

        )


        qty=data.get(

            "qty"

        )




        if not _bot:


            return jsonify({

                "error":

                "BOT OFF"

            })





        if side=="Buy":


            result=_bot.buy(qty)



        elif side=="Sell":


            result=_bot.sell(qty)



        else:


            return jsonify({

                "error":

                "INVALID SIDE"

            })




        return jsonify({

            "result":

            result

        })



    except Exception as e:


        add_log(

            f"ORDER API ERROR {e}"

        )


        return jsonify({

            "error":

            str(e)

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


        result=_bot.close()



        return jsonify({

            "result":

            result

        })



    except Exception as e:


        return jsonify({

            "error":

            str(e)

        })









# =====================================================
# LEVERAGE
# =====================================================


@app.route(

    "/api/leverage",

    methods=["POST"]

)

def api_leverage():


    try:


        data=request.json



        value=int(

            data.get(

                "leverage",

                100

            )

        )



        if value>100:


            value=100





        _settings["leverage"]=value





        result=_bot.set_leverage()



        return jsonify({

            "result":

            result

        })



    except Exception as e:


        return jsonify({

            "error":

            str(e)

        })









# =====================================================
# SETTINGS
# =====================================================


@app.route(

    "/api/settings",

    methods=["POST"]

)

def api_settings():


    try:


        data=request.json



        _settings.update(

            data

        )



        if "symbol" in data:


            from api.bybit_api import bybit_api


            bybit_api.change_symbol(

                data["symbol"]

            )




        add_log(

            "SETTINGS UPDATED"

        )



        return jsonify({

            "settings":

            _settings

        })



    except Exception as e:


        return jsonify({

            "error":

            str(e)

        })









# =====================================================
# MODE
# =====================================================


def get_trading_mode():


    try:


        from config import MODE


        return MODE



    except:


        return "DEMO"









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
