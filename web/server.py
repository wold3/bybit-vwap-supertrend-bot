# =====================================================
# web/server.py
# VWAP SUPERTREND BOT V2
# FLASK CONTROL SERVER
# =====================================================


from flask import (

    Flask,

    jsonify,

    request

)


import threading
import time



import config






# =====================================================
# FLASK APP
# =====================================================


app = Flask(__name__)







# =====================================================
# GLOBAL DATA
# =====================================================


_bot = None



_logs = []



_status = {


    "bot":

    "STOPPED",



    "position":

    "NONE",



    "symbol":

    config.SYMBOL,



    "profit_percent":

    0,



    "leverage":

    config.LEVERAGE


}







_settings = {


    "symbol":

    config.SYMBOL,


    "leverage":

    config.LEVERAGE,


    "stop_loss":

    config.STOP_LOSS_PERCENT,



    "tp1":

    config.TP1_PERCENT,



    "tp2":

    config.TP2_PERCENT,



    "tp3":

    config.TP3_PERCENT



}









# =====================================================
# BOT CONNECT
# =====================================================


def set_bot(bot):


    global _bot


    _bot = bot



    add_log(

        "BOT CONNECTED"

    )









# =====================================================
# LOG
# =====================================================


def add_log(msg):


    try:


        timestamp=time.strftime(

            "%H:%M:%S"

        )



        text=f"[{timestamp}] {msg}"



        _logs.append(text)



        if len(_logs)>500:


            del _logs[:-500]



        print(text)




    except:


        pass










# =====================================================
# STATUS UPDATE
# =====================================================


def update_status(data):


    try:


        _status.update(

            data

        )


    except Exception as e:


        add_log(

            f"STATUS ERROR {e}"

        )









# =====================================================
# GET SYMBOL
# =====================================================


def get_trading_symbol():


    return _settings.get(

        "symbol",

        config.SYMBOL

    )









# =====================================================
# GET MODE
# =====================================================


def get_trading_mode():


    try:


        return config.MODE



    except:


        return "DEMO"










# =====================================================
# INDEX
# =====================================================


@app.route("/")


def index():


    return jsonify({


        "server":

        "VWAP SUPERTREND BOT",



        "status":

        "running"



    })

# =====================================================
# STATUS API
# =====================================================


@app.route("/api/status")


def api_status():


    return jsonify({


        "logs":

        _logs[-100:],



        "status":

        _status,



        "settings":

        _settings



    })









# =====================================================
# CANDLE API
# =====================================================


@app.route("/api/candles")


def api_candles():


    try:


        if _bot:


            data = _bot.market_data.get_candles()



            if data is not None:


                return data.to_json()



        return jsonify({


            "result":{


                "list":[]


            }


        })




    except Exception as e:


        add_log(

            f"CANDLE ERROR {e}"

        )


        return jsonify({


            "result":{


                "list":[]


            }


        })











# =====================================================
# ORDER API
# =====================================================


@app.route(

    "/api/order",

    methods=["POST"]

)


def api_order():


    try:


        data=request.json or {}



        side=data.get(

            "side"

        )



        qty=data.get(

            "qty"

        )





        if not _bot:


            return jsonify({


                "error":

                "BOT OFFLINE"


            })







        if side=="Buy":


            result=_bot.buy(

                qty

            )



        elif side=="Sell":


            result=_bot.sell(

                qty

            )



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
# CLOSE API
# =====================================================


@app.route(

    "/api/close",

    methods=["POST"]

)


def api_close():


    try:


        if not _bot:


            return jsonify(False)



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
# LEVERAGE API
# =====================================================


@app.route(

    "/api/leverage",

    methods=["POST"]

)


def api_leverage():


    try:


        data=request.json or {}



        leverage=int(

            data.get(

                "leverage",

                config.LEVERAGE

            )

        )





        if leverage < 1:


            leverage=1



        if leverage > 100:


            leverage=100





        _settings["leverage"]=leverage



        config.LEVERAGE=leverage





        if _bot:


            result=_bot.set_leverage()


        else:


            result=False





        update_status({


            "leverage":

            leverage



        })



        add_log(

            f"LEVERAGE CHANGE {leverage}X"

        )





        return jsonify({


            "result":

            result,


            "leverage":

            leverage



        })





    except Exception as e:


        return jsonify({


            "error":

            str(e)



        })

# =====================================================
# STOP LOSS API
# =====================================================


@app.route(

    "/api/stoploss",

    methods=["POST"]

)


def api_stoploss():


    try:


        data=request.json or {}



        percent=float(

            data.get(

                "percent",

                config.STOP_LOSS_PERCENT

            )

        )



        _settings["stop_loss"]=percent



        config.STOP_LOSS_PERCENT=percent




        add_log(

            f"STOP LOSS {percent}%"

        )



        return jsonify({


            "stop_loss":

            percent



        })





    except Exception as e:


        return jsonify({


            "error":

            str(e)



        })











# =====================================================
# TAKE PROFIT API
# =====================================================


@app.route(

    "/api/takeprofit",

    methods=["POST"]

)


def api_takeprofit():


    try:


        data=request.json or {}



        tp1=float(

            data.get(

                "tp1",

                config.TP1_PERCENT

            )

        )



        tp2=float(

            data.get(

                "tp2",

                config.TP2_PERCENT

            )

        )



        tp3=float(

            data.get(

                "tp3",

                config.TP3_PERCENT

            )

        )





        _settings["tp1"]=tp1

        _settings["tp2"]=tp2

        _settings["tp3"]=tp3



        config.TP1_PERCENT=tp1

        config.TP2_PERCENT=tp2

        config.TP3_PERCENT=tp3





        add_log(

            f"TP SET {tp1}/{tp2}/{tp3}"

        )



        return jsonify({


            "tp1":

            tp1,


            "tp2":

            tp2,


            "tp3":

            tp3



        })




    except Exception as e:


        return jsonify({


            "error":

            str(e)



        })









# =====================================================
# SETTINGS API
# =====================================================


@app.route(

    "/api/settings",

    methods=["POST"]

)


def api_settings():


    try:


        data=request.json or {}



        _settings.update(

            data

        )



        if "symbol" in data:


            _settings["symbol"]=data["symbol"].upper()



            update_status({


                "symbol":

                _settings["symbol"]



            })







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
# BOT START
# =====================================================


@app.route(

    "/api/start",

    methods=["POST"]

)


def api_start():


    try:


        if not _bot:


            return jsonify(False)



        result=_bot.start()



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
# BOT STOP
# =====================================================


@app.route(

    "/api/stop",

    methods=["POST"]

)


def api_stop():


    try:


        if not _bot:


            return jsonify(False)



        result=_bot.stop()



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
# SERVER RUN
# =====================================================


def run_server():


    add_log(

        "WEB SERVER START"

    )



    app.run(


        host=config.HOST,


        port=config.PORT,


        debug=False,


        use_reloader=False



    )

