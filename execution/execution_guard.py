import time
import threading
from services.logger_service import logger


class ExecutionGuard:

    def __init__(self):

        self.lock = threading.Lock()
        self.last_order_time = 0
        self.min_interval = 2  # seconds
        self.recent_symbols = set()

    # -----------------------------------
    # 1. Global Lock
    # -----------------------------------

    def acquire(self):

        return self.lock.acquire(blocking=False)

    def release(self):

        if self.lock.locked():
            self.lock.release()

    # -----------------------------------
    # 2. Rate Limit
    # -----------------------------------

    def rate_limit(self):

        now = time.time()

        if now - self.last_order_time < self.min_interval:
            logger.warning("Rate limit blocked")
            return False

        self.last_order_time = now
        return True

    # -----------------------------------
    # 3. Duplicate Symbol Block
    # -----------------------------------

    def allow_symbol(self, symbol):

        if symbol in self.recent_symbols:
            logger.warning("Duplicate symbol blocked: %s", symbol)
            return False

        self.recent_symbols.add(symbol)
        return True

    def clear_symbol(self, symbol):

        if symbol in self.recent_symbols:
            self.recent_symbols.remove(symbol)


# Singleton
execution_guard = ExecutionGuard()
