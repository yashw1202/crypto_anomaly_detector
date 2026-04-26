import sqlalchemy as sa
import pandas as pd

DB_URL = "sqlite:///crypto.db"

engine = sa.create_engine(DB_URL)

def create_table():
    with engine.connect() as conn:
        conn.execute(sa.text("""
            CREATE TABLE IF NOT EXISTS crypto_data (
                id TEXT,
                symbol TEXT,
                current_price REAL,
                market_cap REAL,
                total_volume REAL,
                price_change_percentage_24h REAL,
                high_24h REAL,
                low_24h REAL,
                fetched_at TEXT,
                is_anomaly INTEGER,
                momentum TEXT
            )
        """))
        conn.commit()

def save_to_db(df):
    df["is_anomaly"] = df["is_anomaly"].astype(int)
    df["momentum"] = df["momentum"].astype(str)
    df.to_sql("crypto_data", con=engine, if_exists="append", index=False)
    print(f"Saved {len(df)} rows to database.")

def read_from_db():
    return pd.read_sql("SELECT * FROM crypto_data", con=engine)

if __name__ == "__main__":
    from ingestion.fetch import fetch_crypto_data
    from processing.clean import clean_crypto_data

    create_table()
    raw = fetch_crypto_data()
    cleaned = clean_crypto_data(raw)
    save_to_db(cleaned)

    print("\nData in DB:")
    print(read_from_db())