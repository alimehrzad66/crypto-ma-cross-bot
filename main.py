import requests
import numpy as np

TOKEN = "8092692270:AAE1AATHk0Qyg_okjktO2gShivQNFInfCLs"
CHAT_ID = "431116432"

SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT",
    "SOLUSDT", "AVAXUSDT", "DOGEUSDT", "MATICUSDT", "DOTUSDT",
    "SHIBUSDT", "LTCUSDT", "TRXUSDT", "LINKUSDT", "ATOMUSDT",
    "UNIUSDT", "ICPUSDT", "FILUSDT", "APTUSDT", "NEARUSDT"
]

def get_klines(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=15m&limit=30"
    response = requests.get(url)
    try:
        data = response.json()
    except Exception as e:
        print(f"{symbol} JSON decode error:", e)
        return []

    if not isinstance(data, list):
        print(f"{symbol} Unexpected response:", data)
        return []

    closes = [float(candle[4]) for candle in data]
    return closes

def moving_average(data, period):
    return np.convolve(data, np.ones(period)/period, mode='valid')

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def main():
    for symbol in SYMBOLS:
        closes = get_klines(symbol)
        if not closes:
            continue

        ma9 = moving_average(closes, 9)
        ma21 = moving_average(closes, 21)

        if len(ma9) < 2 or len(ma21) < 2:
            continue

        if ma9[-2] < ma21[-2] and ma9[-1] > ma21[-1]:
            send_telegram_message(f"{symbol} 📈 کراس صعودی")
        elif ma9[-2] > ma21[-2] and ma9[-1] < ma21[-1]:
            send_telegram_message(f"{symbol} 📉 کراس نزولی")

if __name__ == "__main__":
    main()
