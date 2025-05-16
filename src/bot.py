import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from process_data import get_complete_financials
from export_data import export_to_csv

# Set up logging to show bot activity in the terminal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get the Telegram Bot token from the environment variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Set this in your environment

# Dictionary of ratio explanations
RATIO_EXPLANATIONS = {
    "per": "📈 *PER (Price to Earnings Ratio)*\nMeasures how much investors are willing to pay per dollar of earnings.\nFormula: Price / EPS",
    "ps": "📊 *PS (Price to Sales Ratio)*\nCompares a company’s stock price to its revenues.\nFormula: Price / Sales per Share",
    "pbv": "🏦 *PBV (Price to Book Value)*\nCompares stock price with the book value of equity.\nFormula: Price / Book Value per Share",
    "pcf": "💵 *PCF (Price to Cash Flow)*\nCompares price with the company's operating cash flow.\nFormula: Price / Cash Flow per Share",
    "roe": "🔁 *ROE (Return on Equity)*\nMeasures how effectively a company uses shareholder equity to generate profit.\nFormula: Net Income / Shareholder Equity",
    "de": "💼 *Debt-to-Equity Ratio*\nIndicates how much debt a company uses to finance assets vs. equity.\nFormula: Total Debt / Total Equity",
    "current_ratio": "💧 *Current Ratio*\nMeasures the company's ability to cover short-term obligations.\nFormula: Current Assets / Current Liabilities",
    "quick_ratio": "⚡ *Quick Ratio*\nA more strict measure of liquidity, excluding inventory.\nFormula: (Current Assets - Inventory) / Current Liabilities",
    "cash_ratio": "💸 *Cash Ratio*\nIndicates a company's ability to pay off short-term liabilities with cash and cash equivalents.\nFormula: Cash / Current Liabilities",
    "inventory_turnover": "📦 *Inventory Turnover*\nShows how many times inventory is sold and replaced over a period.\nFormula: Cost of Goods Sold / Average Inventory",
    "days_inventory": "📅 *Days Inventory*\nAverage number of days the company holds inventory before selling.\nFormula: 365 / Inventory Turnover",
    "asset_turnover": "🔄 *Asset Turnover*\nMeasures how efficiently a company uses assets to generate revenue.\nFormula: Revenue / Total Assets",
    "intrinsic_industry": "🧠 *Intrinsic Value based on Industry Average*\nAverage of intrinsic values based on peer multiples (PER, PS, PBV, PCF).",
    "intrinsic_final": "🎯 *Final Intrinsic Value*\nAverage of industry-based and historical-based intrinsic values. Combines market and historical perspectives.",
    "intrinsic_historical": "📈 *Estimated Fair Price based on historical PS+PBV (5Y)*\nAverage of fair price calculated using 5Y historical Price/Sales and Price/Book ratios."
}

# Format financial data into a readable text message
def format_ratios_text(data):
    lines = []

    # Categorías definidas
    valuation_keys = [
        "PER (Current FMP)",
        "PS (Current FMP)",
        "PBV (Current FMP)",
        "Price to Cash Flow (PCF)"
    ]
    liquidity_keys = [
        "Current Ratio",
        "Quick Ratio",
        "Cash Ratio",
        "Inventory Turnover",
        "Days Inventory",
        "Asset Turnover"
    ]
    intrinsic_keys = [
        "Intrinsic Value based on Peer PER",
        "Intrinsic Value based on Peer PS",
        "Intrinsic Value based on Peer PBV",
        "Intrinsic Value based on Peer PCF",
        "Intrinsic Value based on Industry Average",
        "Estimated Fair Price based on historical PS+PBV (5Y)",
        "Final Intrinsic Value (Avg Industry + Historical)"
    ]

    for row in data:
        company = row.get("Company", "Unknown")
        lines.append(f"\n📊 *{company}*")

        # PRICE
        if "PRICE" in row:
            lines.append(f"💵 Price: {row['PRICE']}")

        # Valuation Ratios
        lines.append("\n📈 *Valuation Ratios*")
        for key in valuation_keys:
            if key in row:
                lines.append(f"- {key}: {row[key]}")

        # Liquidity & Efficiency
        lines.append("\n💰 *Liquidity & Efficiency*")
        for key in liquidity_keys:
            if key in row:
                lines.append(f"- {key}: {row[key]}")

        # Intrinsic Value Estimates
        lines.append("\n🎯 *Intrinsic Value Estimates*")
        for key in intrinsic_keys:
            if key in row:
                lines.append(f"- {key}: {row[key]}")

        # Recommendation
        if "RECOMMENDATION" in row:
            lines.append(f"\n🧠 *Recommendation*: {row['RECOMMENDATION']}")

    return "\n".join(lines)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to the Financial Analysis Bot! Use /analize followed by tickers to get started. Example: /analize GOOGL,AAPL,MSFT")

# /analize command handler
async def analize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Validate input
    if not context.args:
        await update.message.reply_text("❗Please provide tickers. Example: /analize GOOGL,AAPL")
        return

    # Parse and clean tickers
    tickers = [ticker.strip().upper() for ticker in context.args[0].split(",")]
    financial_data = []
    per_list = []

    # Fetch data for each ticker
    for ticker in tickers:
        data = get_complete_financials(ticker)
        if data:
            financial_data.append(data)
            per = data.get("PER (Current FMP)")
            if isinstance(per, (int, float)):
                per_list.append(per)

    if not financial_data:
        await update.message.reply_text("❗Could not retrieve valid data for the tickers provided.")
        return
    
    # Calculate Intrinsic Value based on Peer PER
    peer_avg_per = sum(per_list) / len(per_list) if per_list else None
    for row in financial_data:
        price = row.get("PRICE")
        ticker_per = row.get("PER (Current FMP)")
        if price and ticker_per and peer_avg_per:
            row["Intrinsic Value based on Peer PER"] = round((price * peer_avg_per) / ticker_per, 3)

    # Send a formatted text summary of the financials
    text = format_ratios_text(financial_data)
    await update.message.reply_markdown(text)

    # Export results to CSV and send the file to the user
    # export_to_csv(financial_data, filename="financial_summary.csv")
    # await update.message.reply_document(document=open("../data/financial_summary.csv", "rb"))

# Handler for ratio explanation commands
async def explain_ratio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.lstrip("/").lower()
    explanation = RATIO_EXPLANATIONS.get(cmd)

    if explanation:
        await update.message.reply_markdown(explanation)
    else:
        await update.message.reply_text("❓ Sorry, I don't have information on that ratio.")

# Entry point of the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analize", analize))

    # Register commands for explanations
    for ratio_cmd in RATIO_EXPLANATIONS.keys():
        app.add_handler(CommandHandler(ratio_cmd, explain_ratio))
        
    print("🤖 Bot is running...")
    app.run_polling()
