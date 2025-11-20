from abc import ABC, abstractmethod
from typing import List
import pandas as pd
import FinanceDataReader as fdr
from finance_data.models import Ticker

class TickerRepository(ABC):
    """
    종목 정보를 제공하는 저장소 인터페이스입니다.
    """
    
    @abstractmethod
    def load_all(self) -> List[Ticker]:
        """
        모든 종목 정보를 로드합니다.
        
        Returns:
            List[Ticker]: 종목 객체 리스트
        """
        pass

class FinanceDataReaderRepository(TickerRepository):
    """
    FinanceDataReader 라이브러리를 사용하여 주식 정보를 가져오는 리포지토리 구현체입니다.
    """

    def load_all(self) -> List[Ticker]:
        """
        KOSPI와 KOSDAQ 시장의 모든 종목을 가져옵니다.
        """
        # KOSPI, KOSDAQ 종목 가져오기
        kospi_df = fdr.StockListing('KOSPI')
        kosdaq_df = fdr.StockListing('KOSDAQ')

        tickers = []
        
        # DataFrame을 Ticker 객체로 변환
        for _, row in kospi_df.iterrows():
            tickers.append(self._row_to_ticker(row, 'KOSPI'))
            
        for _, row in kosdaq_df.iterrows():
            tickers.append(self._row_to_ticker(row, 'KOSDAQ'))
            
        return tickers

    def _row_to_ticker(self, row: pd.Series, market: str) -> Ticker:
        return Ticker(
            code=str(row['Code']),
            name=str(row['Name']),
            market=market
        )
