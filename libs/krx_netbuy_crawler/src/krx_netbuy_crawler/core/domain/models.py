from datetime import date
from pydantic import BaseModel, Field

class KrxNetBuyItem(BaseModel):
    """
    KRX 순매수 데이터(일별)의 단일 행을 나타냅니다.
    """
    date: date
    market: str = Field(..., description="시장 구분: 'KOSPI' 또는 'KOSDAQ'")
    investor: str = Field(..., description="투자자 구분: 'Foreigner'(외국인) 또는 'Institution'(기관)")
    name: str = Field(..., description="종목명")
    net_buy_amount: int = Field(..., description="순매수 금액 (원 단위)")

class WatchlistItem(BaseModel):
    """
    일일 관심 종목으로 선정된 종목을 나타냅니다.
    """
    date: date
    name: str = Field(..., description="종목명")
    market: str = Field(..., description="시장 구분")
