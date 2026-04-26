import schedule
import time
from ingestion.fetch import fetch_crypto_data
from processing.clean import clean_crypto_data
from storage.db import create_table, save_to_db
from logger import logger

def run_pipeline():
    logger.info("Pipeline started.")

    raw = fetch_crypto_data()
    if raw is None:
        logger.error("Data fetch failed. Skipping this run.")
        return

    logger.info(f"Fetched {len(raw)} records.")

    cleaned = clean_crypto_data(raw)
    logger.info("Data cleaning complete.")

    save_to_db(cleaned)
    logger.info(f"Saved {len(cleaned)} rows to database.")

    anomalies = cleaned[cleaned["is_anomaly"] == True]
    if not anomalies.empty:
        logger.warning(f"{len(anomalies)} anomalies detected:")
        for _, row in anomalies.iterrows():
            logger.warning(f"  {row['id']} | price: ${row['current_price']} | 24h change: {row['price_change_percentage_24h']}%")
    else:
        logger.info("No anomalies detected.")

    logger.info("Pipeline finished.\n")

if __name__ == "__main__":
    create_table()
    run_pipeline()

    schedule.every(5).minutes.do(run_pipeline)
    logger.info("Scheduler started. Running every 5 minutes.")

    while True:
        schedule.run_pending()
        time.sleep(1)