import requests

BOT_TOKEN = '8092692270:AAE1AATHk0Qyg_okjktO2gShivQNFInfCLs'
CHAT_ID = '431116432'
LBANK_API_URL = 'https://api.lbank.info/v2/ticker.do?symbol=all'

def get_lbank_tickers():
    try:
        response = requests.get(LBANK_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"خطا در دریافت اطلاعات از LBank: {e}")
        return None

    if data.get('result') != 'true' or 'data' not in data:
        print("پاسخ نامعتبر از LBank.")
        return None

    tickers = data['data']
    changes = []
    for ticker in tickers:
        symbol = ticker.get('symbol', '').upper()
        change_percent = ticker.get('change', 0) * 100  # تبدیل به درصد
        changes.append(f"{symbol}: {change_percent:.2f}%")

    return changes

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"خطا در ارسال پیام به تلگرام: {e}")
        return False

def main():
    changes = get_lbank_tickers()
    if changes is None:
        send_to_telegram("❌ خطا در دریافت اطلاعات از LBank")
        return

    message = "📊 تغییرات ۲۴ ساعته بازار LBank:\n\n" + "\n".join(changes)
    send_to_telegram(message)

if __name__ == '__main__':
    main()
