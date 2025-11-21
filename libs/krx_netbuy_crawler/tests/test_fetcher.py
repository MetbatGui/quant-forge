import os
import sys
import pandas as pd
from io import BytesIO
from krx_netbuy_crawler.infra.adapters.krx_fetcher_adapter import KrxFetcherAdapter

def test_fetch_real_data():
    """
    Tests fetching real data from KRX.
    """
    fetcher = KrxFetcherAdapter()
    date_str = "20251120" # Use a valid past date
    market = "KOSPI"
    investor = "foreigner"
    
    print(f"Fetching data for {market} {investor} on {date_str}...")
    try:
        data = fetcher.fetch_net_value_data(market, investor, date_str)
        print(f"Successfully fetched {len(data)} bytes.")
        
        # Verify it's a valid Excel file
        df = pd.read_excel(BytesIO(data))
        print("Excel file parsed successfully.")
        print(f"Columns: {df.columns.tolist()}")
        print(df.head(3))
        
        # Basic validation
        assert len(data) > 0
        assert not df.empty
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise

if __name__ == "__main__":
    test_fetch_real_data()
