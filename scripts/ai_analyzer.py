# ai_analyzer.py — OpenAI GPT-4o-mini 기반 뉴스 감성 분석 모듈
from openai import OpenAI
import json
import os
from datetime import datetime


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """당신은 한국 주식 시장 전문 뉴스 분석가입니다.
각 뉴스 항목에 대해 아래 JSON 형식으로만 응답하세요. 다른 텍스트는 포함하지 마세요.

{
  "analyses": [
    {
      "title": "뉴스 제목",
      "score": (정수, -5 ~ +5),
      "reason": "점수 판단 근거 1줄 요약",
      "related_stocks": ["관련 종목명1", "종목명2"]
    }
  ]
}

점수 기준:
- +5: 매우 강한 호재 (대규모 실적 서프라이즈, 혁신적 신사업 발표 등)
- +3~+4: 강한 호재 (실적 개선, 긍정적 정책 등)
- +1~+2: 약한 호재
- 0: 중립 또는 주가 영향 없음
- -1~-2: 약한 악재
- -3~-4: 강한 악재 (실적 부진, 규제 강화 등)
- -5: 매우 강한 악재 (대규모 사고, 상장폐지 우려 등)"""


def analyze_news(news_items: list[dict]) -> list[dict]:
    """OpenAI gpt-4o-mini를 사용하여 뉴스 감성 분석을 수행합니다.

    Args:
        news_items: news_fetcher에서 수집된 뉴스 아이템 리스트

    Returns:
        분석 결과가 포함된 뉴스 아이템 리스트
    """
    if not news_items:
        return []

    # 뉴스 텍스트를 하나의 프롬프트로 결합
    news_text = "\n".join(
        f"- [{i + 1}] {item['title']}: {item['description']}"
        for i, item in enumerate(news_items)
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"다음 뉴스를 분석해주세요:\n\n{news_text}"},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
        )

        result = json.loads(response.choices[0].message.content)
        analyses = result.get("analyses", [])

        # 원본 뉴스 데이터와 분석 결과 병합
        for i, analysis in enumerate(analyses):
            if i < len(news_items):
                analysis["link"] = news_items[i]["link"]
                analysis["pub_date"] = news_items[i]["pub_date"]
                analysis["analyzed_at"] = datetime.now().isoformat()

        return analyses

    except Exception as e:
        print(f"[ERROR] AI 분석 실패: {e}")
        return []
