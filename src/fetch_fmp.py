import os
import requests

# from fetch_yahoo import get_financial_ratios_yahoo  # Temporarily disabled due to Yahoo Finance rate-limiting

API_KEY = os.getenv("FMP_API_KEY")

if not API_KEY:
    raise ValueError("API KEY not found. Set the 'FMP_API_KEY' environment variable.")


def get_fmp_ratios(ticker):
    """Fetches missing financial ratios from Financial Modeling Prep (FMP) API."""
    base_url = "https://financialmodelingprep.com/api/v3"
    ratios_url = f"{base_url}/ratios/{ticker}?apikey={API_KEY}"
    price_url = f"{base_url}/stock/full/real-time-price/{ticker}?apikey={API_KEY}"

    response_ratios = requests.get(ratios_url)
    response_price = requests.get(price_url)

    if response_ratios.status_code != 200 or response_price.status_code != 200:
        print(f"Failed to retrieve data from {ticker}")
        return None

    ratios_data = response_ratios.json()
    price_data = response_price.json()

    if not ratios_data or not price_data:
        print(f"No data available for {ticker}")
        return None

    # Extract the most recent financial ratios
    latest_ratios = ratios_data[0]

    # Extract financial ratios from 5 years ago
    five_years_ago_ratios = ratios_data[4] if len(ratios_data) > 4 else {}

    # Extract the most recent price
    latest_price = price_data[0].get("lastSalePrice")  # adjusted for expected structure

    # === USE FMP FOR CURRENT PER, PS, PBV ===
    current_per = latest_ratios.get("priceEarningsRatio")
    current_ps = latest_ratios.get("priceSalesRatio")
    current_pbv = latest_ratios.get("priceToBookRatio")

    # === COMMENTED YAHOO FINANCE CALLS ===
    # yahoo_data = get_financial_ratios_yahoo(ticker)
    # current_per = yahoo_data.get("PER (P/E Ratio)")
    # current_ps = yahoo_data.get("PS (Price to Sales)")
    # current_pbv = yahoo_data.get("PBV (Price to Book)")

    # === Price to Historical Ratios ===
    price_to_historical_per = (
        (latest_price * five_years_ago_ratios.get("priceEarningsRatio")) / current_per
        if latest_price and five_years_ago_ratios.get("priceEarningsRatio") and current_per
        else None
    )
    
    price_to_historical_ps = (
        (latest_price * five_years_ago_ratios.get("priceSalesRatio")) / current_ps
        if latest_price and five_years_ago_ratios.get("priceSalesRatio") and current_ps
        else None
    )

    price_to_historical_pbv = (
        (latest_price * five_years_ago_ratios.get("priceToBookRatio")) / current_pbv
        if latest_price and five_years_ago_ratios.get("priceToBookRatio") and current_pbv
        else None
    )
    
    # === Estimated Fair Price Based on 5Y PS and PBV ===
    historical_fair_price_5y = None
    if (
        latest_price
        and five_years_ago_ratios.get("priceSalesRatio")
        and current_ps
        and five_years_ago_ratios.get("priceToBookRatio")
        and current_pbv
    ):
        fair_price_ps = (latest_price * five_years_ago_ratios["priceSalesRatio"]) / current_ps
        fair_price_pbv = (latest_price * five_years_ago_ratios["priceToBookRatio"]) / current_pbv
        historical_fair_price_5y = (fair_price_ps + fair_price_pbv) / 2

    # Final financial data output
    fmp_ratios = {
        "Company": ticker,
        "PRICE": latest_price,
        "PER (Current FMP)": current_per,
        "PS (Current FMP)": current_ps,
        "PBV (Current FMP)": current_pbv,
        "5Y ago PER (P/E Ratio)": five_years_ago_ratios.get("priceEarningsRatio"),
        "5Y ago PS (Price to Sales)": five_years_ago_ratios.get("priceSalesRatio"),
        "5Y ago PBV (Price to Book)": five_years_ago_ratios.get("priceToBookRatio"),
        "Estimated Fair Price based on historical PER (5Y)": price_to_historical_per,
        "Estimated Fair Price based on historical PS (5Y)": price_to_historical_ps,
        "Estimated Fair Price based on historical PBV (5Y)": price_to_historical_pbv,
        "Estimated Fair Price based on historical PS+PBV (5Y)": historical_fair_price_5y,
        "Current Ratio": latest_ratios.get("currentRatio"),
        "Quick Ratio": latest_ratios.get("quickRatio"),
        "Cash Ratio": latest_ratios.get("cashRatio"),
        "Inventory Turnover": latest_ratios.get("inventoryTurnover"),
        "Days Inventory": latest_ratios.get("daysOfInventoryOutstanding"),
        "Asset Turnover": latest_ratios.get("assetTurnover"),
        "Price to Cash Flow (PCF)": latest_ratios.get("priceCashFlowRatio"),
    }

    return fmp_ratios
