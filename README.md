# Financial Analysis Tool

## Overview

This project automates the extraction, calculation, and analysis of key financial ratios and estimated intrinsic values for publicly traded companies using data from:

* **Financial Modeling Prep (FMP) API**

The goal is to compare multiple companies based on their valuation, liquidity, efficiency, and intrinsic metrics to support smart investment decisions.

## Features

✅ Fetches valuation ratios (PER, PS, PBV, PCF) and financial metrics from FMP
✅ Calculates intrinsic values using:

* Peer multiples (PER, PS, PBV, PCF)
* Historical 5Y valuation ratios
* Combined industry and historical estimates
  ✅ Computes average values per ratio across all selected tickers
  ✅ Generates investment recommendations (Underpriced, Overpriced, Fairly Priced)
  ✅ Exports results as a structured, readable CSV table
  ✅ Supports multiple stock tickers via dynamic user input
  ✅ All values rounded to 3 decimal places for professional presentation

## Installation

Ensure you have Python installed (version 3.7+ recommended). Then, install the required dependencies:

```bash
pip install requests pandas
```

## Environment Setup

Set your FMP API key as an environment variable to keep it secure:

**Windows (Command Prompt):**

```cmd
set FMP_API_KEY=your_fmp_api_key
```

**Linux/macOS (Terminal):**

```bash
export FMP_API_KEY=your_fmp_api_key
```

## Usage

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/financial-analysis-tool.git
   ```
2. Navigate to the project directory:

   ```bash
   cd financial-analysis-tool
   ```
3. Run the script to analyze financial data:

   ```bash
   python main.py
   ```

## Output

* The program generates a CSV file with:

  * Key ratios and values as rows
  * Tickers as columns
  * An `AVERAGE` column per metric
  * Additional rows for calculated intrinsic values and recommendations

## Roadmap

* ✅ Extract and process data from FMP API
* ✅ Compute intrinsic value estimates based on peer and historical analysis
* ✅ Export CSV with clean formatting and summary
* 🔜 Telegram Bot integration for ticker-based querying
* 🚀 Future: Web app with interactive visual explanations and metrics

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss proposed modifications.

## License

MIT License
