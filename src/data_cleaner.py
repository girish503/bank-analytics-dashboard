# src/data_cleaner.py
# Purpose: Clean raw transaction data

import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataCleaner:

    def __init__(self, df):
        self.df     = df.copy()
        self.issues = []

    def _clean_amount(self, value):
        """Convert ₹1,50,000 or 50000 → float"""
        try:
            cleaned = float(
                str(value)
                .replace("₹", "")
                .replace(",", "")
                .strip()
            )
            return cleaned
        except ValueError:
            msg = f"Invalid amount value: {value}"
            logger.warning(f"⚠️ {msg}")
            self.issues.append(msg)
            return None

    def clean_all(self):
        logger.info("🧹 Starting data cleaning...")

        # Step 1 — Clean amount
        self.df["amount"] = self.df["amount"].apply(
            self._clean_amount
        )

        # Step 2 — Drop bad rows
        before = len(self.df)
        self.df.dropna(subset=["amount"], inplace=True)
        dropped = before - len(self.df)
        if dropped > 0:
            logger.warning(f"⚠️ Dropped {dropped} invalid rows!")

        # Step 3 — Fix date column
        self.df["date"] = pd.to_datetime(self.df["date"])

        # Step 4 — Clean text columns
        self.df["type"]          = self.df["type"].str.strip().str.title()
        self.df["status"]        = self.df["status"].str.strip().str.title()
        self.df["customer_name"] = self.df["customer_name"].str.strip()

        # Step 5 — Add helper columns
        self.df["month"] = self.df["date"].dt.strftime("%B %Y")
        self.df["day"]   = self.df["date"].dt.day_name()

        # Step 6 — Remove duplicates
        self.df.drop_duplicates(inplace=True)

        logger.info(
            f"✅ Cleaning done! "
            f"{len(self.df)} clean rows ready."
        )
        return self.df

    def quality_report(self):
        print(f"\n{'='*40}")
        print(f"DATA QUALITY REPORT")
        print(f"Clean Rows : {len(self.df)}")
        print(f"Issues Found: {len(self.issues)}")
        for issue in self.issues:
            print(f"  ⚠️  {issue}")
        print(f"{'='*40}\n")