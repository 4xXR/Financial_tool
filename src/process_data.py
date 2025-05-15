# from fetch_yahoo import get_financial_ratios_yahoo
from fetch_fmp import get_fmp_ratios

def get_complete_financials(ticker):
    """
    Combines financial data from Yahoo Finance and FMP API
    """
    # yahoo_data = get_financial_ratios_yahoo(ticker)
    fmp_data = get_fmp_ratios(ticker)

    if not fmp_data:
        print(f"Skipping {ticker} due to missing data")
        return None
    
    # Merge Yahoo and FMP data
    # complete_data = {**yahoo_data, **fmp_data}
    return fmp_data