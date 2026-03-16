# generate_data.py
# Purpose: Generate 500 realistic bank transactions
# Run once: python generate_data.py

import pandas as pd
import random
from datetime import datetime, timedelta
import os

CUSTOMERS = [
    ("Ravi Kumar",     "ACC001"),
    ("Priya Shah",     "ACC002"),
    ("Kiran Reddy",    "ACC003"),
    ("Sneha Mehta",    "ACC004"),
    ("Arjun Singh",    "ACC005"),
    ("Meena Nair",     "ACC006"),
    ("Rahul Verma",    "ACC007"),
    ("Deepa Rao",      "ACC008"),
    ("Suresh Iyer",    "ACC009"),
    ("Kavitha Pillai", "ACC010"),
    ("Arun Sharma",    "ACC011"),
    ("Pooja Patel",    "ACC012"),
    ("Vikram Menon",   "ACC013"),
    ("Anita Joshi",    "ACC014"),
    ("Rajesh Gupta",   "ACC015"),
]

CREDIT_RANGES = [
    (5000,   15000),
    (1000,   5000),
    (50000,  200000),
    (10000,  50000),
]

DEBIT_RANGES = [
    (500,    5000),
    (1000,   10000),
    (5000,   25000),
    (10000,  50000),
]

def random_amount(txn_type):
    if txn_type == "Credit":
        low, high = random.choice(CREDIT_RANGES)
    else:
        low, high = random.choice(DEBIT_RANGES)
    amount = random.randint(low, high)
    return round(amount / 500) * 500

def random_date(start, end):
    delta      = end - start
    rand_days  = random.randint(0, delta.days)
    return start + timedelta(days=rand_days)

def generate_status():
    return random.choices(
        ["Success", "Failed"],
        weights=[90, 10]
    )[0]

# ── Generate 500 rows ─────────────────────────
print("Generating 500 transactions...")

start_date = datetime(2025, 1, 1)
end_date   = datetime(2026, 3, 31)

rows = []
for i in range(1, 501):
    customer, account = random.choice(CUSTOMERS)
    txn_type = random.choice(["Credit", "Debit"])
    amount   = random_amount(txn_type)
    date     = random_date(start_date, end_date)
    status   = generate_status()

    rows.append({
        "id":            i,
        "customer_name": customer,
        "account_no":    account,
        "type":          txn_type,
        "amount":        amount,
        "date":          date.strftime("%Y-%m-%d"),
        "status":        status
    })

df = pd.DataFrame(rows)
df = df.sort_values("date").reset_index(drop=True)

# ── Add 2 dirty rows to test cleaning ─────────
dirty = pd.DataFrame([
    {
        "id": 501,
        "customer_name": "Test User",
        "account_no":    "ACC001",
        "type":          "Credit",
        "amount":        "ABC",
        "date":          "2026-01-15",
        "status":        "Success"
    },
    {
        "id": 502,
        "customer_name": "Test User 2",
        "account_no":    "ACC002",
        "type":          "Debit",
        "amount":        "XYZ",
        "date":          "2026-02-10",
        "status":        "Success"
    },
])

df = pd.concat([df, dirty], ignore_index=True)

# ── Save ──────────────────────────────────────
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/transactions.csv", index=False)

print(f"Done! {len(df)} rows saved!")
print(f"Credits : {len(df[df['type']=='Credit'])}")
print(f"Debits  : {len(df[df['type']=='Debit'])}")
print(f"Success : {len(df[df['status']=='Success'])}")
print(f"Failed  : {len(df[df['status']=='Failed'])}")
print("Now run: python pipeline.py")
