import requests

# تنظیمات تلگرام
BOT_TOKEN = '8092692270:AAE1AATHk0Qyg_okjktO2gShivQNFInfCLs'
CHAT_ID = '431116432'

# 1. گرفتن داده از CoinGecko
def get_coingecko_tickers():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 250,
        'page': 1,
        'price_change_percentage': '24h'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# 2. فیلتر ارزهایی با تغییر مثبت بیشتر از 5٪
def filter_top_gainers(tickers, threshold=5.0):
    gainers = []
    for ticker in tickers:
        change_24h = ticker.get('price_change_percentage_24h', 0)
        if change_24h and change_24h >= threshold:
            gainers.append((ticker['symbol'].upper(), change_24h))
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
    tickers = get_coingecko_tickers()
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
