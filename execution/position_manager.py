from datetime import datetime

from api.bybit_api import (
    close_position,
    get_position,
    get_unrealized_pnl,
    get_last_price,
)

from database.repository import (
    save_position,
    delete_position,
    update_position_price,
    get_positions,
)

from execution.execution_guard import execution_guard

from services.logger_service import logger
from services.telegram_service import send_error, send_message


class PositionManager:

    def __init__(self):
        self.last_sync = None

    def sync(self, symbol):

        try:

            logger.info("Sync %s", symbol)

            position = get_position(symbol)

            if not position:
                delete_position(symbol)
                return None

            size = float(position.get("size", 0))

            if size == 0:
                delete_position(symbol)
                return None

            save_position(
                symbol=symbol,
                side=position.get("side"),
                qty=size,
                entry_price=float(position.get("avgPrice", 0)),
                leverage=int(float(position.get("leverage", 1))),
            )

            update_position_price(
                symbol=symbol,
                mark_price=get_last_price(symbol),
                unrealized_pnl=get_unrealized_pnl(symbol),
            )

            self.last_sync = datetime.utcnow()

            return get_position(symbol)

        except Exception as e:
            logger.exception(e)
            send_error(str(e))
            return None

    def close(self, symbol):

        try:

            result = close_position(symbol)

            send_message(f"CLOSE | {symbol}")

            execution_guard.clear_symbol(symbol)

            return result

        except Exception as e:
            logger.exception(e)
            send_error(str(e))
            return False

    def close_all(self):

        try:

            positions = get_positions()

            results = []

            for p in positions:

                symbol = p.get("symbol")
                results.append(close_position(symbol))
                execution_guard.clear_symbol(symbol)

            send_message("ALL POSITIONS CLOSED")

            return results

        except Exception as e:
            logger.exception(e)
            send_error(str(e))
            return []

    def summary(self, symbol):

        pos = get_position(symbol)

        if not pos:
            return {"symbol": symbol, "open": False}

        return {
            "symbol": symbol,
            "open": True,
            "side": pos.get("side"),
            "size": pos.get("size"),
            "entry": pos.get("avgPrice"),
            "pnl": get_unrealized_pnl(symbol),
        }

    def health(self):

        return {
            "engine": "PositionManager",
            "last_sync": (
                self.last_sync.isoformat()
                if self.last_sync
                else None
            ),
        }


position_manager = PositionManager()
