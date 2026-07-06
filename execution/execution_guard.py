import time
import threading


class ExecutionGuard:

    def __init__(self, cooldown_sec: int = 3):

        self.cooldown_sec = cooldown_sec

        self.last_execution_time = {}

        self.lock = threading.Lock()

    # =====================================================
    # Check Allow Execution
    # =====================================================
    def allow(self, symbol: str) -> bool:

        with self.lock:

            now = time.time()

            last_time = self.last_execution_time.get(symbol)

            if last_time is None:
                self.last_execution_time[symbol] = now
                return True

            if now - last_time < self.cooldown_sec:
                return False

            self.last_execution_time[symbol] = now

            return True

    # =====================================================
    # Force Reset
    # =====================================================
    def reset(self, symbol: str = None):

        with self.lock:

            if symbol:
                self.last_execution_time.pop(symbol, None)
            else:
                self.last_execution_time.clear()

    # =====================================================
    # Status
    # =====================================================
    def status(self):

        return {
            "tracked_symbols": len(self.last_execution_time),
            "cooldown_sec": self.cooldown_sec,
        }


# =====================================================
# Singleton
# =====================================================
execution_guard = ExecutionGuard()
