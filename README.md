# Crypto Market Data Pipeline

A production-style data pipeline that ingests live cryptocurrency market data,
cleans and processes it, detects anomalies, and stores it in a local database
running automatically on a schedule.

## What it does

- Fetches live price data for 5 major cryptocurrencies every 5 minutes via CoinGecko API.
- Cleans and validates the data, handles missing values, type errors and nulls.
- Detects anomalies using Z-score statistical analysis on 24h price changes.
- Labels price momentum ie. strong_up, up, stable, down and strong_down.
- Stores all data in a local SQLite database with full history.
- Logs every pipeline run to a daily log file

## Tech Stack

- Python
- Pandas & Numpy —> data processing and anomaly detection
- SQLAlchemy —> database ORM
- SQLite —> local database storage
- Schedule —> pipeline orchestration
- CoinGecko API —> live market data source

## Project Structure

crypto_pipeline/
│
├── ingestion/ # data fetching from API
├── processing/ # cleaning and anomaly detection
├── storage/ # database setup and writes
├── logs/ # daily pipeline logs
├── logger.py # logging config
├── main.py # pipeline entry point
└── requirements.txt

## How to run

```bash
# clone the repo
git clone https://github.com/yourusername/crypto_pipeline.git
cd crypto_pipeline

# create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run the pipeline
python main.py
```

## Sample output

2026-04-26 10:00:01 | INFO | Pipeline started.

2026-04-26 10:00:02 | INFO | Fetched 5 records.

2026-04-26 10:00:02 | INFO | Data cleaning complete.

2026-04-26 10:00:02 | INFO | Saved 5 rows to database.

2026-04-26 10:00:02 | WARNING | 1 anomalies detected:

2026-04-26 10:00:02 | WARNING | solana | price: $142.3 | 24h change: -8.5%

2026-04-26 10:00:02 | INFO | Pipeline finished.

## What I learned

- Building an end-to-end ETL pipeline from scratch.
- Statistical anomaly detection using Z-score analysis.
- Database design and storage with SQLAlchemy.
- Pipeline scheduling and production logging.
- Clean project structure for data engineering.

## Contributing

Contributions are welcome! Here are some ideas to get started:

- Add more coins beyond the current 5
- Add email or Telegram alerts when anomalies are detected
- Migrate from SQLite to PostgreSQL
- Add a Kafka streaming layer for real time ingestion
- Write unit tests for the cleaning and anomaly detection logic
- Add a Dockerfile for containerized deployment

### How to contribute

1. Fork the repo
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit (`git commit -m "add: your feature description"`)
5. Push (`git push origin feature/your-feature-name`)
6. Open a Pull Request

Feel free to open an issue first if you want to discuss an idea before building it.