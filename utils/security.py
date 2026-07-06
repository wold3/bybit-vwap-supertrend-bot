import hmac
import hashlib
import time

from config import WEBHOOK_SECRET


# =====================================================
# Signature 생성
# =====================================================
def generate_signature(payload: str, timestamp: str) -> str:

    message = f"{timestamp}.{payload}".encode()

    signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        message,
        hashlib.sha256,
    ).hexdigest()

    return signature


# =====================================================
# Signature 검증
# =====================================================
def verify_signature(payload: str, timestamp: str, signature: str) -> bool:

    expected = generate_signature(payload, timestamp)

    return hmac.compare_digest(expected, signature)


# =====================================================
# Replay Attack 방지
# =====================================================
def is_fresh_request(timestamp: str, tolerance_sec: int = 30) -> bool:

    try:

        req_time = int(timestamp)
        now = int(time.time())

        return abs(now - req_time) <= tolerance_sec

    except Exception:
        return False


# =====================================================
# Full Request Validation
# =====================================================
def validate_request(payload: str, timestamp: str, signature: str) -> tuple:

    if not is_fresh_request(timestamp):

        return False, "stale_request"

    if not verify_signature(payload, timestamp, signature):

        return False, "invalid_signature"

    return True, "ok"
