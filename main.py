import requests

def get_bitpin_tickers():
    url = "https://api.bitpin.ir/v1/market/tickers"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"خطا در دریافت اطلاعات از بیت‌پین: {e}")
        return None

    # داده ها معمولا در کلید 'tickers' هستند، بسته به ساختار JSON می‌تونی چک کنی
    if 'tickers' not in data:
        print("کلید 'tickers' در پاسخ موجود نیست.")
        return None

    tickers = data['tickers']
    for ticker in tickers:
        symbol = ticker.get('symbol', 'N/A')
        last_price = ticker.get('last', 'N/A')
        print(f"{symbol}: {last_price}")

if __name__ == "__main__":
    get_bitpin_tickers()
