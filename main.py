import requests
import pandas as pd

BOT_TOKEN = '8092692270:AAE1AATHk0Qyg_okjktO2gShivQNFInfCLs'
CHAT_ID = '431116432'
TD_API_KEY = 'cbb117052e324d43bdd5172b796b45ea'

# لیست ارزهای مدنظر به صورت uppercase (فقط حروف بزرگ)
symbols_list = [
    "BTC", "IRT", "ETH", "S", "CATS", "MEMEFI", "MAJOR", "FDUSD", "PNUT", "HYPE", "TRUMP", "MELANIA",
    "POND", "USDT", "TON", "PAXG", "NOT", "HMSTR", "CATI", "WAT", "EIGEN", "DIA", "MOODENG", "IO",
    "XAUT", "GOAT", "GRASS", "ACT", "CLV", "BRETT", "VIRTUAL", "ATH", "XCN", "DEXE", "MOVE", "GT",
    "PENGU", "FARTCOIN", "MORPHO", "DEEP", "KAON", "HEI", "AI16Z", "BNB", "TAPS", "PIXFI", "DOGS",
    "RBTC", "SUNDOG", "CAT", "NEIROCTO", "TURBO", "X", "DRIFT", "ORCA", "LAYER", "FHE", "VINE",
    "ADA", "DYM", "STRK", "PAWS", "SOL", "KAVA", "PIXEL", "SPELL", "BOME", "ETHFI", "POPCAT", "XRP",
    "BCH", "JUP", "NMR", "OM", "BEAMX", "PORTAL", "STG", "RAY", "GTC", "LISTA", "DOT", "MAVIA",
    "WAXP", "AGI", "ZBU", "MEW", "ZETA", "CVC", "BONK", "MAGIC", "POWR", "ALT", "ONDO", "BADGER",
    "PHB", "DAO", "AERGO", "RSR", "GME", "T", "RLC", "WEN", "TOKEN", "W", "AEVO", "TNSR", "FARM",
    "PEPE2", "PERP", "TOMI", "EDU", "AI", "PENDLE", "RAD", "COQ", "SLERF", "ENA", "ZRO", "PONKE",
    "RENDER", "USDC", "YGG", "JTO", "ZRX", "TIA", "NFP", "PEIPEI", "MLN", "HIFI", "FXS", "UMA",
    "ACE", "ARPA", "XLM", "BABYDOGE", "TRB", "MEME", "SYN", "XAI", "LTC", "UNFI", "PYR", "XMR",
    "UNI", "LPT", "BLZ", "BIGTIME", "AUCTION", "MYRO", "WIF", "G", "EOS", "LINK", "CYBER", "FITFI",
    "CTC", "MUBI", "XEM", "WSM", "TRX", "STARL", "XTZ", "CRO", "JST", "THETA", "ARB", "ARKM", "WLD",
    "CFX", "RACA", "CXT", "COMBO", "VOLT", "HFT", "BONE", "JASMY", "VINU", "VET", "LQTY", "TAMA",
    "MILO", "GHST", "BLUR", "SSV", "MNT", "PYTH", "ATOM", "SUN", "FORM", "ACH", "DASH", "DOGE",
    "SPA", "GRT", "LDO", "GLMR", "RDNT", "STCHAIN", "FIL", "AAVE", "HTX", "TRVL", "BUSD", "WAVES",
    "ZEC", "YFI", "DAI", "GALA", "APE", "MDT", "ETC", "SHIB", "COMP", "NFT", "SUSHI", "MKR",
    "IOTA", "ONE", "MANA", "BOB", "BDEFI", "CELR", "B100", "CHZ", "EGLD", "RPL", "BGC", "TWT",
    "ZIL", "CRV", "B2", "POL", "CAKE", "ANKR", "WIN", "VIC", "KCS", "XEC", "CVX", "SUI", "GMT",
    "GMX", "SAND", "LUNA", "MIR", "1INCH", "AXS", "AVAX", "ALICE", "ENJ", "OP", "REEF", "TLM",
    "LRC", "HOT", "VTHO", "KISHU", "FEG", "ALGO", "FORTH", "QNT", "IOTX", "LINA", "DODO", "CTK",
    "DENT", "CHR", "BEL", "C98", "BAND", "INJ", "XVS", "SXP", "ONT", "BAT", "SNX", "NEAR",
    "SKL", "SEI", "SLF", "MASK", "DYDX", "COTI", "FET", "SLP", "CELO", "FTT", "BNT", "KSM",
    "AUDIO", "ENS", "SRM", "ELON", "STORJ", "IMX", "PEPE", "AIDOGE", "SHIBAI", "EPX", "LUNC",
    "GLM", "HT", "AMP", "ID", "MDX", "PEOPLE", "KNC", "POLS", "BAKE", "SFM", "BTTC", "METIS",
    "API3", "BLOK", "MBOX", "REN", "NKN", "VRA", "MOVR", "BETA", "IDEX", "RLY", "AMPL", "QI",
    "PORTO", "JOE", "PSG", "OOKI", "LAZIO", "CGPT", "ARV", "ATM", "JUV", "ASR", "DC", "FLOKI"
]

def get_ohlcv_from_twelvedata(symbol):
    symbol_td = f"{symbol}/USD"
    url = "https://api.twelvedata.com/time_series"
    params = {
        'symbol': symbol_td,
        'interval': '1h',
        'outputsize': 50,
        'apikey': TD_API_KEY
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if 'values' not in data:
            return None
        df = pd.DataFrame(data['values'])
        df['close'] = df['close'].astype(float)
        df = df.sort_values('datetime')
        return df
    except Exception as e:
        # اگر خطایی بود نادیده می‌گیریم
        return None

def analyze_ma_cross(df):
    df['ma9'] = df['close'].rolling(window=9).mean()
    df['ma21'] = df['close'].rolling(window=21).mean()

    if len(df) < 22:  # حداقل 22 کندل باید باشه
        return "⏸ بدون سیگنال"

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
    try:
        requests.post(url, data={'chat_id': CHAT_ID, 'text': text})
    except:
        pass

def main():
    signals_found = []

    for symbol in symbols_list:
        df = get_ohlcv_from_twelvedata(symbol)
        if df is not None:
            signal = analyze_ma_cross(df)
            if signal != "⏸ بدون سیگنال":
                signals_found.append(f"{symbol}/USD ➜ {signal}")

    if signals_found:
        summary = "📊 سیگنال‌های MA کراس:\n\n" + "\n".join(signals_found)
    else:
        summary = "❌ هیچ سیگنالی وجود ندارد."

    send_to_telegram(summary)

if __name__ == "__main__":
    main()
