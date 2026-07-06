import logging

logger = logging.getLogger(__name__)


class SignalParser:
    """
    TradingView / 외부 신호 표준화 파서
    """

    VALID_SIGNALS = {"BUY", "SELL", "LONG", "SHORT"}

    def parse(self, data):
        """
        다양한 입력을 표준 signal로 변환
        """

        try:

            if data is None:
                return None

            # =========================
            # dict 형태 입력
            # =========================
            if isinstance(data, dict):

                signal = data.get("signal") or data.get("action")

                if not signal:
                    return None

            # =========================
            # string 입력
            # =========================
            elif isinstance(data, str):

                signal = data.strip().upper()

            else:
                return None

            # =========================
            # validation
            # =========================
            if signal not in self.VALID_SIGNALS:
                logger.warning("Invalid signal: %s", signal)
                return None

            return signal

        except Exception as e:
            logger.exception(e)
            return None


# =====================================================
# Convenience Functions
# =====================================================

parser = SignalParser()


def parse_signal(data):
    return parser.parse(data)
