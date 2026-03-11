#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 대시보드 + Cloudflare 터널 동시 실행 스크립트
# ═══════════════════════════════════════════════════════════

# 절전 방지 활성화
termux-wake-lock

# 현재 디렉토리를 프로젝트 루트로 설정
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "🖥️ Flask 대시보드 시작 중..."
python dashboard/app.py &
FLASK_PID=$!
echo "  → Flask PID: $FLASK_PID (http://localhost:5000)"

# Flask 시작 대기
sleep 3

echo "🌐 Cloudflare 터널 시작 중..."
cloudflared tunnel --url http://localhost:5000 &
TUNNEL_PID=$!
echo "  → 터널 PID: $TUNNEL_PID"
echo ""
echo "⏳ 터널 URL이 출력될 때까지 잠시 기다려주세요..."
echo "   (https://xxxxx.trycloudflare.com 형태의 URL이 표시됩니다)"
echo ""
echo "종료하려면 Ctrl+C를 누르세요."

# 종료 시 정리
trap "echo '정리 중...'; kill $FLASK_PID $TUNNEL_PID 2>/dev/null; termux-wake-unlock; echo '✅ 종료됨'" EXIT
wait
