import pandas as pd
import numpy as np

def clean_crypto_data(df):

    # drop rows where critical fields are missing
    df = df.dropna(subset=["current_price", "total_volume", "market_cap"])

    # reset index cleanly
    df = df.reset_index(drop=True)

    # enforce correct data types
    df["current_price"] = pd.to_numeric(df["current_price"], errors="coerce")
    df["market_cap"] = pd.to_numeric(df["market_cap"], errors="coerce")
    df["total_volume"] = pd.to_numeric(df["total_volume"], errors="coerce")
    df["price_change_percentage_24h"] = pd.to_numeric(df["price_change_percentage_24h"], errors="coerce")

    # round to keep things clean
    df["current_price"] = df["current_price"].round(4)
    df["price_change_percentage_24h"] = df["price_change_percentage_24h"].round(2)

    # flag coins with abnormal 24h price change
    # anything beyond 2 standard deviations is flagged
    mean = df["price_change_percentage_24h"].mean()
    std = df["price_change_percentage_24h"].std()
    df["is_anomaly"] = np.where(
        (df["price_change_percentage_24h"] > mean + 2 * std) |
        (df["price_change_percentage_24h"] < mean - 2 * std),
        True, False
    )

    # add a simple price momentum label
    df["momentum"] = pd.cut(
        df["price_change_percentage_24h"],
        bins=[-np.inf, -5, -2, 2, 5, np.inf],
        labels=["strong_down", "down", "stable", "up", "strong_up"]
    )

    return df

if __name__ == "__main__":
    from ingestion.fetch import fetch_crypto_data
    raw = fetch_crypto_data()
    cleaned = clean_crypto_data(raw)
    print(cleaned)
    print("\nAnomalies flagged:")
    print(cleaned[cleaned["is_anomaly"] == True][["id", "current_price", "price_change_percentage_24h"]])