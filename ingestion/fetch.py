import requests
import pandas as pd
from datetime import datetime

COINS = ["bitcoin", "ethereum", "solana", "binancecoin", "ripple"]

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ",".join(COINS),
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"API error: {response.status_code}")
        return None

    data = response.json()

    df = pd.DataFrame(data)

    df = df[[
        "id", "symbol", "current_price",
        "market_cap", "total_volume",
        "price_change_percentage_24h",
        "high_24h", "low_24h"
    ]]

    df["fetched_at"] = datetime.utcnow()

    return df

if __name__ == "__main__":
    df = fetch_crypto_data()
    print(df)