import os
import requests

API_KEY = os.getenv("FMP_API_KEY")
if not API_KEY:
    raise ValueError("API KEY not found. Set the 'FMP_API_KEY' environment variable.")


def get_fmp_ratios(ticker: str):
    """
    Fetch financial ratios and price from FMP using STABLE endpoints.
    Returns a dict with the metrics your bot/app expects, or None if it fails.
    """
    ticker = ticker.strip().upper()

    # ✅ STABLE endpoints (replace legacy /api/v3)
    ratios_url = "https://financialmodelingprep.com/stable/ratios"
    quote_url = "https://financialmodelingprep.com/stable/quote"

    # Some FMP endpoints accept optional params like period/limit.
    # If your plan ignores them, it still returns data; if not supported, it won't break.
    ratios_params = {
        "symbol": ticker,
        "apikey": API_KEY,
        "period": "annual",
        "limit": 5,
    }
    quote_params = {"symbol": ticker, "apikey": API_KEY}

    try:
        response_ratios = requests.get(ratios_url, params=ratios_params, timeout=20)
        response_quote = requests.get(quote_url, params=quote_params, timeout=20)
    except requests.RequestException as e:
        print(f"Request error for {ticker}: {e}")
        return None

    if response_ratios.status_code != 200 or response_quote.status_code != 200:
        print(f"Failed to retrieve data from {ticker}")
        print(f"Ratios status: {response_ratios.status_code}, Quote status: {response_quote.status_code}")
        return None

    ratios_data = response_ratios.json()
    quote_data = response_quote.json()

    if not isinstance(ratios_data, list) or not ratios_data:
        print(f"No ratios data available for {ticker}")
        return None

    if not isinstance(quote_data, list) or not quote_data:
        print(f"No quote data available for {ticker}")
        return None

    # Most recent ratios (index 0)
    latest_ratios = ratios_data[0]

    # 5 years ago ratios (index 4 if available)
    five_years_ago_ratios = ratios_data[4] if len(ratios_data) > 4 else {}

    # Price from quote endpoint
    latest_price = quote_data[0].get("price")

    # Current valuation ratios
    current_per = latest_ratios.get("priceEarningsRatio")
    current_ps = latest_ratios.get("priceSalesRatio")
    current_pbv = latest_ratios.get("priceToBookRatio")

    # Historical fair prices based on 5Y ratios
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

    # Average of fair price from historical PS + PBV
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

    # Round numeric values
    for key, value in list(fmp_ratios.items()):
        if isinstance(value, (int, float)):
            fmp_ratios[key] = round(value, 3)

    return fmp_ratios
