import os
import requests

API_KEY = os.getenv("FMP_API_KEY")

if not API_KEY:
    raise ValueError("API KEY not found. Set the 'FMP_API_KEY' environment variable.")

def get_fmp_ratios(ticker):
    """Fetches missing financial ratios from Financial Modeling Prep (FMP) API."""
    base_url = "https://financialmodelingprep.com/api/v3"
    ratios_url = f"{base_url}/ratios/{ticker}?apikey={API_KEY}"
    price_url = f"{base_url}/otc/real-time-price/{ticker}?apikey={API_KEY}"

    response_ratios = requests.get(ratios_url)
    response_price = requests.get(price_url)

    if response_ratios.status_code != 200 or response_price.status_code != 200:
        print(f"Failed to retrieve data from {ticker}")
        return None
    
    ratios_data = response_ratios.json()
    price_data = response_price.json()
    
    data = {
        "ratios": ratios_data,
        "price": price_data
    }

    if not data:
        print(f"No data available for {ticker}")
        return None
    
    # Extract the most recent financial ratios
    latest_ratios = data["ratios"][0]

    # Extract financial ratios from 5 years ago
    five_years_ago_ratios = data ["ratios"][4]

    # Extract the most recent price
    latest_price = data["price"][0]

    # Price relative to historical valuation values
    price_to_historical_per = latest_price.get("lastSalePrice") * five_years_ago_ratios.get("priceEarningsRatio")
    price_to_historical_ps = latest_price.get("lastSalePrice") * five_years_ago_ratios.get("priceSalesRatio")
    price_to_historical_pbv = latest_price.get("lastSalePrice") * five_years_ago_ratios.get("priceToBookRatio")

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
        "PRICE" : latest_price.get("lastSalePrice"),
        "Price relative to historical PER (5Y)": price_to_historical_per,
        "Price relative to historical PS (5Y)": price_to_historical_ps,
        "Price relative to historical PBV (5Y)": price_to_historical_pbv,
    }

    return fmp_ratios