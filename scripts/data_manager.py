# data_manager.py — JSON 데이터 관리 (저장/로드/로테이션/중복 제거)
import json
import os
from datetime import datetime, timedelta

# 프로젝트 루트 기준 데이터 파일 경로
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DATA_FILE = os.path.join(DATA_DIR, "news_results.json")

# 데이터 보관 기간 (일)
RETENTION_DAYS = 7


def load_existing_data() -> list[dict]:
    """기존 분석 결과를 JSON 파일에서 로드합니다."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[WARN] 기존 데이터 로드 실패, 빈 리스트로 시작: {e}")
        return []


def save_data(data: list[dict]):
    """분석 결과를 JSON 파일에 저장합니다.

    - 최근 RETENTION_DAYS일분만 유지 (로테이션)
    - URL 기준 중복 제거
    """
    # 데이터 디렉토리 생성
    os.makedirs(DATA_DIR, exist_ok=True)

    # 7일 이내 데이터만 유지
    cutoff = (datetime.now() - timedelta(days=RETENTION_DAYS)).isoformat()
    filtered = [
        item for item in data
        if item.get("analyzed_at", "") >= cutoff
    ]

    # URL 기준 중복 제거 (최신 항목 유지)
    seen_links = set()
    unique_data = []
    for item in reversed(filtered):  # 역순으로 순회하여 최신 항목 우선
        link = item.get("link", "")
        if link and link not in seen_links:
            seen_links.add(link)
            unique_data.append(item)
    unique_data.reverse()  # 다시 시간순으로 정렬

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(unique_data, f, ensure_ascii=False, indent=2)

    print(f"[INFO] 데이터 저장 완료: {len(unique_data)}건 (7일 보관)")


def get_existing_links(existing_data: list[dict]) -> set:
    """기존 뉴스 URL 집합을 반환합니다 (중복 수집 방지용)."""
    return {item.get("link", "") for item in existing_data if item.get("link")}
