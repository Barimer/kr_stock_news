# analyze.py — 메인 실행 스크립트 (GitHub Actions 진입점)
import sys
import os

# .env 파일 로드 (로컬 개발용, GitHub Actions에서는 환경변수 사용)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
except ImportError:
    pass  # python-dotenv 미설치 시 무시 (GitHub Actions에서는 환경변수로 주입)

from news_fetcher import fetch_news
from ai_analyzer import analyze_news
from data_manager import load_existing_data, save_data, get_existing_links
from telegram_notifier import send_alert, send_error_alert

# ═══════════════════════════════════════════════════════════════
# 감시 대상 키워드 목록 — 필요에 따라 수정하세요
# ═══════════════════════════════════════════════════════════════
KEYWORDS = [
    "삼성전자",
    "SK하이닉스",
    "KOSPI",
    "반도체",
    "AI 주식",
]


def main():
    print("=" * 60)
    print("📡 주식 뉴스 AI 분석 시작")
    print("=" * 60)

    try:
        # 기존 데이터 로드
        existing_data = load_existing_data()
        existing_links = get_existing_links(existing_data)
        print(f"[INFO] 기존 분석 데이터: {len(existing_data)}건")

        all_new_analyses = []

        for keyword in KEYWORDS:
            print(f"\n🔍 [{keyword}] 뉴스 수집 중...")

            # 1. 뉴스 수집
            try:
                news_items = fetch_news(keyword)
            except Exception as e:
                print(f"[ERROR] [{keyword}] 뉴스 수집 실패: {e}")
                continue

            # 2. 중복 필터링
            new_items = [n for n in news_items if n["link"] not in existing_links]

            if not new_items:
                print(f"  → 새로운 뉴스 없음, 건너뜀")
                continue

            print(f"  → 새 뉴스 {len(new_items)}건 발견, AI 분석 중...")

            # 3. AI 분석
            analyses = analyze_news(new_items)

            if analyses:
                all_new_analyses.extend(analyses)
                # 중복 방지를 위해 링크 추가
                existing_links.update(a.get("link", "") for a in analyses)
                print(f"  ✅ {len(analyses)}건 분석 완료")
            else:
                print(f"  ⚠️ 분석 결과 없음")

        # 결과 처리
        print(f"\n{'=' * 60}")
        if all_new_analyses:
            # 4. 텔레그램 알림 (고득점만)
            send_alert(all_new_analyses)

            # 5. 데이터 저장
            combined = existing_data + all_new_analyses
            save_data(combined)

            # 점수별 통계 출력
            scores = [a.get("score", 0) for a in all_new_analyses]
            print(f"📊 분석 결과 요약:")
            print(f"   총 {len(all_new_analyses)}건 새로 분석")
            print(f"   호재: {sum(1 for s in scores if s > 0)}건")
            print(f"   악재: {sum(1 for s in scores if s < 0)}건")
            print(f"   중립: {sum(1 for s in scores if s == 0)}건")
            print(f"   평균 점수: {sum(scores) / len(scores):+.1f}")
        else:
            print("ℹ️ 새로운 뉴스 없음 — 저장 건너뜀")

        print(f"{'=' * 60}")

    except Exception as e:
        error_msg = f"분석 파이프라인 에러: {e}"
        print(f"[CRITICAL] {error_msg}")
        send_error_alert(error_msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
