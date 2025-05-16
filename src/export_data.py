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

        # === Intrinsic Value by PER ===
        pers = df.loc["PER (Current FMP)"] # Extrae la fila de PER actuales, por ticker
        avg_per = pers.mean() # Calcula el PER promedio de todos los tickers
        intrinsic_peer = (prices * avg_per) / pers
        df.loc["Intrinsic Value based on Peer PER"] = intrinsic_peer

        # === Intrinsic Value by PS ===
        pss = df.loc["PS (Current FMP)"]
        avg_ps = pss.mean()
        intrinsic_ps = (prices * avg_ps) / pss
        df.loc["Intrinsic Value based on Peer PS"] = intrinsic_ps

        # === Intrinsic Value by PBV ===
        pbvs = df.loc["PBV (Current FMP)"]
        avg_pbv = pbvs.mean()
        intrinsic_pbv = (prices * avg_pbv) / pbvs
        df.loc["Intrinsic Value based on Peer PBV"] = intrinsic_pbv

        # === Intrinsic Value by PCF ===
        pcfs = df.loc["Price to Cash Flow (PCF)"]
        avg_pcf = pcfs.mean()
        intrinsic_pcf = (prices * avg_pcf) / pcfs
        df.loc["Intrinsic Value based on Peer PCF"] = intrinsic_pcf

    except Exception as e:
        print(f"Error calculating Intrinsic Values: {e}")

    # Adding 'AVERAGAE' column
    df['AVERAGE']=df.mean(axis=1, numeric_only=True)

    df.to_csv(filename)
    print(f"Data succesfully saved to {filename}")