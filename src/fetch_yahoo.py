import yfinance as yf

def get_financial_ratios_yahoo(ticker):
    """Retrieves key financial ratios from Yahoo Finance."""
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