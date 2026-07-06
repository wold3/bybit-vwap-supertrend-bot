import logging

from api.bybit_api import (
    close_position,
    get_last_price,
    get_position,
    get_unrealized_pnl,
)
from database.repository import (
    delete_position,
    save_position,
    update_position_price,
)

logger = logging.getLogger(__name__)


class PositionManager:

    def sync(self, symbol):

        position = get_position(symbol)

        if position is None:

            delete_position(symbol)

            return None

        size = float(position.get("size", 0))

        if size == 0:

            delete_position(symbol)

            return None

        side = position["side"]

        entry_price = float(
            position["avgPrice"]
        )

        leverage = int(
            float(position["leverage"])
        )

        save_position(
            symbol=symbol,
            side=side,
            qty=size,
            entry_price=entry_price,
            leverage=leverage,
        )

        pnl = get_unrealized_pnl(symbol)

        price = get_last_price(symbol)

        update_position_price(
            symbol,
            price,
            pnl,
        )

        return get_position(symbol)

    def close(self, symbol):

        return close_position(symbol)

    def is_open(self, symbol):

        position = get_position(symbol)

        if position is None:
            return False

        return float(
            position.get("size", 0)
        ) > 0

    def pnl(self, symbol):

        return get_unrealized_pnl(symbol)


position_manager = PositionManager()
