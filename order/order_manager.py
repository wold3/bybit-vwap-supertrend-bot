# =====================================================
# order_manager.py
# VWAP SUPERTREND BOT ORDER MANAGER
# =====================================================

import time

from api.bybit_api import bybit_api

from risk.risk_manager import risk_manager

from config import (
    TAKE_PROFIT_PERCENT,
    STOP_LOSS_PERCENT
)

from web.server import (
    add_log,
    update_status,
    get_trading_mode
)


class OrderManager:

    def __init__(self):

        self.last_order_time = 0
        self.cooldown = 3

        print("[ORDER MANAGER READY]")

    # =====================================================
    # ORDER CHECK
    # =====================================================

    def can_order(self):

        now = time.time()

        if now - self.last_order_time < self.cooldown:

            add_log("ORDER COOLDOWN")

            return False

        return True

    # =====================================================
    # OPEN POSITION
    # =====================================================

    def open_position(

        self,

        side,

        qty

    ):

        mode = get_trading_mode()

        print(

            "[OPEN ORDER]",

            mode,

            side,

            qty

        )

        if not self.can_order():

            return None

        # -----------------------------
        # Risk Check
        # -----------------------------

        if not risk_manager.allow_order(qty):

            add_log(

                "ORDER BLOCKED BY RISK"

            )

            return None

        try:

            # -----------------------------
            # Set Leverage
            # -----------------------------

            bybit_api.set_leverage()

            # -----------------------------
            # Market Order
            # -----------------------------

            result = bybit_api.place_order(

                side=side,

                qty=qty,

                reduce_only=False

            )

            if not result or not result.get("result"):

                add_log(

                    f"ORDER FAILED {side}"

                )

                return None

            self.last_order_time = time.time()

            add_log(

                f"ORDER SUCCESS {side} {qty}"

            )

            update_status({

                "position": side,

                "position_size": qty

            })

            # -----------------------------
            # TP / SL
            # -----------------------------

            self.set_tp_sl(side)

            return result

        except Exception as e:

            add_log(

                f"ORDER ERROR {e}"

            )

            return None

    # =====================================================
    # TP / SL
    # =====================================================

    def set_tp_sl(

        self,

        side

    ):

        try:

            price = bybit_api.get_price()

            if price is None:

                add_log(

                    "TP SL PRICE ERROR"

                )

                return False

            if side == "Buy":

                tp = round(

                    price *

                    (

                        1 +

                        TAKE_PROFIT_PERCENT / 100

                    ),

                    2

                )

                sl = round(

                    price *

                    (

                        1 -

                        STOP_LOSS_PERCENT / 100

                    ),

                    2

                )

            else:

                tp = round(

                    price *

                    (

                        1 -

                        TAKE_PROFIT_PERCENT / 100

                    ),

                    2

                )

                sl = round(

                    price *

                    (

                        1 +

                        STOP_LOSS_PERCENT / 100

                    ),

                    2

                )

            result = bybit_api.set_trading_stop(

                tp,

                sl

            )

            if result:

                add_log(

                    f"TP={tp} SL={sl}"

                )

                return True

            add_log(

                "TP SL FAILED"

            )

            return False

        except Exception as e:

            add_log(

                f"TP SL ERROR {e}"

            )

            return False



    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(self):

        try:

            result = bybit_api.close_position()

            if not result:

                add_log(

                    "POSITION CLOSE FAILED"

                )

                return None

            update_status(

                {

                    "position":

                        "NONE",

                    "position_size":

                        0

                }

            )

            self.last_order_time = time.time()

            add_log(

                "POSITION CLOSED"

            )

            return result

        except Exception as e:

            add_log(

                f"CLOSE ERROR {e}"

            )

            return None



    # =====================================================
    # FORCE CLOSE
    # =====================================================

    def emergency_close(self):

        add_log(

            "EMERGENCY CLOSE"

        )

        return self.close_position()



    # =====================================================
    # STATUS
    # =====================================================

    def status(self):

        return {

            "cooldown":

                self.cooldown,

            "last_order":

                self.last_order_time

        }


# =====================================================
# INSTANCE
# =====================================================

order_manager = OrderManager()
