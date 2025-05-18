import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from process_data import get_complete_financials
# from export_data import export_to_csv

# Set up logging to show bot activity in the terminal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get the Telegram Bot token from the environment variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Set this in your environment

# Dictionary of ratio explanations
RATIO_EXPLANATIONS = {
    "per": "📈 *PER (Price to Earnings Ratio)*\nMeasures how much investors are willing to pay per dollar of earnings.\nFormula: Price / EPS\n👉 Lower PER (10–20) may indicate undervaluation, higher PER (>30) may suggest overvaluation or growth expectations.",
    "ps": "📊 *PS (Price to Sales Ratio)*\nCompares a company’s stock price to its revenues.\nFormula: Price / Sales per Share\n👉 PS < 2 is generally considered good for value investors.",
    "pbv": "🏦 *PBV (Price to Book Value)*\nCompares stock price with the book value of equity.\nFormula: Price / Book Value per Share\n👉 PBV < 1 suggests undervaluation, but PBV between 1–3 is typical.",
    "pcf": "💵 *PCF (Price to Cash Flow)*\nCompares price with the company's operating cash flow.\nFormula: Price / Cash Flow per Share\n👉 PCF < 10 is often seen as attractive.",
    "roe": "🔁 *ROE (Return on Equity)*\nMeasures how effectively a company uses shareholder equity to generate profit.\nFormula: Net Income / Shareholder Equity\n👉 ROE > 15% is considered strong.",
    "de": "💼 *Debt-to-Equity Ratio*\nIndicates how much debt a company uses to finance assets vs. equity.\nFormula: Total Debt / Total Equity\n👉 D/E < 1 is typically considered healthy, but varies by industry.",
    "current_ratio": "💧 *Current Ratio*\nMeasures the company's ability to cover short-term obligations.\nFormula: Current Assets / Current Liabilities\n👉 Ratio > 1 is good; >2 may indicate inefficiency.",
    "quick_ratio": "⚡ *Quick Ratio*\nA more strict measure of liquidity, excluding inventory.\nFormula: (Current Assets - Inventory) / Current Liabilities\n👉 Ratio > 1 is healthy.",
    "cash_ratio": "💸 *Cash Ratio*\nIndicates a company's ability to pay off short-term liabilities with cash and cash equivalents.\nFormula: Cash / Current Liabilities\n👉 Ratio > 0.5 is good, but too high may suggest underutilization.",
    "inventory_turnover": "📦 *Inventory Turnover*\nShows how many times inventory is sold and replaced over a period.\nFormula: Cost of Goods Sold / Average Inventory\n👉 Higher is better; <2 might indicate overstocking.",
    "days_inventory": "📅 *Days Inventory*\nAverage number of days the company holds inventory before selling.\nFormula: 365 / Inventory Turnover\n👉 Lower is better; <100 is considered efficient.",
    "asset_turnover": "🔄 *Asset Turnover*\nMeasures how efficiently a company uses assets to generate revenue.\nFormula: Revenue / Total Assets\n👉 Ratio > 1 is ideal for asset-light businesses.",
    "intrinsic_industry": "🧠 *Intrinsic Value based on Industry Average*\nAverage of intrinsic values based on peer multiples (PER, PS, PBV, PCF).\n👉 Higher than current price suggests undervaluation.",
    "intrinsic_final": "🎯 *Final Intrinsic Value*\nAverage of industry-based and historical-based intrinsic values. Combines market and historical perspectives.\n👉 Compares favorably to current price for investment potential.",
    "intrinsic_historical": "📈 *Estimated Fair Price based on historical PS+PBV (5Y)*\nAverage of fair price calculated using 5Y historical Price/Sales and Price/Book ratios.\n👉 Helps assess relative valuation over time."
}

