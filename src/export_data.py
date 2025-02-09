import pandas as pd

def export_to_csv(data, filename="../data/financial_data.csv"):
    """Exports financial data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data succesfully saved to {filename}")