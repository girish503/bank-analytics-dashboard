# src/database_handler.py
# Purpose: All database operations

import sqlite3
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

class DatabaseHandler:

    def __init__(self, db_path="database/bank.db"):
        self.db_path = db_path
        os.makedirs("database", exist_ok=True)

    def create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id            INTEGER PRIMARY KEY,
                    customer_name TEXT    NOT NULL,
                    account_no    TEXT    NOT NULL,
                    type          TEXT    NOT NULL,
                    amount        REAL    NOT NULL,
                    date          TEXT    NOT NULL,
                    month         TEXT,
                    day           TEXT,
                    status        TEXT    NOT NULL
                )
            """)
        logger.info("✅ Database tables ready!")

    def load_dataframe(self, df):
        with sqlite3.connect(self.db_path) as conn:
            df.to_sql(
                "transactions",
                conn,
                if_exists="replace",
                index=False
            )
        logger.info(f"✅ {len(df)} rows loaded to database!")

    def query(self, sql):
        """Run any SQL → return DataFrame"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                return pd.read_sql_query(sql, conn)
        except Exception as e:
            logger.error(f"❌ Query failed: {e}")
            raise