# news_fetcher.py — 네이버 뉴스 검색 API 호출 모듈
import requests
import os
import re


NAVER_API_URL = "https://openapi.naver.com/v1/search/news.json"


def fetch_news(keyword: str, display: int = 10) -> list[dict]:
    """네이버 뉴스 검색 API를 호출하여 최신 뉴스를 수집합니다.

    Args:
        keyword: 검색할 키워드 (예: "삼성전자")
        display: 가져올 뉴스 개수 (최대 100)

    Returns:
        전처리된 뉴스 아이템 리스트
    """
    headers = {
        "X-Naver-Client-Id": os.environ["NAVER_CLIENT_ID"],
        "X-Naver-Client-Secret": os.environ["NAVER_CLIENT_SECRET"],
    }
    params = {
        "query": keyword,
        "display": display,
        "sort": "date",  # 최신순 정렬
    }

    response = requests.get(NAVER_API_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    items = response.json().get("items", [])
    return [_clean_news_item(item) for item in items]


def _clean_news_item(item: dict) -> dict:
    """뉴스 아이템에서 HTML 태그를 제거하고 필요한 필드만 추출합니다."""
    return {
        "title": _strip_html(item.get("title", "")),
        "description": _strip_html(item.get("description", "")),
        "link": item.get("originallink") or item.get("link", ""),
        "pub_date": item.get("pubDate", ""),
    }


def _strip_html(text: str) -> str:
    """HTML 태그 및 엔티티를 제거합니다."""
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&quot;", '"').replace("&amp;", "&")
    text = text.replace("&lt;", "<").replace("&gt;", ">")
    return text.strip()
