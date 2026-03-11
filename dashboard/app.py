# app.py — Flask 웹 대시보드 서버 (Termux에서 실행)
from flask import Flask, render_template, jsonify
import requests
import os
import time

# .env 파일 로드 (로컬 개발용)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
except ImportError:
    pass

app = Flask(__name__)

# ═══════════════════════════════════════════════════════════════
# GitHub Raw URL — 레포 설정 후 아래 값을 실제 URL로 교체하세요
# ═══════════════════════════════════════════════════════════════
GITHUB_RAW_URL = os.environ.get(
    "GITHUB_RAW_URL",
    "https://raw.githubusercontent.com/Barimer/kr_stock_news/main/data/news_results.json"
)

# 로컬 데이터 파일 경로 (GitHub URL 실패 시 fallback)
LOCAL_DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "news_results.json"
)


@app.route("/")
def index():
    """메인 대시보드 페이지"""
    return render_template("index.html")


@app.route("/api/news")
def api_news():
    """뉴스 분석 데이터를 반환하는 API 엔드포인트"""
    data = _fetch_data()
    if data is None:
        return jsonify({"status": "error", "message": "데이터를 가져올 수 없습니다"}), 500

    # 점수 절대값 기준 내림차순 정렬
    data.sort(key=lambda x: abs(x.get("score", 0)), reverse=True)

    # 통계 계산
    scores = [item.get("score", 0) for item in data]
    stats = {
        "total": len(data),
        "positive": sum(1 for s in scores if s > 0),
        "negative": sum(1 for s in scores if s < 0),
        "neutral": sum(1 for s in scores if s == 0),
        "avg_score": round(sum(scores) / len(scores), 2) if scores else 0,
    }

    return jsonify({"status": "ok", "data": data, "stats": stats})


def _fetch_data():
    """GitHub Raw URL에서 데이터를 가져오고, 실패 시 로컬 파일에서 읽습니다."""
    # 1. GitHub에서 가져오기 시도 (캐시 방지)
    try:
        url = f"{GITHUB_RAW_URL}?t={int(time.time())}"
        resp = requests.get(url, timeout=10)
        if resp.ok:
            return resp.json()
    except Exception:
        pass

    # 2. Fallback: 로컬 파일
    try:
        import json
        with open(LOCAL_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
