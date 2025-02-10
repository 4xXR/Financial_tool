import os
import requests

API_KEY = os.getenv("FMP_API_KEY")

if not API_KEY:
    raise ValueError("API KEY not found. Set the 'FMP_API_KEY' environment variable.")

def get_fmp_ratios(ticker):
    """Fetches missing financial ratios from Financial Modeling Prep (FMP) API."""
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

    # Extract financial ratios from 5 years ago
    five_years_ago_ratios = data [4]

    fmp_ratios = {
        "Company": ticker,
        "Current Ratio": latest_ratios.get("currentRatio"),
        "Quick Ratio": latest_ratios.get("quickRatio"),
        "Cash Ratio": latest_ratios.get("cashRatio"),
        "Inventory Turnover": latest_ratios.get("inventoryTurnover"),
        "Days Inventory": latest_ratios.get("daysOfInventoryOutstanding"),
        "Asset Turnover": latest_ratios.get("assetTurnover"),
        "Price to Cash Flow (PCF)": latest_ratios.get("priceCashFlowRatio"),
        "5Y ago PER (P/E Ratio)": five_years_ago_ratios.get("priceEarningsRatio"),
        "5Y ago PS (Price to Sales)": five_years_ago_ratios.get("priceSalesRatio"),
        "5Y ago PBV (Price to Book)": five_years_ago_ratios.get("priceToBookRatio"),
        "PRICE" : latest_ratios.get("lastSalePrice"),
        #"5Y ago priceFairValue": five_years_ago_ratios.get("priceFairValue"),
    }

    return fmp_ratios