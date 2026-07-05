# Bybit VWAP + SuperTrend Auto Trading Bot

TradingView Webhook → Python → Bybit V5 자동매매 시스템

---

## 구조

TradingView (Pine Script)
        ↓ Webhook(JSON)
Flask Server (app.py)
        ↓
Signal Parser
        ↓
Bybit API Engine
        ↓
실거래

---

## 기능

- VWAP + SuperTrend 전략
- BUY / SELL / SHORT / EXIT 자동 처리
- Bybit V5 API 연동
- Long / Short / Reverse
- Testnet / Mainnet 지원
- Webhook 기반 자동매매

---

## 설치

```bash
git clone https://github.com/your-repo/bybit-bot
cd bybit-bot

python -m venv venv
source venv/bin/activate   # windows: venv\Scripts\activate

pip install -r requirements.txt
