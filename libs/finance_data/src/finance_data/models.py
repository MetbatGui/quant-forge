from dataclasses import dataclass

@dataclass(frozen=True)
class Ticker:
    """
    주식 종목의 핵심 정보를 담는 불변 데이터 객체입니다.

    Attributes:
        code (str): 종목 코드 (예: 005930)
        name (str): 종목명 (예: 삼성전자)
        market (str): 소속 시장 (예: KOSPI, KOSDAQ)
    """
    code: str
    name: str
    market: str
