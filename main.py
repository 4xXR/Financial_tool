import os
import requests
import yfinance as yf
import pandas as pd

API_KEY = os.getenv("FMP_API_KEY")

if not API_KEY:
    raise ValueError("API KEY not found. Set the 'FMP_API_KEY' environment variable.")

def get_financial_ratios_yahoo(ticker):
    """
    Retrieves key financial ratios for a company from Yahoo Finance.

    Parameters:
    ticker (str): The stock symbol of the company (e.g., "GOOGL", "AAPL").

    Returns:
    dict: Dictionary containing financial ratios.
    """
    stock = yf.Ticker(ticker)

    # Extract key financial ratios
    yahoo_ratios = {
        "Company": ticker,
        "PER (P/E Ratio)": stock.info.get("trailingPE"),
        "PBV (Price to Book)": stock.info.get("priceToBook"),
        "ROE (Return on Equity)": stock.info.get("returnOnEquity"),
        "Net Margin": stock.info.get("profitMargins"),
        "Debt/Equity": stock.info.get("debtToEquity"),
        "PS (Price to Sales)": stock.info.get("priceToSalesTrailing12Months"),
    }

    return yahoo_ratios

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

    fmp_ratios = {
        "Company": ticker,
        "Current Ratio": latest_ratios.get("currentRatio"),
        "Quick Ratio": latest_ratios.get("quickRatio"),
        "Cash Ratio": latest_ratios.get("cashRatio"),
        "Inventory Turnover": latest_ratios.get("inventoryTurnover"),
        "Days Inventory": latest_ratios.get("daysOfInventoryOutstanding"),
        "Asset Turnover": latest_ratios.get("assetTurnover"),
        "Price to Cash Flow (PCF)": latest_ratios.get("priceCashFlowRatio"),
    }

    return fmp_ratios

def get_complete_financials(ticker):
    """
    Combines financial data from Yahoo Finance and FMP API.

    Parameters:
    ticker (str): The stock symbol (e.g., "GOOGL").

    Returns:
    dict: Combined dictionary of financial ratios.
    """
    yahoo_data = get_financial_ratios_yahoo(ticker)
    fmp_data = get_fmp_ratios(ticker)

    if not yahoo_data or not fmp_data:
        print(f"Skipping {ticker} due to missing data")
        return None
    
    # Merge Yahoo and FMP data
    complete_data = {**yahoo_data, **fmp_data}
    return complete_data

    

# List of companies to analyze
tickers = ["GOOGL", "AAPL", "MSFT"]  # Example tickers

# Retieves ratios for each company
financial_data = [get_complete_financials(ticker) for ticker in tickers if get_complete_financials(ticker) is not None]

# Create a DataFrame for better visualization
df_financial_ratios = pd.DataFrame(financial_data)

# Display results
print(df_financial_ratios)