import sys
import os

# Add src to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

try:
    from finance_data.repository import FinanceDataReaderRepository
    from finance_data.service import TickerMappingService
    
    print("Initializing Repository...")
    repo = FinanceDataReaderRepository()
    
    print("Initializing Service...")
    service = TickerMappingService(repo)
    
    target_name = "삼성전자"
    print(f"Searching for code of '{target_name}'...")
    code = service.get_code(target_name)
    
    if code == "005930":
        print(f"SUCCESS: {target_name} -> {code}")
    else:
        print(f"FAILURE: {target_name} -> {code} (Expected 005930)")

    target_name = "카카오"
    print(f"Searching for code of '{target_name}'...")
    code = service.get_code(target_name)
    
    if code:
        print(f"SUCCESS: {target_name} -> {code}")
    else:
        print(f"FAILURE: Could not find {target_name}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
