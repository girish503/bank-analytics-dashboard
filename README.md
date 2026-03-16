# 🏦 BankIQ Analytics — Enterprise Banking Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A production-ready banking analytics dashboard built with Python, SQL and Streamlit.**
Simulates real-world fintech systems used by banks like HDFC, ICICI, and Axis.

[🚀 Live Demo](https://bank-analytics-dashboard-y7okv5mbc5vpquoy5aol5n.streamlit.app/) • [📖 Documentation](#documentation) • [🐛 Report Bug](https://github.com/girish503/bank-analytics-dashboard/issues) • [✨ Request Feature](https://github.com/girish503/bank-analytics-dashboard/issues)

</div>

---

## 📸 Screenshots

| Overview | Customer Analysis |
|---|---|
| ![Overview](https://via.placeholder.com/400x250/0a0e1a/00d4aa?text=Executive+Overview) | ![Customers](https://via.placeholder.com/400x250/0a0e1a/4b8bff?text=Customer+Analysis) |

| Fraud Detection | Account Monitor |
|---|---|
| ![Fraud](https://via.placeholder.com/400x250/0a0e1a/ff4b4b?text=Fraud+Detection) | ![Account](https://via.placeholder.com/400x250/0a0e1a/ffd700?text=Account+Monitor) |

---

## 🎯 About The Project

BankIQ Analytics is an end-to-end banking data analytics system that demonstrates how financial institutions monitor, analyze, and act on transaction data in real time.

This project covers the **complete data lifecycle**:
- Raw CSV ingestion → Automated cleaning → SQLite storage → SQL analysis → Interactive dashboard

Built as a portfolio project to demonstrate **Python OOP, advanced SQL, data visualization**, and **Streamlit deployment** skills in a real-world banking context.

---

## ✨ Features

### 📊 8 Interactive Dashboard Pages
| Page | Description |
|---|---|
| 🏠 **Overview** | Executive KPIs, monthly trends, heatmap, amount distribution |
| 👥 **Customers** | Segmentation (Platinum/Gold/Silver/Basic), intelligence map |
| 💳 **Transactions** | Full transaction table with live filters |
| ⚠️ **Risk Center** | Suspicious transaction alerts, failed transaction monitor |
| 📈 **Growth Analysis** | Month over month revenue trends like SBI quarterly reports |
| 🔍 **Fraud Detection** | Multi-signal fraud scoring like ICICI fraud team |
| 🏛️ **Account Monitor** | Running balance tracker, dormant account detection |
| 📋 **Reports** | Cashflow analysis, account health scores, velocity monitoring |

### 🔥 Key Technical Highlights
- **Automated Data Pipeline** — raw CSV → clean data → SQLite in 3 steps
- **Advanced SQL** — CTEs, Window Functions (ROW_NUMBER, RANK, LAG, NTILE), Subqueries, CASE WHEN
- **Fraud Detection** — multi-signal risk scoring across 4 risk categories
- **Customer Segmentation** — NTILE-based Platinum/Gold/Silver/Basic classification
- **Running Balance** — per-account passbook-style balance history
- **Dormant Detection** — accounts flagged by last activity date
- **Data Quality Reporting** — dirty data detection and cleaning audit trail

---

## 🏗️ Project Architecture

```
bank_analytics/
│
├── 📁 data/
│   ├── raw/
│   │   └── transactions.csv        ← raw input (502 rows with dirty data)
│   └── cleaned/
│
├── 📁 database/
│   └── bank.db                     ← SQLite database
│
├── 📁 src/                         ← core Python modules
│   ├── __init__.py
│   ├── models.py                   ← OOP: Transaction & BankAccount classes
│   ├── data_loader.py              ← file handling with exception management
│   ├── data_cleaner.py             ← data cleaning pipeline
│   ├── database_handler.py         ← SQLite operations
│   ├── analyzer.py                 ← 15+ SQL business queries
│   └── charts.py                   ← Matplotlib & Seaborn visualizations
│
├── 📁 logs/
│   └── pipeline.log                ← full pipeline audit trail
│
├── app.py                          ← Streamlit dashboard (8 pages)
├── pipeline.py                     ← master data pipeline runner
├── generate_data.py                ← realistic data generator (500 rows)
├── runtime.txt                     ← Python 3.11 for deployment
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11 | Core application |
| **Data Processing** | Pandas, NumPy | Data manipulation |
| **Database** | SQLite | Data storage |
| **Query Language** | SQL | Business analytics |
| **Visualization** | Matplotlib, Seaborn | Charts & heatmaps |
| **Dashboard** | Streamlit | Interactive web UI |
| **Architecture** | OOP + Modules | Clean code structure |
| **Logging** | Python logging | Pipeline audit trail |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.11+ installed.

```bash
python --version
# Python 3.11.x
```

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/girish503/bank-analytics-dashboard.git
cd bank-analytics-dashboard
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Generate sample data**
```bash
python generate_data.py
```

**4. Run the data pipeline**
```bash
python pipeline.py
```

**5. Launch the dashboard**
```bash
streamlit run app.py
```

**6. Open in browser**
```
http://localhost:8501
```

---

## 📊 SQL Concepts Demonstrated

This project demonstrates **production-level SQL** across all major concepts:

```sql
-- Window Functions (ROW_NUMBER, RANK, DENSE_RANK, LAG, NTILE)
ROW_NUMBER() OVER(PARTITION BY month ORDER BY SUM(amount) DESC)

-- CTEs (Common Table Expressions)
WITH customer_stats AS (
    SELECT customer_name, SUM(amount) AS total_volume
    FROM transactions GROUP BY customer_name
)

-- Subqueries for fraud detection
WHERE amount > (SELECT AVG(amount) * 3 FROM transactions)

-- CASE WHEN for categorization
CASE WHEN health_score >= 80 THEN '🟢 Excellent'
     WHEN health_score >= 60 THEN '🟡 Good'
     ELSE '🔴 Poor' END AS health_status

-- Running balance using SUM OVER
SUM(CASE WHEN type='Credit' THEN amount ELSE -amount END)
OVER(PARTITION BY account_no ORDER BY date)
```

---

## 🐍 Python Concepts Demonstrated

| Concept | Where Used |
|---|---|
| **OOP — Classes & Objects** | `models.py` — Transaction, BankAccount |
| **File Handling** | `data_loader.py` — CSV reading |
| **Exception Handling** | `data_cleaner.py` — dirty data management |
| **Modules & Imports** | All files — clean modular architecture |
| **List Comprehension** | `data_cleaner.py` — data transformation |
| **Logging** | `pipeline.py` — full audit trail |
| **Generators** | Large file processing |
| **Lambda Functions** | Chart formatters, data sorting |
| **Context Managers** | Database connections (`with` statement) |

---

## 🤝 Contributing

Contributions are what make the open source community amazing! Any contributions you make are **greatly appreciated**.

### How to Contribute

**1. Fork the project**
```bash
# Click "Fork" button on GitHub
```

**2. Create your feature branch**
```bash
git checkout -b feature/AmazingFeature
```

**3. Make your changes**
```bash
# Edit files, add features, fix bugs
```

**4. Run tests manually**
```bash
python pipeline.py
streamlit run app.py
# Verify all 8 pages load correctly!
```

**5. Commit your changes**
```bash
git add .
git commit -m "feat: Add AmazingFeature"
```

**6. Push to the branch**
```bash
git push origin feature/AmazingFeature
```

**7. Open a Pull Request**
```
Go to GitHub → Pull Requests → New Pull Request
Describe what you changed and why!
```

---

### 💡 Ideas for Contributions

Here are some great ways to contribute:

| Area | Ideas |
|---|---|
| 🔍 **New SQL Queries** | Add quarterly summaries, cohort analysis, product-wise breakdown |
| 📊 **New Charts** | Add candlestick charts, treemaps, network graphs |
| 🧹 **Data Quality** | Improve cleaning pipeline, add more validation rules |
| 🔐 **Security** | Add login system, role-based access |
| 📤 **Export** | Add PDF report generation, Excel export |
| 🗄️ **Database** | Migrate from SQLite to PostgreSQL |
| 🧪 **Testing** | Add unit tests with pytest |
| 🌍 **Deployment** | Docker containerization, CI/CD pipeline |

---

### 📝 Commit Message Convention

Please follow this convention for commit messages:

```
feat:     Add new feature
fix:      Fix a bug
docs:     Update documentation
style:    Formatting changes
refactor: Code restructuring
test:     Add or update tests
chore:    Maintenance tasks
```

Examples:
```bash
git commit -m "feat: Add quarterly revenue comparison chart"
git commit -m "fix: Fix month sorting in cashflow analysis"
git commit -m "docs: Update installation instructions"
```

---

## 🐛 Reporting Bugs

Found a bug? Please open an issue with:

1. **Description** — what happened vs what you expected
2. **Steps to reproduce** — exact steps to recreate the bug
3. **Screenshots** — if applicable
4. **Environment** — OS, Python version, browser

[Open an Issue →](https://github.com/girish503/bank-analytics-dashboard/issues)

---

## 📈 Roadmap

- [x] Core data pipeline (load → clean → store)
- [x] 8-page Streamlit dashboard
- [x] Advanced SQL analytics (CTEs, Window Functions)
- [x] Fraud detection system
- [x] Customer segmentation
- [x] Streamlit Cloud deployment
- [ ] PostgreSQL migration
- [ ] User authentication system
- [ ] PDF report generation
- [ ] REST API with Flask
- [ ] Docker containerization
- [ ] Unit tests with pytest
- [ ] CI/CD with GitHub Actions

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Author

**Girish Adusumalli**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/girish503)

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io) — for making dashboard deployment incredibly simple
- [Pandas](https://pandas.pydata.org) — for powerful data manipulation
- [Seaborn](https://seaborn.pydata.org) — for beautiful statistical visualizations
- [SQLite](https://sqlite.org) — for lightweight embedded database
- Inspired by real banking systems at HDFC, ICICI, SBI, and Axis Bank

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

Made with ❤️ by Girish Adusumalli

</div>
