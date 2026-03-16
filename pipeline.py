# pipeline.py
# Purpose: Master runner — runs entire pipeline!
# Run this first before dashboard!

import logging
import os

# Setup logging FIRST before any imports
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Now import project modules
from src.data_loader      import DataLoader
from src.data_cleaner     import DataCleaner
from src.database_handler import DatabaseHandler

def run_pipeline():

    print("\n🚀 Starting Bank Analytics Pipeline...\n")
    logging.info("="*50)
    logging.info("PIPELINE STARTED")

    # ── Step 1: Load Raw Data ──────────────────
    print("Step 1/3 → Loading raw data...")
    loader = DataLoader("data/raw/transactions.csv")
    df_raw = loader.load()
    print(f"         ✅ {len(df_raw)} rows loaded!\n")

    # ── Step 2: Clean Data ─────────────────────
    print("Step 2/3 → Cleaning data...")
    cleaner  = DataCleaner(df_raw)
    df_clean = cleaner.clean_all()
    cleaner.quality_report()
    print(f"         ✅ {len(df_clean)} clean rows ready!\n")

    # ── Step 3: Load to Database ───────────────
    print("Step 3/3 → Loading to database...")
    db = DatabaseHandler()
    db.create_tables()
    db.load_dataframe(df_clean)
    print("         ✅ Database ready!\n")

    print("="*50)
    print("✅ Pipeline Complete!")
    print("Now run → streamlit run app.py")
    print("="*50)
    logging.info("PIPELINE COMPLETE!")

if __name__ == "__main__":
    run_pipeline()