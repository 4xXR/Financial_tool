import yfinance as yf

def get_financial_ratios_yahoo(ticker):
    """Retrieves key financial ratios from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    info = stock.info

    # Extract key financial ratios
    yahoo_ratios = {
        "Company": ticker,
        "PER (P/E Ratio)": info.get("trailingPE"),
        "PBV (Price to Book)": info.get("priceToBook"),
        "ROE (Return on Equity)": info.get("returnOnEquity"),
        "Net Margin": info.get("profitMargins"),
        "Debt/Equity": info.get("debtToEquity"),
        "PS (Price to Sales)": info.get("priceToSalesTrailing12Months"),
    }

    return yahoo_ratios