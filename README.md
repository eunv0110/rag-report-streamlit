# RAG 보고서 생성 Streamlit UI

AI 기반 자동 보고서 생성 서비스의 사용자 친화적인 웹 인터페이스입니다.
<img width="1783" height="979" alt="image" src="https://github.com/user-attachments/assets/6144d225-0f81-467b-a205-46e388f3d4e1" />

## 주요 기능

- 💬 **대화형 인터페이스**: 채팅 형식으로 간편하게 보고서 요청
- 📊 **실시간 진행 상황**: 보고서 생성 과정을 단계별로 확인
- 📥 **즉시 다운로드**: 생성된 보고서를 PDF 또는 DOCX 형식으로 바로 다운로드
- ⚙️ **유연한 설정**: 보고서 타입, 출력 형식, 날짜 범위 등을 자유롭게 설정
- 💬 **피드백 시스템**: 생성된 보고서에 대한 평점과 피드백 제공
- 🎨 **깔끔한 UI**: 직관적이고 세련된 사용자 인터페이스

### 메인 화면
- 깔끔한 채팅 인터페이스
- 사이드바에서 실시간 서버 상태 확인
- 보고서 설정 커스터마이징

### 보고서 생성 과정
1. 🚀 보고서 생성 요청 시작
2. 🔍 관련 문서 검색
3. 🤖 AI 문서 분석
4. 📝 보고서 작성
5. ✅ 생성 완료

## 빠른 시작

### 1. 사전 요구사항

- Python 3.8 이상
- RAG Report API 서버가 실행 중이어야 합니다

### 2. 설치 및 실행

```bash
# 저장소 클론
git clone <repository-url>
cd rag-report-streamlit

# 가상환경 생성 및 활성화 (선택사항)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
echo "API_BASE_URL=http://localhost:8000" > .env

# Streamlit 앱 실행
streamlit run app.py
```

앱이 자동으로 브라우저에서 열립니다. (기본값: http://localhost:8501)

## ⚙️ 환경 설정

### 환경 변수

`.env` 파일을 생성하여 API 엔드포인트를 설정하세요:

```bash
API_BASE_URL=http://localhost:8000
```

### Streamlit Cloud 배포

Streamlit Cloud에 배포 시 secrets를 설정하세요:

```toml
# .streamlit/secrets.toml
API_BASE_URL = "https://your-api-server.com"
```

## 사용 방법

### 1. 보고서 설정

사이드바에서 다음 항목을 설정할 수 있습니다:

- **작성자**: 보고서에 표시될 작성자 이름
- **보고서 타입**:
  - 📅 주간 보고서 (weekly)
  - 👔 최종 보고서 (executive)
- **출력 형식**:
  - 📕 PDF
  - 📘 DOCX (Word)
- **날짜 범위 필터링** (선택사항):
  - 특정 기간의 문서만 검색하여 보고서 생성

### 2. 보고서 요청

메시지 입력창에 원하는 보고서 내용을 입력하세요.

**예시**:
```
이번 주 주간 보고서 작성해줘
12월 첫째 주 프로젝트 진행 상황 정리해줘
최근 한 달간의 성과를 요약해줘
```

### 3. 보고서 다운로드 및 피드백

- 보고서 생성 완료 후 **다운로드 버튼**을 클릭하여 파일을 받으세요
- **피드백 버튼**을 눌러 보고서 품질을 평가하고 의견을 남길 수 있습니다
  - 평점: 1-10 (1: 매우 나쁨, 10: 매우 좋음)
  - 의견: 자유롭게 피드백 작성

## 의존성

```
streamlit
streamlit-chat
requests
python-dotenv
```

## 개발 가이드

### 디렉토리 구조

```
rag-report-streamlit/
├── app.py                    # 메인 Streamlit 애플리케이션
├── requirements.txt          # Python 의존성
├── .env                      # 환경 변수 (git에서 제외)
├── .gitignore               # Git 제외 파일 목록
└── README.md                # 이 파일
```

### 주요 기능 구현

#### 세션 상태 관리
```python
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False
```

#### API 호출
```python
response = requests.post(
    f"{API_BASE_URL}/generate-report",
    json=request_data,
    timeout=300
)
```

#### 피드백 제출
```python
feedback_payload = {
    "trace_id": trace_id,
    "score": rating,
    "comment": feedback_text,
    "feedback_type": "user_satisfaction"
}
```

## 📚 관련 프로젝트

- [RAG Report API](../rag-report-api/README.md) - 백엔드 API 서버
- [RAG Report Generator](../rag-report-generator/README.md) - 보고서 생성 엔진

---

Made with ❤️ using Streamlit
