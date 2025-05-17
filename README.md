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
✅ Includes Telegram bot for mobile interaction with `/analize` and ratio commands  
✅ `/help` command provides full menu of available bot functionality

## Installation

Ensure you have Python installed (version 3.7+ recommended). Then, install the required dependencies:

```bash
pip install requests pandas python-telegram-bot
```

## Environment Setup

Set your FMP API key and Telegram Bot token as environment variables to keep them secure:

**Windows (Command Prompt):**

```cmd
set FMP_API_KEY=your_fmp_api_key
set TELEGRAM_BOT_TOKEN=your_bot_token
```

**Linux/macOS (Terminal):**

```bash
export FMP_API_KEY=your_fmp_api_key
export TELEGRAM_BOT_TOKEN=your_bot_token
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
3. Run the script to analyze financial data via CLI:

   ```bash
   python main.py
   ```
4. Or run the Telegram bot:

   ```bash
   python bot.py
   ```

## Output

* The program generates a CSV file with:
  * Key ratios and values as rows
  * Tickers as columns
  * An `AVERAGE` column per metric
  * Additional rows for calculated intrinsic values and recommendations

* The Telegram bot returns:
  * Cleanly formatted ratio data per ticker
  * Intrinsic value estimates
  * Investment recommendation
  * Explanatory commands like `/per`, `/ps`, etc.

## Roadmap

* ✅ Extract and process data from FMP API
* ✅ Compute intrinsic value estimates based on peer and historical analysis
* ✅ Export CSV with clean formatting and summary
* ✅ Telegram Bot integration for mobile and remote interaction
* 🚀 Future: Web app with interactive visual explanations and metrics

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss proposed modifications.

## License

MIT License
