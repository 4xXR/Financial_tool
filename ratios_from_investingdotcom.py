import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_investing_ratios(ticker):
    """
    Scrapes financial ratios from Investing.com for a given stock ticker.

    Parameters:
    ticker (str): The stock symbol (e.g., "GOOGL").

    Returns:
    dict: Dictionary containing key financial ratios.
    """

    # Manually get the URL for the stock's financial ratios page
    url = f"https://www.investing.com/equities/{ticker}-ratios"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Request the page
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve data for {ticker}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the ratios table (Inspect Investing.com to confirm the correct class or ID)
    ratios_table = soup.find("table", {"class": "datatable"})  # Adjust selector if necessary

    ratios = {}

    if ratios_table:
        for row in ratios_table:
            for row in ratios_table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) > 1:
                    ratio_name = cols[0].text.strip()
                    ratio_value = cols[1].text.strip()
                    ratios[ratio_name] = ratio_value

    return ratios
    
# Example: Get ratios for Google (GOOGL)
ticker = "google-inc"
investing_ratios = get_investing_ratios(ticker) # This format depends on Investing.com URL

# Convert to DataFrame for readability
df_investing_ratios = pd.DataFrame(list(investing_ratios.items()), columns=["Ratio", "Value"])

# Display results
print(df_investing_ratios)