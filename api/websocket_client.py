import json
import threading
import time
import logging

logger = logging.getLogger(__name__)


class WebSocketClient:

    def __init__(self):
        self.price_callback = None
        self.running = False
        self.ws = None

    # =====================================================
    # 콜백 설정
    # =====================================================
    def set_price_callback(self, callback):
        self.price_callback = callback

    # =====================================================
    # 안전 JSON 파서
    # =====================================================
    def safe_parse(self, msg):

        if msg is None:
            return None

        # 이미 dict면 그대로 사용
        if isinstance(msg, dict):
            return msg

        # string이면 JSON 변환 시도
        if isinstance(msg, str):
            try:
                return json.loads(msg)
            except Exception:
                return None

        return None

    # =====================================================
    # 메시지 처리 (핵심 수정 포인트)
    # =====================================================
    def on_message(self, msg):

        try:
            data = self.safe_parse(msg)

            if not isinstance(data, dict):
                return

            # Bybit 구조 대응 (여러 형태 방어)
            price = None

            # 1) 일반 trade 구조
            if "data" in data:
                inner = data["data"]

                if isinstance(inner, list) and len(inner) > 0:
                    item = inner[0]

                    if isinstance(item, dict):
                        price = item.get("price")

                elif isinstance(inner, dict):
                    price = inner.get("price")

            # 2) 직접 price 들어오는 경우
            if price is None:
                price = data.get("price")

            if price is None:
                return

            # float 변환
            try:
                price = float(price)
            except:
                return

            # 콜백 호출
            if self.price_callback:
                self.price_callback(price)

        except Exception as e:
            logger.error(f"WS on_message error: {e}")

    # =====================================================
    # 더미 WS start (실제 프로젝트 구조 유지)
    # =====================================================
    def start(self):

        self.running = True
        logger.info("WebSocket started")

        # 실제 WS 연결이 있으면 여기서 연결해야 함
        # 현재 구조에서는 mock 또는 외부 client가 있을 가능성 있음

        def mock_stream():
            import random

            while self.running:
                try:
                    # mock price (실데이터 연결 전까지 안전 테스트)
                    price = 65000 + random.randint(-100, 100)

                    if self.price_callback:
                        self.price_callback(price)

                    time.sleep(1)

                except Exception as e:
                    logger.error(f"WS mock error: {e}")
                    time.sleep(2)

        t = threading.Thread(target=mock_stream, daemon=True)
        t.start()

    # =====================================================
    # 종료
    # =====================================================
    def stop(self):
        self.running = False
        logger.info("WebSocket stopped")


# 싱글톤 객체
ws_client = WebSocketClient()
