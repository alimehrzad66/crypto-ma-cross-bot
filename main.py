import requests
import numpy as np

TOKEN = "8092692270:AAE1AATHk0Qyg_okjktO2gShivQNFInfCLs"
CHAT_ID = "431116432"

SYMBOL = "BTCUSDT"

def get_klines():
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval=1h&limit=30"
    response = requests.get(url)
    try:
        data = response.json()
    except Exception as e:
        print("JSON decode error:", e)
        return []

    if not isinstance(data, list):
        print("Unexpected response:", data)
        return []

    closes = [float(candle[4]) for candle in data]
    return closes

def moving_average(data, period):
    return np.convolve(data, np.ones(period)/period, mode='valid')

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def main():
    closes = get_klines()
    if not closes:
        print("No close data available.")
        return

    ma9 = moving_average(closes, 9)
    ma21 = moving_average(closes, 21)
    
    if len(ma9) < 2 or len(ma21) < 2:
        return
    
    if ma9[-2] < ma21[-2] and ma9[-1] > ma21[-1]:
        send_telegram_message("کراس صعودی رخ داد!")
    elif ma9[-2] > ma21[-2] and ma9[-1] < ma21[-1]:
        send_telegram_message("کراس نزولی رخ داد!")

if __name__ == "__main__":
    main()
