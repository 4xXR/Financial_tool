import yfinance as yf
import pandas as pd

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
    ratios = {
        "Company": ticker,
        "PER (P/E Ratio)": stock.info.get("trailingPE"),
        "PBV (Price to Book)": stock.info.get("priceToBook"),
        "ROE (Return on Equity)": stock.info.get("returnOnEquity"),
        "Net Margin": stock.info.get("profitMargins"),
        "Debt/Equity": stock.info.get("debtToEquity"),
        "PS (Price to Sales)": stock.info.get("priceToSalesTrailing12Months"),
    }

    return ratios

# List of companies to analyze
tickers = ["GOOGL", "AAPL", "MSFT"]  # Google, Apple, Microsoft

# Retieves ratios for each company
financial_data = [get_financial_ratios_yahoo(ticker) for ticker in tickers]

# Create a DataFrame for better visualization
df_financial_ratios = pd.DataFrame(financial_data)

# Display the DataFrame
print(df_financial_ratios)