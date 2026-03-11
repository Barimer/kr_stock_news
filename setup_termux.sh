#!/bin/bash
# ═══════════════════════════════════════════════════════════
# Termux 초기 설정 스크립트
# ═══════════════════════════════════════════════════════════

echo "🔧 Termux 환경 설정 시작..."

# 1. 패키지 업데이트
pkg update -y && pkg upgrade -y

# 2. 필수 패키지 설치
pkg install -y python git cloudflared

# 3. Python 의존성 설치
pip install flask requests python-dotenv

# 4. 절전 방지 설정
termux-wake-lock

echo ""
echo "✅ 설치 완료!"
echo ""
echo "📌 다음 단계:"
echo "  1. 프로젝트 클론: git clone https://github.com/{owner}/stock-analyzer.git"
echo "  2. 대시보드 실행: bash run_dashboard.sh"
