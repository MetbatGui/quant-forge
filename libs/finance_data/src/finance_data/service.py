from typing import Dict, Optional, List
from finance_data.models import Ticker
from finance_data.repository import TickerRepository

class TickerMappingService:
    """
    종목 매핑 및 검색 로직을 담당하는 서비스 클래스입니다.
    """

    def __init__(self, repository: TickerRepository):
        """
        TickerService를 초기화합니다.

        Args:
            repository (TickerRepository): 사용할 구체적인 리포지토리 구현체
        """
        self._repo = repository
        self._code_map = self._initialize_map()

    def _initialize_map(self) -> Dict[str, Ticker]:
        """
        리포지토리에서 데이터를 로드하여 검색용 해시맵을 구축합니다.

        Returns:
            Dict[str, Ticker]: {종목명: Ticker객체} 형태의 맵
        """
        tickers = self._repo.load_all()
        return {t.name: t for t in tickers}

    def get_ticker(self, name: str) -> Optional[Ticker]:
        """
        정확한 종목명으로 Ticker 정보를 조회합니다.

        Args:
            name (str): 종목명

        Returns:
            Optional[Ticker]: 해당 종목 객체 또는 None
        """
        return self._code_map.get(name)

    def search_by_keyword(self, keyword: str) -> List[Ticker]:
        """
        키워드가 포함된 모든 종목을 검색합니다.

        Args:
            keyword (str): 검색 키워드

        Returns:
            List[Ticker]: 검색된 종목 리스트
        """
        return [
            ticker 
            for name, ticker in self._code_map.items() 
            if keyword in name
        ]

    def get_code(self, name: str) -> Optional[str]:
        """
        종목명으로 종목 코드를 조회합니다.
        
        Args:
            name (str): 종목명
            
        Returns:
            Optional[str]: 종목 코드 (찾지 못한 경우 None)
        """
        ticker = self.get_ticker(name)
        return ticker.code if ticker else None
