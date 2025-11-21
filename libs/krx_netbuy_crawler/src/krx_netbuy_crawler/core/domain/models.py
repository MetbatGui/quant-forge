from datetime import date
from pydantic import BaseModel, Field

class KrxNetBuyItem(BaseModel):
    """
    Represents a single row of KRX Net Buy data (Daily).
    """
    date: date
    market: str = Field(..., description="Market type: 'KOSPI' or 'KOSDAQ'")
    investor: str = Field(..., description="Investor type: 'Foreigner' or 'Institution'")
    name: str = Field(..., description="Stock name")
    net_buy_amount: int = Field(..., description="Net buy amount in Won")

class WatchlistItem(BaseModel):
    """
    Represents a selected stock for the daily watchlist.
    """
    date: date
    name: str = Field(..., description="Stock name")
    market: str = Field(..., description="Market type")
