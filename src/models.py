# src/models.py
# Purpose: Blueprint classes for bank entities

class Transaction:
    """Represents one bank transaction"""

    def __init__(self, id, customer_name, account_no,
                 type, amount, date, status):
        self.id            = id
        self.customer_name = customer_name
        self.account_no    = account_no
        self.type          = type
        self.amount        = amount
        self.date          = date
        self.status        = status

    def is_large(self):
        return self.amount > 100000

    def display(self):
        print(f"{self.customer_name} | "
              f"{self.type} | "
              f"₹{self.amount:,} | "
              f"{self.status}")


class BankAccount:
    """Represents a customer bank account"""

    total_accounts = 0

    def __init__(self, account_no, customer_name):
        self.account_no    = account_no
        self.customer_name = customer_name
        self.transactions  = []
        BankAccount.total_accounts += 1

    def add_transaction(self, txn):
        self.transactions.append(txn)

    def get_balance(self):
        balance = 0
        for t in self.transactions:
            if t.type == "Credit":
                balance += t.amount
            else:
                balance -= t.amount
        return balance

    def summary(self):
        print(f"\n{'='*40}")
        print(f"Account  : {self.account_no}")
        print(f"Customer : {self.customer_name}")
        print(f"Balance  : ₹{self.get_balance():,.2f}")
        print(f"Txn Count: {len(self.transactions)}")
        print(f"{'='*40}")