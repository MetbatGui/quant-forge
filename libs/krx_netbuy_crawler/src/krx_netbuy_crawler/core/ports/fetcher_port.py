from abc import ABC, abstractmethod

class FetcherPort(ABC):
    """
    Interface for fetching data from external sources (KRX).
    """
    
    @abstractmethod
    def fetch_net_value_data(self, market: str, investor: str, date_str: str) -> bytes:
        """
        Fetches the net buy value data from KRX.
        
        Args:
            market (str): Market type ('KOSPI' or 'KOSDAQ').
            investor (str): Investor type ('Foreigner' or 'Institution').
            date_str (str): Date string in 'YYYYMMDD' format.
            
        Returns:
            bytes: The raw content of the fetched data (typically Excel file bytes).
        """
        pass
