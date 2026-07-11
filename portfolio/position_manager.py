# =====================================================
# portfolio/position_manager.py
# POSITION MANAGER
# =====================================================

import threading
import time

from api.bybit_api import bybit_api

from web.server import (
    add_log,
    update_status
)


class PositionManager:

    def __init__(self):

        self.lock = threading.Lock()

        self.position = {

            "symbol": "",

            "side": "NONE",

            "size": 0.0,

            "entry_price": 0.0,

            "mark_price": 0.0,

            "liq_price": 0.0,

            "unrealised_pnl": 0.0,

            "updated": 0

        }

        print(

            "[POSITION MANAGER READY]"

        )

    # =====================================================
    # UPDATE FROM API
    # =====================================================

    def refresh(self):

        try:

            data = bybit_api.get_position()

            if not data:

                return False

            rows = data["result"]["list"]

            if not rows:

                return False

            p = rows[0]

            with self.lock:

                self.position["symbol"] = p["symbol"]

                self.position["side"] = p["side"] if p["side"] else "NONE"

                self.position["size"] = float(p["size"])

                self.position["entry_price"] = float(p["avgPrice"] or 0)

                self.position["mark_price"] = float(p["markPrice"] or 0)

                self.position["liq_price"] = float(p["liqPrice"] or 0)

                self.position["unrealised_pnl"] = float(

                    p["unrealisedPnl"] or 0

                )

                self.position["updated"] = time.time()

            update_status(self.position)

            return True

        except Exception as e:

            add_log(

                f"POSITION REFRESH ERROR {e}"

            )

            return False

    # =====================================================
    # GET POSITION
    # =====================================================

    def get_position(self):

        with self.lock:

            return self.position.copy()

    # =====================================================
    # HAS POSITION
    # =====================================================

    def has_position(self):

        with self.lock:

            return self.position["size"] > 0



    # =====================================================
    # IS LONG
    # =====================================================

    def is_long(self):

        with self.lock:

            return (

                self.position["side"] == "Buy"

                and

                self.position["size"] > 0

            )



    # =====================================================
    # IS SHORT
    # =====================================================

    def is_short(self):

        with self.lock:

            return (

                self.position["side"] == "Sell"

                and

                self.position["size"] > 0

            )



    # =====================================================
    # UPDATE FROM REST API
    # =====================================================

    def refresh(self):

        try:

            from api.bybit_api import bybit_api

            result = bybit_api.get_position()

            if not result:

                return False

            rows = result["result"]["list"]

            if not rows:

                return False

            self.update(rows)

            return True

        except Exception as e:

            add_log(

                f"POSITION REFRESH ERROR {e}"

            )

            return False



    # =====================================================
    # STATUS
    # =====================================================

    def status(self):

        with self.lock:

            return {

                "side":

                    self.position["side"],

                "size":

                    self.position["size"],

                "entry_price":

                    self.position["entry_price"],

                "pnl":

                    self.position["pnl"]

            }



    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        with self.lock:

            self.position = {

                "side": "NONE",

                "size": 0.0,

                "entry_price": 0.0,

                "pnl": 0.0

            }

        update_status({

            "position": "NONE",

            "position_size": 0,

            "entry_price": 0,

            "pnl": 0

        })

        add_log(

            "POSITION RESET"

        )



    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        try:

            self.reset()

            print(

                "[POSITION MANAGER CLOSED]"

            )

        except Exception as e:

            print(

                "[POSITION CLOSE ERROR]",

                e

            )


# =====================================================
# INSTANCE
# =====================================================

position_manager = PositionManager()
