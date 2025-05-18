import requests

# تنظیمات تلگرام
BOT_TOKEN = '8092692270:AAE1AATHk0Qyg_okjktO2gShivQNFInfCLs'
CHAT_ID = '431116432'

# 1. گرفتن داده از بایننس
def get_binance_tickers():
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# 2. فیلتر ارزهایی با تغییر مثبت بیشتر از 5٪
def filter_top_gainers(tickers, threshold=5.0):
    gainers = []
    for ticker in tickers:
        symbol = ticker['symbol']
        price_change_percent = float(ticker['priceChangePercent'])

        if price_change_percent >= threshold:
            gainers.append((symbol, price_change_percent))
    return gainers

# 3. ارسال پیام به تلگرام
def send_to_telegram(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)

# 4. اجرای مراحل
def main():
    tickers = get_binance_tickers()
    gainers = filter_top_gainers(tickers)

    if not gainers:
        message = "🚫 هیچ ارزی با رشد بیش از ۵٪ در ۲۴ ساعت گذشته پیدا نشد."
    else:
        message = "📈 *ارزهای با رشد بیش از ۵٪ در ۲۴ ساعت گذشته:*\n"
        for symbol, change in gainers:
            message += f"• `{symbol}` ➜ +{change:.2f}%\n"

    send_to_telegram(message)

if __name__ == '__main__':
    main()
