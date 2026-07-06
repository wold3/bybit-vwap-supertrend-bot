import time
import random
from telegram import telegram


class RetryEngine:

    def __init__(self):

        self.max_retry = 3
        self.base_delay = 1.0  # seconds

    # =================================================
    # EXECUTE WITH RETRY
    # =================================================
    def execute_with_retry(self, execute_func, *args, **kwargs):

        last_error = None

        for attempt in range(1, self.max_retry + 1):

            try:
                print(f"[RETRY] Attempt {attempt}")

                result = execute_func(*args, **kwargs)

                # 성공 조건 (API 응답 기준)
                if result and self._is_success(result):
                    print("[RETRY] SUCCESS")
                    return result

                raise Exception("Order failed response")

            except Exception as e:

                last_error = str(e)

                delay = self.base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.5)

                print(f"[RETRY ERROR] {e} | next retry in {delay:.2f}s")

                time.sleep(delay)

        # =================================================
        # FAIL FINAL
        # =================================================
        telegram.send(
            "❌ ORDER FAILED AFTER RETRIES\n"
            f"Error: {last_error}"
        )

        print("[RETRY] FINAL FAIL")

        return None

    # =================================================
    # SUCCESS CHECK
    # =================================================
    def _is_success(self, result):

        try:
            # Bybit V5 성공 코드 체크
            return result.get("retCode") == 0
        except:
            return False


# SINGLETON
retry_engine = RetryEngine()
