import os
import requests

from fetch_yahoo import get_financial_ratios_yahoo

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
    
    if not ratios_data or price_data:
        print(f"No data available for {ticker}")
        return None
    
    # Extract the most recent financial ratios
    latest_ratios = ratios_data[0]

    # Extract financial ratios from 5 years ago
    five_years_ago_ratios = ratios_data[4]

    # Extract the most recent price
    latest_price = price_data[0]

    # Price relative to historical valuation values
    yahoo_data = get_financial_ratios_yahoo(ticker)
    current_per = yahoo_data.get("PER (P/E Ratio)")
    current_ps = yahoo_data.get("PS (Price to Sales)")
    current_pbv = yahoo_data.get("PBV (Price to Book)")

    price_to_historical_per = (latest_price.get("lastSalePrice") * five_years_ago_ratios.get("priceEarningsRatio")) / current_per
    price_to_historical_ps = (latest_price.get("lastSalePrice") * five_years_ago_ratios.get("priceSalesRatio")) / current_ps
    price_to_historical_pbv = (latest_price.get("lastSalePrice") * five_years_ago_ratios.get("priceToBookRatio")) / current_pbv

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