# /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📘 Available Commands:\n"
        "/start - Show welcome message\n"
        "/help - Show this help menu\n"
        "/analize TICKER1,TICKER2 - Analyze one or more stock tickers\n\n"
        "📊 Ratio Explanations:\n"
        "/per - Price to Earnings\n"
        "/ps - Price to Sales\n"
        "/pbv - Price to Book Value\n"
        "/pcf - Price to Cash Flow\n"
        "/roe - Return on Equity\n"
        "/de - Debt to Equity\n"
        "/current_ratio - Current Ratio\n"
        "/quick_ratio - Quick Ratio\n"
        "/cash_ratio - Cash Ratio\n"
        "/inventory_turnover - Inventory Turnover\n"
        "/days_inventory - Days Inventory\n"
        "/asset_turnover - Asset Turnover\n"
        "/intrinsic_industry - Intrinsic Value (Industry)\n"
        "/intrinsic_historical - Historical Fair Value\n"
        "/intrinsic_final - Final Intrinsic Value"
    )
    await update.message.reply_text(help_text)

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
    logging.info("✅ /start command received")
    await update.message.reply_text("👋 Welcome to the Financial Analysis Bot! Use /analize followed by tickers to get started. Example: /analize GOOGL,AAPL,MSFT")

# /analize command handler
async def analize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Validate input
    if not context.args:
        logging.info("✅ /analize command received")
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

        # Additional intrinsic values: PS, PBV, PCF
    def safe_avg(lst):
        return sum(lst) / len(lst) if lst else None

    ps_list = [r.get("PS (Current FMP)") for r in financial_data if isinstance(r.get("PS (Current FMP)"), (int, float))]
    pbv_list = [r.get("PBV (Current FMP)") for r in financial_data if isinstance(r.get("PBV (Current FMP)"), (int, float))]
    pcf_list = [r.get("Price to Cash Flow (PCF)") for r in financial_data if isinstance(r.get("Price to Cash Flow (PCF)"), (int, float))]

    avg_ps = safe_avg(ps_list)
    avg_pbv = safe_avg(pbv_list)
    avg_pcf = safe_avg(pcf_list)

    for row in financial_data:
        price = row.get("PRICE")

        ps = row.get("PS (Current FMP)")
        pbv = row.get("PBV (Current FMP)")
        pcf = row.get("Price to Cash Flow (PCF)")

        val_ps = (price * avg_ps) / ps if price and ps and avg_ps else None
        val_pbv = (price * avg_pbv) / pbv if price and pbv and avg_pbv else None
        val_pcf = (price * avg_pcf) / pcf if price and pcf and avg_pcf else None

        if val_ps: row["Intrinsic Value based on Peer PS"] = round(val_ps, 3)
        if val_pbv: row["Intrinsic Value based on Peer PBV"] = round(val_pbv, 3)
        if val_pcf: row["Intrinsic Value based on Peer PCF"] = round(val_pcf, 3)

        # Industry average value
        values = [v for v in [val_ps, val_pbv, val_pcf, row.get("Intrinsic Value based on Peer PER")] if v]
        industry_avg = safe_avg(values)
        if industry_avg:
            row["Intrinsic Value based on Industry Average"] = round(industry_avg, 3)

        # Final intrinsic value with historical PS+PBV
        historical = row.get("Estimated Fair Price based on historical PS+PBV (5Y)")
        if industry_avg and historical:
            row["Final Intrinsic Value (Avg Industry + Historical)"] = round((industry_avg + historical) / 2, 3)

        # Recommendation
        final_intrinsic = row.get("Final Intrinsic Value (Avg Industry + Historical)")
        if price and final_intrinsic:
            diff = (final_intrinsic - price) / price
            if diff > 0.10:
                row["RECOMMENDATION"] = "Underpriced"
            elif diff < -0.10:
                row["RECOMMENDATION"] = "Overpriced"
            else:
                row["RECOMMENDATION"] = "Fairly Priced"

    # Send a formatted text summary of the financials
    text = format_ratios_text(financial_data)
    #await update.message.reply_markdown(text)
    print(text)
    # Telegram's character limit per message is 4096, use 4000 to be safe
    for chunk in [text[i:i + 4000] for i in range(0, len(text), 4000)]:
        await update.message.reply_markdown(chunk)

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
    app.add_handler(CommandHandler("help", help_command))

    # Register commands for explanations
    for ratio_cmd in RATIO_EXPLANATIONS.keys():
        app.add_handler(CommandHandler(ratio_cmd, explain_ratio))

        # Dummy HTTP server to keep port open for Render Web Service
    import threading
    import http.server
    import socketserver

    def run_dummy_server():
        port = int(os.environ.get("PORT", 10000)) # Use PORT for Render
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            logging.info(f"🌐 Dummy web server running on port {port}")
            httpd.serve_forever()

    threading.Thread(target=run_dummy_server, daemon=True).start()

    print("🤖 Bot is running...")
    app.run_polling()