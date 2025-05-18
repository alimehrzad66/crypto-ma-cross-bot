import requests
import pandas as pd

# کلیدها به صورت ثابت اینجا تعریف شدند
BOT_TOKEN = '8092692270:AAE1AATHk0Qyg_okjktO2gShivQNFInfCLs'
CHAT_ID = '431116432'
TD_API_KEY = 'cbb117052e324d43bdd5172b796b45ea'

def get_top_gainers_from_coingecko(threshold=5):
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 250,
        'page': 1,
        'price_change_percentage': '24h'
    }
    r = requests.get(url, params=params)
    data = r.json()
    gainers = []
    for coin in data:
        change = coin.get('price_change_percentage_24h', 0)
        if change and change >= threshold:
            symbol = coin['symbol'].upper()
            gainers.append(symbol)
    return gainers

def get_ohlcv_from_twelvedata(symbol):
    symbol_td = f"{symbol}/USD"
    url = f"https://api.twelvedata.com/time_series"
    params = {
        'symbol': symbol_td,
        'interval': '1h',
        'outputsize': 50,
        'apikey': TD_API_KEY
    }
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        if 'values' not in data:
            return None
        df = pd.DataFrame(data['values'])
        df['close'] = df['close'].astype(float)
        df = df.sort_values('datetime')
        return df
    except:
        return None

def analyze_ma_cross(df):
    df['ma9'] = df['close'].rolling(window=9).mean()
    df['ma21'] = df['close'].rolling(window=21).mean()

    last_ma9 = df['ma9'].iloc[-1]
    prev_ma9 = df['ma9'].iloc[-2]
    last_ma21 = df['ma21'].iloc[-1]
    prev_ma21 = df['ma21'].iloc[-2]

    if prev_ma9 < prev_ma21 and last_ma9 > last_ma21:
        return "📈 سیگنال خرید"
    elif prev_ma9 > prev_ma21 and last_ma9 < last_ma21:
        return "📉 سیگنال فروش"
    else:
        return "⏸ بدون سیگنال"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})

def main():
    gainers = get_top_gainers_from_coingecko()

    if not gainers:
        send_to_telegram("هیچ ارزی با رشد بالای ۵٪ یافت نشد.")
        return

    signals_found = []

    for symbol in gainers:
        df = get_ohlcv_from_twelvedata(symbol)
        if df is not None and len(df) >= 21:
            signal = analyze_ma_cross(df)
            if signal != "⏸ بدون سیگنال":
                signals_found.append(f"{symbol}/USD ➜ {signal}")

    if signals_found:
        summary = "📊 سیگنال‌های MA کراس روی ارزهای با رشد >۵٪:\n\n"
        summary += "\n".join(signals_found)
    else:
        summary = "❌ هیچ سیگنالی وجود ندارد."

    send_to_telegram(summary)

if __name__ == "__main__":
    main()
