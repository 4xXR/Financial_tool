from process_data import get_complete_financials
from export_data import export_to_csv

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