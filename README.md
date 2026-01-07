# RAG 보고서 생성 Streamlit 앱

사용자가 질문을 입력하면 RAG 시스템이 자동으로 보고서를 생성하는 웹 애플리케이션입니다.

## 기능

- ✅ 보고서 자동 생성 (주간 보고서, 최종 보고서)
- ✅ PDF/DOCX 형식 지원
- ✅ 날짜 범위 필터링
- ✅ 실시간 진행 상황 표시
- ✅ **사용자 로그 수집** (Google Sheets)
- ✅ **피드백 시스템** (별점 + 텍스트)

## 빠른 시작

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일이 이미 설정되어 있습니다:
- `API_BASE_URL`: RAG API 엔드포인트
- `GOOGLE_SHEETS_CREDENTIALS`: Google Sheets 인증 정보

### 3. Google Sheets API 활성화 (로깅 사용 시)

Google Cloud Console에서 다음 API를 활성화해야 합니다:
1. **Google Sheets API**
2. **Google Drive API**

자세한 설정 방법은 [SETUP_GOOGLE_SHEETS.md](SETUP_GOOGLE_SHEETS.md)를 참고하세요.

### 4. 앱 실행

```bash
streamlit run steamlit.py
```

브라우저에서 `http://localhost:8501`로 접속하세요.

## 사용 방법

1. 사이드바에서 보고서 설정 (타입, 형식, 작성자 등)
2. 채팅창에 원하는 보고서 요청 입력
   - 예: "이번 주 주간 보고서 작성해줘"
3. 보고서가 생성되면 다운로드 버튼 클릭
4. (선택) 피드백 버튼을 눌러 평가 남기기

## 로깅 및 피드백

앱은 자동으로 다음 데이터를 Google Sheets에 저장합니다:

### Logs 워크시트
- 사용자 입력
- 요청 파라미터 (보고서 타입, 형식, 날짜 등)
- 응답 시간
- 성공/실패 상태
- 에러 메시지
- 세션 ID

### Feedback 워크시트
- 별점 (1-5)
- 피드백 텍스트
- 보고서 타입
- 사용자 입력
- 세션 ID

스프레드시트가 없으면 첫 실행 시 자동으로 생성됩니다.

## Streamlit Cloud 배포

1. GitHub에 코드 푸시 (`.env` 파일은 제외됨)
2. [Streamlit Cloud](https://streamlit.io/cloud)에서 앱 배포
3. **Secrets** 설정:

```toml
API_BASE_URL = "http://3.38.91.237:8000"

[gcp_service_account]
type = "service_account"
project_id = "report-generator-483608"
private_key_id = "2fea73d7b3915f19fd6de939f47e0bb222f1acf6"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "service-account@report-generator-483608.iam.gserviceaccount.com"
client_id = "112500163492599024406"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/service-account%40report-generator-483608.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

자세한 내용은 [SETUP_GOOGLE_SHEETS.md](SETUP_GOOGLE_SHEETS.md)를 참고하세요.

## 파일 구조

```
rag-report-streamlit/
├── steamlit.py              # 메인 앱
├── sheets_logger.py         # Google Sheets 로거
├── requirements.txt         # 패키지 목록
├── requirements.lock        # 고정된 버전
├── .env                     # 환경 변수 (Git에서 제외)
├── .gitignore              # Git 제외 파일
├── README.md               # 이 파일
└── SETUP_GOOGLE_SHEETS.md  # Google Sheets 설정 가이드
```

## 문제 해결

### "Google Sheets credentials not found" 경고
- 정상입니다. 로깅 기능을 사용하지 않으면 무시해도 됩니다.
- 로깅을 사용하려면 `.env` 파일에 `GOOGLE_SHEETS_CREDENTIALS`를 설정하세요.

### "API 서버에 연결할 수 없습니다"
- API 서버가 실행 중인지 확인하세요.
- `.env` 파일의 `API_BASE_URL`이 올바른지 확인하세요.

### Google Sheets 권한 오류
- 서비스 계정에 스프레드시트 편집 권한이 있는지 확인하세요.
- Google Sheets API와 Google Drive API가 활성화되었는지 확인하세요.

## 기술 스택

- **Frontend**: Streamlit
- **UI Components**: streamlit-chat
- **API Client**: requests
- **Logging**: gspread + Google Sheets
- **Environment**: python-dotenv

## 라이선스

MIT
