# Financial Analysis Tool

## Overview
This project automates the extraction and analysis of key financial ratios for stocks using data from:
- **Yahoo Finance** (via `yfinance`)
- **Financial Modeling Prep (FMP) API**

The goal is to compare multiple companies based on their valuation, liquidity, and efficiency ratios to assist in investment decision-making.

## Features
✅ Fetches **valuation ratios** (PER, PBV, ROE, Net Margin, Debt/Equity, PS) from **Yahoo Finance**.
✅ Fetches **liquidity and efficiency ratios** (Current Ratio, Quick Ratio, Inventory Turnover, Asset Turnover, Days Inventory, PCF) from **Financial Modeling Prep API**.
✅ Supports **multiple stock tickers** for analysis.
✅ Combines all data into a structured **Pandas DataFrame**.

## Installation
Ensure you have Python installed (version 3.7+ recommended). Then, install the required dependencies:

```bash
pip install yfinance requests pandas
```

## Environment Setup
Since the **FMP API Key** should not be exposed in the code, store it as an environment variable:

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

## Next Steps
- ✅ **Fetch financial data from Yahoo Finance and FMP API** (Completed)
- 📊 **Add export options (CSV, Excel, JSON)** (Next Step)
- 🔄 **Implement dynamic ticker input (User Selection / File Input)** (Planned)
- 🚀 **Build a simple GUI or Web Interface for easier interaction** (Future Feature)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss proposed modifications.

## License
MIT License


