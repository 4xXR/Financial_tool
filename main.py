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
    Combines financial data from Yahoo Finance and FMP API
    """
    yahoo_data = get_financial_ratios_yahoo(ticker)
    fmp_data = get_fmp_ratios(ticker)

    if not yahoo_data or not fmp_data:
        print(f"Skipping {ticker} due to missing data")
        return None
    
    # Merge Yahoo and FMP data
    complete_data = {**yahoo_data, **fmp_data}
    return complete_data

def export_to_csv(data, filename="financial_data.csv"):
    """Exports financial data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data succesfully saved to {filename}")

# User input system for ticker selection
def get_user_tickers():
    """Prompts the user to input stock tickers dynamically"""
    tickers = input("Enter stock tickers separated by commas (e.g., GOOGL, AAPL, MSFT): ")
    return [ticker.upper().strip() for ticker in tickers.split(",")]

# Get user-selected tickers
tickers = get_user_tickers()

# Retieves ratios for each company
financial_data = []
for ticker in tickers:
    data = get_complete_financials(ticker) # Call function only one due to API is rate-limited
    if data is not None:
        financial_data.append(data)

# Export results to CSV
if financial_data:
    export_to_csv(financial_data)
else:
    print("Not valid financial data available")