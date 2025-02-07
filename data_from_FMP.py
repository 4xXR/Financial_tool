import os
import requests
import pandas as pd

API_KEY = os.getenv("FMP_API_KEY")

if not API_KEY:
    raise ValueError("API KEY not found. Set the 'FMP_API_KEY' environment variable.")

def get_fmp_ratios(ticker):
    """
    Fetches financial ratios from Financial Modeling Prep (FMP) API.

    Parameters:
    ticker (str): The stock symbol (e.g., "GOOGL").

    Returns:
    dict: Dictionary containing key financial ratios.
    """

    base_url = "https://financialmodelingprep.com/api/v3"
    ratios_url = f"{base_url}/ratios/{ticker}?apikey={API_KEY}"

    response = requests.get(ratios_url)

    if response.status_code != 200:
        print(f"Failed to retrieve data from {ticker}")
        return None
    
    data = response.json()
    
    if not data:
        print(f"No data available for {ticker}")
        return None
    
    # Extract the most recent financial ratios
    latest_ratios = data[0]

    ratios = {
        "Company": ticker,
        "Current Ratio": latest_ratios.get("currentRatio"),
        "Quick Ratio": latest_ratios.get("quickRatio"),
        "Cash Ratio": latest_ratios.get("cashRatio"),
        "Inventory Turnover": latest_ratios.get("inventoryTurnover"),
        "Days Inventory": latest_ratios.get("daysOfInventoryOutstanding"),
        "Asset Turnover": latest_ratios.get("assetTurnover"),
        "Price to Cash Flow (PCF)": latest_ratios.get("priceCashFlowRatio"),
    }

    return ratios

# Example: Fetch ratios for Google (GOOGL)
ticker = "GOOGL"
fmp_ratios = get_fmp_ratios(ticker)

# Convert results to a Pandas DataFrame
if fmp_ratios:
    df_fmp_ratios = pd.DataFrame([fmp_ratios])
    print(df_fmp_ratios)
else:
    print("Failed to retrieve financial ratios")