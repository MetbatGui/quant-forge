import cloudscraper
import datetime
import time
from typing import Dict
from krx_netbuy_crawler.core.ports.fetcher_port import FetcherPort

class KrxFetcherAdapter(FetcherPort):
    """
    cloudscraper를 사용하여 KRX에서 데이터를 가져오는 어댑터입니다.
    MDCSTAT02401에 대한 올바른 KRX API 파라미터를 사용합니다.
    """
    
    OTP_URL = "http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd"
    DOWNLOAD_URL = "http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd"
    
    # 시장 코드 매핑
    MARKET_MAP = {
        "KOSPI": "STK",
        "KOSDAQ": "KSQ"
    }
    
    # 투자자 코드 매핑
    INVESTOR_MAP = {
        "foreigner": "9000", 
        "institutions": "7050" 
    }

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def _get_params(self, market: str, investor: str, date_str: str) -> Dict[str, str]:
        """
        OTP 생성을 위한 파라미터를 구성합니다.
        대상: dbms/MDC/STAT/standard/MDCSTAT02401 (투자자별 순매수 상위 종목)
        """
        market = market.upper()
        investor = investor.lower()
        
        mkt_id = self.MARKET_MAP.get(market)
        invst_code = self.INVESTOR_MAP.get(investor)
        
        if not mkt_id:
            raise ValueError(f"잘못된 시장 구분입니다: {market}")
        if not invst_code:
            raise ValueError(f"잘못된 투자자 구분입니다: {investor}")

        params = {
            'locale': 'ko_KR',
            'invstTpCd': invst_code,
            'strtDd': date_str,
            'endDd': date_str,
            'share': '1',
            'money': '3',
            'csvxls_isNo': 'false',
            'name': 'fileDown',
            'url': 'dbms/MDC/STAT/standard/MDCSTAT02401',
            'mktId': mkt_id
        }
        
        if market == 'KOSDAQ':
            params['segTpCd'] = 'ALL'
            
        return params

    def fetch_net_value_data(self, market: str, investor: str, date_str: str = None) -> bytes:
        """
        KRX에서 순매수 데이터를 가져옵니다.
        
        Args:
            market: 시장 구분 (KOSPI 또는 KOSDAQ)
            investor: 투자자 구분 (foreigner 또는 institutions)
            date_str: YYYYMMDD 형식의 날짜, 기본값은 오늘
            
        Returns:
            엑셀 파일 콘텐츠 (bytes)
        """
        if date_str is None:
            date_str = datetime.date.today().strftime('%Y%m%d')
            
        time.sleep(1)  # 속도 제한
        
        params = self._get_params(market, investor, date_str)
        
        print(f"  [KrxFetcherAdapter] 데이터 가져오는 중: {market} ({investor}) - {date_str}")
        
        # 1. OTP 생성
        otp_response = self.scraper.post(self.OTP_URL, data=params, verify=True)
        otp_response.raise_for_status()
        otp = otp_response.text.strip()
        
        if not otp or len(otp) < 50:
            raise ConnectionError(f"OTP 획득 실패. 응답: {otp[:50]}")
        
        # 2. 파일 다운로드
        download_params = {"code": otp}
        file_response = self.scraper.post(self.DOWNLOAD_URL, data=download_params, verify=True)
        file_response.raise_for_status()
        
        return file_response.content
