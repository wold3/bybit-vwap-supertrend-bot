import os
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

load_dotenv()

class ExecutionEngine:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        self.testnet = os.getenv("LIVE_TRADING", "false").lower() != "true"
        
        # 바이비트 세션 초기화
        self.session = HTTP(
            testnet=self.testnet,
            api_key=self.api_key,
            api_secret=self.api_secret,
        )

    def execute(self, symbol, side, qty):
        """매수/매도 주문 실행"""
        try:
            order_side = "Buy" if side == "Buy" else "Sell"
            response = self.session.place_order(
                category="linear",
                symbol=symbol,
                side=order_side,
                orderType="Market",
                qty=str(qty),
            )
            return response
        except Exception as e:
            print(f"주문 실행 오류: {e}")
            return None

    def close_position(self, symbol, side, qty):
        """포지션 종료 (반대 방향 주문)"""
        try:
            # 포지션 종료를 위해 반대 방향 설정
            close_side = "Sell" if side == "Buy" else "Buy"
            response = self.session.place_order(
                category="linear",
                symbol=symbol,
                side=close_side,
                orderType="Market",
                qty=str(qty),
            )
            return response
        except Exception as e:
            print(f"포지션 종료 오류: {e}")
            return None

    def get_account_equity(self):
        """계좌 잔고 조회 (Equity Loop용)"""
        try:
            # 통합 거래 계정(UTA) 잔고 조회
            response = self.session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
            equity = response['result']['list'][0]['coin'][0]['walletBalance']
            return float(equity)
        except Exception as e:
            print(f"잔고 조회 오류: {e}")
            return 0.0

# 전역 인스턴스 생성
execution_engine = ExecutionEngine()
