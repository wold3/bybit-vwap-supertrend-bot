# =====================================================
# web/server.py
# Dashboard Server
# =====================================================

import threading
import json
import os


from http.server import (
    HTTPServer,
    SimpleHTTPRequestHandler
)





HOST = "0.0.0.0"

PORT = 8000





STATUS = {

    "bot":
        "STOPPED",

    "symbol":
        "",

    "price":
        0,

    "vwap":
        0,

    "trend":
        "NONE",

    "volume":
        False,

    "signal":
        "NONE",

    "position":
        "NONE"

}





LOGS = []





SERVER = None






# =====================================================
# UPDATE STATUS
# =====================================================


def update_status(data):


    STATUS.update(data)






# =====================================================
# ADD LOG
# =====================================================


def add_log(message):


    LOGS.append(

        str(message)

    )


    if len(LOGS) > 100:

        LOGS.pop(0)







# =====================================================
# HTTP HANDLER
# =====================================================


class DashboardHandler(
    SimpleHTTPRequestHandler
):


    def do_GET(self):


        if self.path == "/api/status":


            self.send_response(200)


            self.send_header(

                "Content-type",

                "application/json"

            )


            self.end_headers()



            self.wfile.write(

                json.dumps(

                    {

                        "status":

                            STATUS,


                        "logs":

                            LOGS

                    },

                    ensure_ascii=False

                ).encode()

            )


            return







        if self.path == "/":


            self.path = "/dashboard.html"




        return super().do_GET()







# =====================================================
# START SERVER
# =====================================================


def start_dashboard():


    global SERVER



    if SERVER:

        return





    def run():


        global SERVER



        try:


            SERVER = HTTPServer(

                (

                    HOST,

                    PORT

                ),

                DashboardHandler

            )


            print(

                "[WEB SERVER START]",

                PORT

            )



            SERVER.serve_forever()



        except Exception as e:


            print(

                "[WEB SERVER ERROR]",

                e

            )







    thread = threading.Thread(

        target=run,

        daemon=True

    )


    thread.start()
