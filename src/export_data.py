import datetime
import pandas as pd

def export_to_csv(data, filename="../data/financial_data.csv"):
    """Exports financial data to a timestamped CSV file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"../data/financial_data_{timestamp}.csv"

    df = pd.DataFrame(data)
    df = df.set_index("Company").T  # Set tickers as columns, financial metrics as rows
    df.index.name = "RATIOS"

    # Calcula row: Intrinsic Value based on Peer PER
    try:
        prices = df.loc["PRICE"] # Extrae la fila de precios actuales, por ticker
        pers = df.loc["PER (Current FMP)"] # Extrae la fila de PER actuales, por ticker
        avg_per = pers.mean() # Calcula el PER promedio de todos los tickers

        # Calculation: Intrinsic Value using average PER
        intrinsic_by_peer = (prices * avg_per) / pers

        # Inserts the result as a new row into the DataFrame
        df.loc["Intrinsic Value based on Peer PER"] = intrinsic_by_peer

    except Exception as e:
        print(f"Error calculating Intrinsic Value based on Peer PER: {e}")

    # Adding 'AVERAGAE' column
    df['AVERAGE']=df.mean(axis=1, numeric_only=True)

    df.to_csv(filename)
    print(f"Data succesfully saved to {filename}")