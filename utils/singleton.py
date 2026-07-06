import os
import sys
import atexit

LOCK_FILE = "bot.lock"


class SingletonLock:
    """
    BOT 중복 실행 방지 클래스
    - 이미 실행 중이면 종료
    - 종료 시 lock 자동 삭제
    """

    def __init__(self, lock_file: str = LOCK_FILE):
        self.lock_file = lock_file

    # ================================
    # LOCK CHECK
    # ================================
    def acquire(self):

        # 이미 실행 중이면 종료
        if os.path.exists(self.lock_file):

            print("❌ BOT already running (lock file exists)")
            sys.exit(0)

        # lock 생성
        with open(self.lock_file, "w") as f:
            f.write(str(os.getpid()))

        # 종료 시 자동 제거 등록
        atexit.register(self.release)

    # ================================
    # RELEASE LOCK
    # ================================
    def release(self):

        try:
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
        except Exception:
            pass


# ================================
# GLOBAL INSTANCE
# ================================
singleton = SingletonLock()
