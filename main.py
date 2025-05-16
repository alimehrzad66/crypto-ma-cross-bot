import requests

BOT_TOKEN = '8092692270:AAE1AATHk0Qyg_okjktO2gShivQNFInfCLs'
CHAT_ID = '431116432'

NOBITEX_API_URL = 'https://api.nobitex.ir/market/stats'


def get_market_stats():
    response = requests.post(NOBITEX_API_URL, data={'srcCurrency': 'btc', 'dstCurrency': 'rls'})
    if response.status_code != 200:
        return None

    response = requests.post(NOBITEX_API_URL)
    if response.status_code != 200:
        return None
    
    data = response.json()
    if 'stats' not in data:
        return None

    stats = data['stats']
    changes = []
    for symbol, info in stats.items():
        if '24h' in info and 'change' in info['24h']:
            percent_change = info['24h']['change'] * 100
            changes.append(f"{symbol.upper()}: {percent_change:.2f}%")
    return changes


def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.status_code == 200


def main():
    stats = get_market_stats()
    if stats is None:
        send_to_telegram("❌ خطا در دریافت اطلاعات از نوبیتکس")
        return

    message = "📊 تغییرات ۲۴ ساعته بازار نوبیتکس:\n\n" + "\n".join(stats)
    send_to_telegram(message)


if __name__ == '__main__':
    main()
