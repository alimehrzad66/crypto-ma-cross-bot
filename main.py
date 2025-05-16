import requests

BOT_TOKEN = '8092692270:AAE1AATHk0Qyg_okjktO2gShivQNFInfCLs'
CHAT_ID = '431116432'
BITPIN_API_URL = 'https://api.bitpin.ir/v1/market/tickers'

def get_market_prices():
    try:
        response = requests.get(BITPIN_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"خطا در دریافت اطلاعات از بیت‌پین: {e}")
        return None

    tickers = data.get('results')
    if not tickers:
        print("نتایج پیدا نشد.")
        return None

    prices = []
    for item in tickers:
        name = item.get('fa_symbol', 'N/A')
        price = item.get('last_trade_price', 'N/A')
        prices.append(f"{name}: {price:,} تومان")

    return prices

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.status_code == 200

def main():
    prices = get_market_prices()
    if prices is None:
        send_to_telegram("❌ خطا در دریافت اطلاعات از بیت‌پین")
        return

    message = "💰 قیمت لحظه‌ای بازار بیت‌پین:\n\n" + "\n".join(prices)
    send_to_telegram(message)

if __name__ == '__main__':
    main()
