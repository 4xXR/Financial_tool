import datetime
import pandas as pd

def export_to_csv(data, filename="../data/financial_data.csv"):
    """Exports financial data to a timestamped CSV file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"../data/financial_data_{timestamp}.csv"

    df = pd.DataFrame(data)
    df = df.set_index("Company").T  # Set tickers as columns, financial metrics as rows
    df.index.name = "RATIOS"

    df.to_csv(filename)
    print(f"Data succesfully saved to {filename}")