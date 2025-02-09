import datetime
import pandas as pd

def export_to_csv(data, filename="../data/financial_data.csv"):
    """Exports financial data to a timestamped CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"../datafinancial_data_{timestamp}.csv"

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data succesfully saved to {filename}")