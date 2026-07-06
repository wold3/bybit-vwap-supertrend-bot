import requests
import time
import os
import hmac
import hashlib

from portfolio.position_manager import position_manager


class PositionSync:

    def __init__(self):

        self.api_key = os.getenv("BYBIT_API_KEY")
        self.api_secret = os.getenv("BYBIT_API_SECRET")
        self.base_url = "https://api.bybit.com"

    # =================================================
    # FETCH BYBIT POSITION
    # =================================================
    def fetch_positions(self):

        endpoint = "/v5/position/list"

        timestamp = str(int(time.time() * 1000))

        params = {
            "category": "linear",
            "timestamp": timestamp,
            "api_key": self.api_key,
            "recv_window": "5000"
        }

        query = "&".join([f"{k}={params[k]}" for k in sorted(params)])

        signature = hmac.new(
            self.api_secret.encode(),
            query.encode(),
            hashlib.sha256
        ).hexdigest()

        params["sign"] = signature

        url = self.base_url + endpoint

        res = requests.get(url, params=params, timeout=5)

        return res.json()

    # =================================================
    # SYNC TO LOCAL
    # =================================================
    def sync(self):

        try:
            data = self.fetch_positions()

            if data.get("retCode") != 0:
                print("[SYNC ERROR]", data)
                return

            positions = data["result"]["list"]

            # reset local
            position_manager.positions = {}

            for p in positions:

                symbol = p["symbol"]
                size = float(p["size"])
                side = p["side"]
                entry = float(p["avgPrice"])

                if size == 0:
                    continue

                position_manager.positions[symbol] = {
                    "side": side,
                    "qty": size,
                    "entry_price": entry
                }

            print("[SYNC] COMPLETED")

        except Exception as e:
            print("[SYNC ERROR]", e)


# SINGLETON
position_sync = PositionSync()
