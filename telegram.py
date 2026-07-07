# ==========================================
# Telegram compatibility wrapper
# watchdog.py / services/ws_client.py 호환용
# ==========================================

class TelegramService:

    def send(self, message):
        try:
            # 기존 전송 함수가 존재하면 사용
            if "send_message" in globals():
                return send_message(message)

            # 전송 함수가 없을 경우 로그만 출력
            print("[Telegram]", message)
            return True

        except Exception as e:
            print("[Telegram Error]", e)
            return False


# 기존 코드에서
# from telegram import telegram
# 형태로 가져갈 객체 생성

telegram = TelegramService()

telegram.py 맨 아래에 추가하세요.
