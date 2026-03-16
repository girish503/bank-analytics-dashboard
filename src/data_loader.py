# src/data_loader.py
# Purpose: Read raw CSV file safely

import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

class DataLoader:

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        logger.info(f"Loading file: {self.filepath}")

        try:
            # Check file exists first
            if not os.path.exists(self.filepath):
                raise FileNotFoundError(
                    f"File not found: {self.filepath}"
                )

            df = pd.read_csv(self.filepath)

            # Check file is not empty
            if len(df) == 0:
                raise ValueError("CSV file is empty!")

            logger.info(
                f"✅ Loaded {len(df)} rows, "
                f"{len(df.columns)} columns"
            )
            return df

        except FileNotFoundError as e:
            logger.error(f"❌ {e}")
            raise

        except ValueError as e:
            logger.error(f"❌ {e}")
            raise

        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            raise