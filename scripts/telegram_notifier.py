# telegram_notifier.py — 텔레그램 봇 알림 모듈
import requests
import os

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"

# 알림 발송 기준 점수 (절대값)
ALERT_THRESHOLD = 3


def send_alert(analyses: list[dict]):
    """고득점(호재/악재) 뉴스를 텔레그램으로 알림 발송합니다.

    절대값 ALERT_THRESHOLD 이상인 뉴스만 필터링하여 발송합니다.

    Args:
        analyses: AI 분석 결과 리스트
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[WARN] 텔레그램 설정 누락 — 알림 건너뜀")
        return

    # 절대값 기준 필터링
    alerts = [a for a in analyses if abs(a.get("score", 0)) >= ALERT_THRESHOLD]

    if not alerts:
        print("[INFO] 고득점 뉴스 없음 — 알림 없음")
        return

    for alert in alerts:
        message = _format_alert_message(alert)
        _send_telegram_message(token, chat_id, message)

    print(f"[INFO] 텔레그램 알림 {len(alerts)}건 발송 완료")


def send_error_alert(error_message: str):
    """에러 발생 시 텔레그램으로 에러 알림을 발송합니다."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return

    message = f"🚨 시스템 에러 발생!\n\n{error_message}"
    _send_telegram_message(token, chat_id, message)


def _format_alert_message(alert: dict) -> str:
    """알림 메시지를 포맷팅합니다."""
    score = alert.get("score", 0)
    is_positive = score > 0
    emoji = "🟢" if is_positive else "🔴"
    intensity = "⚡강력 " if abs(score) >= 4 else ""
    sentiment = "호재" if is_positive else "악재"

    related = ", ".join(alert.get("related_stocks", [])) or "N/A"

    return (
        f"{emoji} {intensity}{sentiment} 감지!\n\n"
        f"📰 {alert.get('title', 'N/A')}\n"
        f"📊 점수: {score:+d}/5\n"
        f"💡 판단근거: {alert.get('reason', 'N/A')}\n"
        f"🏢 관련종목: {related}\n"
        f"🔗 원문: {alert.get('link', 'N/A')}"
    )


def _send_telegram_message(token: str, chat_id: str, text: str):
    """텔레그램 메시지를 발송합니다."""
    try:
        resp = requests.post(
            TELEGRAM_API_URL.format(token=token),
            json={
                "chat_id": chat_id,
                "text": text,
                "disable_web_page_preview": True,
            },
            timeout=10,
        )
        if not resp.ok:
            print(f"[WARN] 텔레그램 발송 실패: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"[ERROR] 텔레그램 발송 에러: {e}")
