#!/bin/bash

echo "====================================="
echo "  STARTING TRADING SYSTEM"
echo "====================================="

# =========================
# 1. 환경 변수
# =========================
export PYTHONUNBUFFERED=1

# =========================
# 2. 로그 디렉토리 생성
# =========================
mkdir -p logs

# =========================
# 3. Docker 체크
# =========================
if ! command -v docker &> /dev/null
then
    echo "Docker not installed"
    exit 1
fi

# =========================
# 4. 기존 컨테이너 종료
# =========================
echo "Stopping old containers..."
docker compose down

# =========================
# 5. 빌드
# =========================
echo "Building system..."
docker compose build

# =========================
# 6. 실행
# =========================
echo "Starting system..."
docker compose up -d

# =========================
# 7. 상태 확인
# =========================
echo "Checking status..."
docker ps

# =========================
# 8. 완료
# =========================
echo "====================================="
echo "  SYSTEM RUNNING"
echo "====================================="
