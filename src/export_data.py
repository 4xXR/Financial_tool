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

    # === Valor intrínseco promedio por industria ===
    try:
        industry_avg = (
            df.loc["Intrinsic Value based on Peer PER"]
            + df.loc["Intrinsic Value based on Peer PS"]
            + df.loc["Intrinsic Value based on Peer PBV"]
            + df.loc["Intrinsic Value based on Peer PCF"]
            ) / 4
        df.loc["Intrinsic Value based on Industry Average"] = industry_avg
    except Exception as e:
        print(f"Error calculating Industry Average Intrinsic Value: {e}")

    # === Valor intrínseco final: media con valor histórico 5Y ===
    try:
        historical_value = df.loc["Estimated Fair Price based on historical PS+PBV (5Y)"]
        final_intrinsic = (industry_avg + historical_value) / 2
        df.loc["Final Intrinsic Value (Avg Industry + Historical)"] = final_intrinsic
    except Exception as e:
        print(f"Error calculating Final Intrinsic Value: {e}")

    # === Generate RECOMMENDATION column ===
    try:
        final_intrinsic = df.loc["Final Intrinsic Value (Avg Industry + Historical)"]
        current_prices = df.loc["PRICE"]

        recommendation = []
        for ticker in df.columns:
            intrinsic = final_intrinsic.get(ticker)
            price = current_prices.get(ticker)

            if not intrinsic or not price:
                recommendation.append("N/A")
            else:
                diff = (intrinsic - price) / price
                if diff > 0.10:
                    recommendation.append("Underpriced")
                elif diff < -0.10:
                    recommendation.append("Overpriced")
                else:
                    recommendation.append("Fairly Priced")

        df.loc["RECOMMENDATION"] = pd.Series(recommendation, index=df.columns).astype(str)
    except Exception as e:
        print(f"Error generating recommendation column: {e}")

    # Recalculate DataFrame with AVERAGE column (correct visibility in CSV)
    try:
        numeric_only_df = df.apply(pd.to_numeric, errors='coerce')  # force conversion
        averages = numeric_only_df.mean(axis=1)

        # Assign the "AVERAGE" column
        df["AVERAGE"] = averages
    except Exception as e:
        print(f"Error calculating AVERAGE column: {e}")

    df = df.round(3)

    df.to_csv(filename)
    print(f"Data succesfully saved to {filename}")