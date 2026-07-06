import logging

logger = logging.getLogger(__name__)


def send_trade(signal, symbol, qty, price):
    logger.info(f"[TRADE] {signal} {symbol} qty={qty} price={price}")


def send_error(message: str):
    logger.error(f"[ERROR] {message}")
