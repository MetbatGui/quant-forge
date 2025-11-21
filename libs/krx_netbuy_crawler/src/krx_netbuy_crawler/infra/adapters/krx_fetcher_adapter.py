import cloudscraper
import datetime
import time
from typing import Dict
from krx_netbuy_crawler.core.ports.fetcher_port import FetcherPort

class KrxFetcherAdapter(FetcherPort):
    """
    Adapter for fetching data from KRX using cloudscraper.
    Uses the correct KRX API parameters for MDCSTAT02401.
    """
    
    OTP_URL = "http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd"
    DOWNLOAD_URL = "http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd"
    
    # Market Code Mapping
    MARKET_MAP = {
        "KOSPI": "STK",
        "KOSDAQ": "KSQ"
    }
    
    # Investor Code Mapping
    INVESTOR_MAP = {
        "foreigner": "9000", 
        "institutions": "7050" 
    }

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def _get_params(self, market: str, investor: str, date_str: str) -> Dict[str, str]:
        """
        Constructs the parameters for the OTP generation request.
        Targeting: dbms/MDC/STAT/standard/MDCSTAT02401 (Daily Net Buy by Investor)
        """
        market = market.upper()
        investor = investor.lower()
        
        mkt_id = self.MARKET_MAP.get(market)
        invst_code = self.INVESTOR_MAP.get(investor)
        
        if not mkt_id:
            raise ValueError(f"Invalid market: {market}")
        if not invst_code:
            raise ValueError(f"Invalid investor: {investor}")

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
        Fetches the net buy value data from KRX.
        
        Args:
            market: Market type (KOSPI or KOSDAQ)
            investor: Investor type (foreigner or institutions)
            date_str: Date in YYYYMMDD format, defaults to today
            
        Returns:
            Excel file content as bytes
        """
        if date_str is None:
            date_str = datetime.date.today().strftime('%Y%m%d')
            
        time.sleep(1)  # Rate limiting
        
        params = self._get_params(market, investor, date_str)
        
        print(f"  [KrxFetcherAdapter] Fetching data for {market} ({investor}) on {date_str}")
        
        # 1. Generate OTP
        otp_response = self.scraper.post(self.OTP_URL, data=params, verify=True)
        otp_response.raise_for_status()
        otp = otp_response.text.strip()
        
        if not otp or len(otp) < 50:
            raise ConnectionError(f"OTP acquisition failed. Response: {otp[:50]}")
        
        # 2. Download File
        download_params = {"code": otp}
        file_response = self.scraper.post(self.DOWNLOAD_URL, data=download_params, verify=True)
        file_response.raise_for_status()
        
        return file_response.content
