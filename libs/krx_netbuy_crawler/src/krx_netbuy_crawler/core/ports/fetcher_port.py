from abc import ABC, abstractmethod

class FetcherPort(ABC):
    """
    외부 소스(KRX)로부터 데이터를 가져오기 위한 인터페이스입니다.
    """
    
    @abstractmethod
    def fetch_net_value_data(self, market: str, investor: str, date_str: str) -> bytes:
        """
        KRX에서 순매수 데이터를 가져옵니다.
        
        Args:
            market (str): 시장 구분 ('KOSPI' 또는 'KOSDAQ').
            investor (str): 투자자 구분 ('Foreigner' 또는 'Institution').
            date_str (str): 'YYYYMMDD' 형식의 날짜 문자열.
            
        Returns:
            bytes: 가져온 데이터의 원본 콘텐츠 (일반적으로 엑셀 파일 바이트).
        """
        pass
