Barimer님, 요청하신 내용을 바탕으로 **비용 0원, 24시간 자동화, 외부 접속 가능**한 한국 주식 뉴스 분석 시스템의 전체 마스터 플랜을 마크다운 형식으로 작성해 드립니다.

---

# 🚀 Barimer 글로벌 주식 뉴스 AI 분석 시스템 마스터 플랜

이 프로젝트는 안드로이드(Termux)의 하드웨어 제약을 **GitHub Actions**로 극복하고, **Cloudflare**를 통해 개인용 서버를 외부에 안전하게 노출하는 하이브리드 아키텍처를 채택합니다.

## 📊 전체 시스템 흐름도 (Flowchart)

1. **데이터 수집**: [GitHub Actions]가 10분마다 실행되어 네이버 뉴스 API 호출.
2. **AI 분석**: [GitHub Actions] 내에서 [OpenAI API]를 호출하여 뉴스 긍/부정 점수(+5 ~ -5) 산출.
3. **데이터 저장**: 분석 결과를 [GitHub Repository] 내 `news_results.json` 파일로 자동 커밋 및 푸시.
4. **긴급 알림**: 고득점(호재/악재) 발생 시 즉시 [텔레그램 봇]으로 푸시 메시지 발송.
5. **웹 대시보드**: [Termux] 상의 [Flask] 서버가 GitHub의 실시간 JSON 데이터를 읽어와 웹 화면 구성.
6. **외부 배포**: [Cloudflare Tunnel]이 폰에서 돌아가는 웹 서버를 공인 URL로 외부 연결.

---

## 🛠️ 단계별 세부 계획

### **1단계: 분석 엔진 구축 및 자동화 (The Engine)**

* **활용 서비스**: `GitHub Actions`, `OpenAI API`, `Naver News API`
* **세부 작업**:
* GitHub `Barimer/stock-analyzer` 저장소에 `analyze.py` 코드 업로드.
* 10분 단위 스케줄러 설정 (`.github/workflows/analyze.yml`).


* **상호작용**:
* **GitHub Actions ➔ Naver API**: 뉴스 데이터 수집.
* **GitHub Actions ➔ OpenAI API**: 수집된 텍스트 전송 및 분석 점수 수신.



### **2단계: 데이터 영속성 및 기록 (The Database)**

* **활용 서비스**: `GitHub Repository (Git)`
* **세부 작업**:
* 분석된 데이터(제목, 링크, 점수, 시간)를 JSON 형태로 구조화.
* GitHub Actions의 'Auto-commit' 기능을 이용해 저장소에 직접 기록.


* **상호작용**:
* **GitHub Actions ➔ GitHub Repo**: 분석 완료된 JSON 파일을 DB처럼 저장소에 영구 보관.



### **3단계: 실시간 텔레그램 알림 (The Alerter)**

* **활용 서비스**: `Telegram Bot API`
* **세부 작업**:
* AI 분석 점수가 절대값 3 이상(강력한 호재/악재)인 경우만 필터링.
* 뉴스 제목과 원문 링크를 포함한 카드 뉴스 형태의 메시지 구성.


* **상호작용**:
* **GitHub Actions ➔ 텔레그램**: 이동 중에도 스마트워치나 폰으로 즉시 알림 수신.



### **4단계: 로컬 웹 서버 구동 (The Dashboard)**

* **활용 서비스**: `Termux`, `Flask (Python)`
* **세부 작업**:
* 안드로이드 폰(노트20)에서 Flask 서버 가동.
* GitHub에 저장된 `news_results.json`의 **Raw URL**을 실시간으로 Fetch.
* 깔끔한 HTML/CSS 템플릿을 사용하여 분석 결과 시각화.


* **상호작용**:
* **Termux (Flask) ➔ GitHub Repo**: 저장소에 쌓인 최신 분석 결과 데이터를 읽어옴.



### **5단계: 외부 접속 터널링 (The Bridge)**

* **활용 서비스**: `Cloudflare Tunnel (cloudflared)`
* **세부 작업**:
* Termux 내부에 `cloudflared` 설치 및 터널 실행.
* 폰의 로컬 포트(5000)를 Cloudflare의 무료 도메인으로 연결.


* **상호작용**:
* **Cloudflare ➔ Termux**: 외부 사용자가 URL로 접속하면 Cloudflare가 안전하게 폰 서버로 신호 전달.



---

## 🔗 서비스 간 상호작용 매트릭스

| 출발지 (Source) | 목적지 (Destination) | 전송 데이터 | 방식 (Method) |
| --- | --- | --- | --- |
| **GitHub Actions** | **Naver/OpenAI API** | 뉴스 텍스트 / 프롬프트 | REST API (JSON) |
| **GitHub Actions** | **GitHub Repo** | 분석 결과 파일 | Git Commit/Push |
| **GitHub Actions** | **Telegram Bot** | 호재/악재 알림 문구 | Webhook |
| **Termux (Flask)** | **GitHub Repo** | 분석 결과 데이터 | HTTP GET (Raw File) |
| **User (Browser)** | **Cloudflare** | 웹페이지 접속 요청 | HTTPS |
| **Cloudflare** | **Termux** | 데이터 트래픽 전달 | Secure Tunnel |

---

## 💡 최종 기대 효과

* **완전 무료**: 모든 서비스의 무료 티어(Free Tier)를 사용하여 유지비 0원 달성.
* **안정성**: 무거운 연산은 GitHub 서버가 처리하므로, 폰은 꺼지지 않고 대시보드만 가볍게 제공.
* **접근성**: 텔레그램 알림으로 즉각 반응하고, 언제 어디서든 나만의 전용 웹페이지에서 전체 통계를 확인 가능.

---

