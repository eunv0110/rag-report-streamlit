"""Google Sheets 기반 로깅 및 피드백 수집 모듈"""
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import os
from typing import Optional, Dict, Any
import streamlit as st


class SheetsLogger:
    """Google Sheets에 사용자 로그와 피드백을 저장하는 클래스"""

    def __init__(self):
        """Google Sheets 클라이언트 초기화"""
        self.client = None
        self.logs_sheet = None
        self.feedback_sheet = None
        self._initialize_client()

    def _initialize_client(self):
        """Google Sheets API 클라이언트 초기화"""
        try:
            # Streamlit Cloud에서는 secrets 사용
            if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
                credentials_dict = dict(st.secrets['gcp_service_account'])
            # 로컬 환경에서는 환경 변수 사용
            else:
                credentials_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
                if not credentials_json:
                    print("⚠️  Google Sheets credentials not found. Logging disabled.")
                    return
                credentials_dict = json.loads(credentials_json)

            # 스코프 설정
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            credentials = Credentials.from_service_account_info(
                credentials_dict,
                scopes=scopes
            )

            self.client = gspread.authorize(credentials)

            # 스프레드시트 열기 또는 생성
            spreadsheet_id = self._get_spreadsheet_id()
            if spreadsheet_id:
                spreadsheet = self.client.open_by_key(spreadsheet_id)
            else:
                spreadsheet = self.client.create('RAG Report Generator Logs')
                print(f"✅ 새 스프레드시트 생성됨: {spreadsheet.url}")

            # 워크시트 설정
            self._setup_worksheets(spreadsheet)

            print("✅ Google Sheets logger 초기화 완료")

        except Exception as e:
            print(f"⚠️  Google Sheets 초기화 실패: {e}")
            self.client = None

    def _get_spreadsheet_id(self) -> Optional[str]:
        """스프레드시트 ID 가져오기"""
        if hasattr(st, 'secrets') and 'GOOGLE_SHEETS_ID' in st.secrets:
            return st.secrets['GOOGLE_SHEETS_ID']
        return os.getenv('GOOGLE_SHEETS_ID')

    def _setup_worksheets(self, spreadsheet):
        """워크시트 설정 (Logs, Feedback)"""
        try:
            # Logs 워크시트
            try:
                self.logs_sheet = spreadsheet.worksheet('Logs')
            except gspread.WorksheetNotFound:
                self.logs_sheet = spreadsheet.add_worksheet(title='Logs', rows=1000, cols=20)
                # 헤더 추가
                self.logs_sheet.append_row([
                    'Timestamp',
                    'User Input',
                    'Report Type',
                    'Output Format',
                    'Author',
                    'Start Date',
                    'End Date',
                    'Response Time (s)',
                    'Status',
                    'Error Message',
                    'Session ID'
                ])

            # Feedback 워크시트
            try:
                self.feedback_sheet = spreadsheet.worksheet('Feedback')
            except gspread.WorksheetNotFound:
                self.feedback_sheet = spreadsheet.add_worksheet(title='Feedback', rows=1000, cols=20)
                # 헤더 추가
                self.feedback_sheet.append_row([
                    'Timestamp',
                    'Session ID',
                    'Rating',
                    'Feedback Text',
                    'Report Type',
                    'User Input'
                ])

        except Exception as e:
            print(f"⚠️  워크시트 설정 실패: {e}")

    def log_request(
        self,
        user_input: str,
        request_data: Dict[str, Any],
        response_time: float,
        status: str,
        error_message: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        """사용자 요청 로그 저장"""
        if not self.client or not self.logs_sheet:
            return

        try:
            row = [
                datetime.now().isoformat(),
                user_input,
                request_data.get('report_type', ''),
                request_data.get('output_format', ''),
                request_data.get('author', ''),
                request_data.get('start_date', ''),
                request_data.get('end_date', ''),
                f"{response_time:.2f}",
                status,
                error_message or '',
                session_id or ''
            ]
            self.logs_sheet.append_row(row)
            print(f"✅ 로그 저장됨: {user_input[:50]}...")

        except Exception as e:
            print(f"⚠️  로그 저장 실패: {e}")

    def log_feedback(
        self,
        rating: int,
        feedback_text: str,
        report_type: str,
        user_input: str,
        session_id: Optional[str] = None
    ):
        """사용자 피드백 저장"""
        if not self.client or not self.feedback_sheet:
            return

        try:
            row = [
                datetime.now().isoformat(),
                session_id or '',
                rating,
                feedback_text,
                report_type,
                user_input
            ]
            self.feedback_sheet.append_row(row)
            print(f"✅ 피드백 저장됨: {rating}점")

        except Exception as e:
            print(f"⚠️  피드백 저장 실패: {e}")


# 싱글톤 인스턴스
_logger_instance = None

def get_logger() -> SheetsLogger:
    """SheetsLogger 싱글톤 인스턴스 반환"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = SheetsLogger()
    return _logger_instance
