# src/analyzer.py
# Purpose: All business analysis — Professional Level!

from src.database_handler import DatabaseHandler
import logging

logger = logging.getLogger(__name__)


class BankAnalyzer:

    def __init__(self):
        self.db = DatabaseHandler()

    # ════════════════════════════════════════
    # EXISTING QUERIES
    # ════════════════════════════════════════

    def monthly_summary(self):
        return self.db.query("""
            SELECT
                month,
                COUNT(*)                AS total_transactions,
                ROUND(SUM(amount), 2)   AS total_volume,
                ROUND(AVG(amount), 2)   AS avg_amount,
                SUM(CASE WHEN type = 'Credit'
                    THEN amount ELSE 0 END) AS total_credits,
                SUM(CASE WHEN type = 'Debit'
                    THEN amount ELSE 0 END) AS total_debits
            FROM transactions
            WHERE status = 'Success'
            GROUP BY month
            ORDER BY MIN(date)
        """)

    def top_customers(self, n=10):
        return self.db.query(f"""
            WITH customer_stats AS (
                SELECT
                    customer_name,
                    COUNT(*)              AS total_txns,
                    ROUND(SUM(amount), 2) AS total_volume,
                    ROUND(AVG(amount), 2) AS avg_txn
                FROM transactions
                WHERE status = 'Success'
                GROUP BY customer_name
            )
            SELECT *,
                RANK() OVER(
                    ORDER BY total_volume DESC
                ) AS rank
            FROM customer_stats
            LIMIT {n}
        """)

    def failed_transactions(self):
        return self.db.query("""
            SELECT
                customer_name,
                account_no,
                type,
                amount,
                date,
                month
            FROM transactions
            WHERE status = 'Failed'
            ORDER BY amount DESC
        """)

    def suspicious_transactions(self):
        return self.db.query("""
            SELECT
                customer_name,
                account_no,
                type,
                amount,
                date
            FROM transactions
            WHERE amount > (
                SELECT AVG(amount) * 3
                FROM transactions
                WHERE status = 'Success'
            )
            ORDER BY amount DESC
        """)

    def daily_trend(self):
        return self.db.query("""
            SELECT
                day,
                COUNT(*)              AS total_txns,
                ROUND(SUM(amount), 2) AS total_volume
            FROM transactions
            WHERE status = 'Success'
            GROUP BY day
            ORDER BY total_volume DESC
        """)

    def account_summary(self):
        return self.db.query("""
            SELECT
                account_no,
                customer_name,
                SUM(CASE WHEN type='Credit'
                    THEN amount ELSE 0 END) AS total_credited,
                SUM(CASE WHEN type='Debit'
                    THEN amount ELSE 0 END) AS total_debited,
                SUM(CASE WHEN type='Credit'
                    THEN amount ELSE -amount END) AS net_balance
            FROM transactions
            WHERE status = 'Success'
            GROUP BY account_no, customer_name
            ORDER BY net_balance DESC
        """)

    def cashflow_analysis(self):
        return self.db.query("""
            SELECT
                month,
                SUM(CASE WHEN type = 'Credit'
                    THEN amount ELSE 0 END) AS credits,
                SUM(CASE WHEN type = 'Debit'
                    THEN amount ELSE 0 END) AS debits,
                SUM(CASE WHEN type = 'Credit'
                    THEN amount ELSE 0 END) -
                SUM(CASE WHEN type = 'Debit'
                    THEN amount ELSE 0 END) AS net_cashflow,
                CASE
                    WHEN SUM(CASE WHEN type = 'Credit'
                        THEN amount ELSE 0 END) >
                         SUM(CASE WHEN type = 'Debit'
                        THEN amount ELSE 0 END)
                        THEN '🟢 Positive'
                    ELSE '🔴 Negative'
                END AS cashflow_status
            FROM transactions
            WHERE status = 'Success'
            GROUP BY month
            ORDER BY MIN(date)
        """)

    def account_health_score(self):
        return self.db.query("""
            WITH account_stats AS (
                SELECT
                    account_no,
                    customer_name,
                    COUNT(*)   AS txn_count,
                    SUM(CASE WHEN type = 'Credit'
                        THEN amount ELSE 0 END) AS credits,
                    SUM(CASE WHEN type = 'Debit'
                        THEN amount ELSE 0 END) AS debits,
                    SUM(CASE WHEN status = 'Failed'
                        THEN 1 ELSE 0 END) AS failed_count
                FROM transactions
                GROUP BY account_no, customer_name
            ),
            scored AS (
                SELECT *,
                    CASE
                        WHEN credits > debits * 1.5 THEN 40
                        WHEN credits > debits       THEN 30
                        WHEN credits = debits       THEN 20
                        ELSE 10
                    END AS credit_score,
                    CASE
                        WHEN failed_count = 0  THEN 30
                        WHEN failed_count = 1  THEN 20
                        WHEN failed_count <= 3 THEN 10
                        ELSE 0
                    END AS reliability_score,
                    CASE
                        WHEN txn_count >= 10 THEN 30
                        WHEN txn_count >= 5  THEN 20
                        WHEN txn_count >= 1  THEN 10
                        ELSE 0
                    END AS activity_score
                FROM account_stats
            )
            SELECT
                account_no,
                customer_name,
                credits       AS total_credits,
                debits        AS total_debits,
                failed_count,
                txn_count,
                credit_score + reliability_score
                    + activity_score AS health_score,
                CASE
                    WHEN credit_score + reliability_score
                        + activity_score >= 80
                        THEN '🟢 Excellent'
                    WHEN credit_score + reliability_score
                        + activity_score >= 60
                        THEN '🟡 Good'
                    WHEN credit_score + reliability_score
                        + activity_score >= 40
                        THEN '🟠 Average'
                    ELSE '🔴 Poor'
                END AS health_status
            FROM scored
            ORDER BY health_score DESC
        """)

    def transaction_velocity(self):
        return self.db.query("""
            SELECT
                account_no,
                customer_name,
                COUNT(*)              AS txn_count,
                ROUND(SUM(amount), 2) AS total_amount,
                ROUND(MAX(amount), 2) AS largest_txn,
                ROUND(MIN(amount), 2) AS smallest_txn,
                ROUND(AVG(amount), 2) AS avg_txn,
                CASE
                    WHEN COUNT(*) >= 5
                        AND AVG(amount) > (
                            SELECT AVG(amount) * 2
                            FROM transactions
                        )
                        THEN '🚨 High Risk'
                    WHEN COUNT(*) >= 3
                        THEN '⚠️ Monitor'
                    ELSE '✅ Normal'
                END AS velocity_flag
            FROM transactions
            WHERE status = 'Success'
            GROUP BY account_no, customer_name
            ORDER BY txn_count DESC
        """)

    # ════════════════════════════════════════
    # NEW ADVANCED QUERIES
    # ════════════════════════════════════════

    def month_over_month_growth(self):
        """
        Month over month growth using LAG!
        Fixed — consistent ORDER BY MIN(date)!
        """
        return self.db.query("""
            WITH monthly_revenue AS (
                SELECT
                    month,
                    MIN(date)             AS first_date,
                    ROUND(SUM(amount), 2) AS revenue
                FROM transactions
                WHERE status = 'Success'
                  AND type   = 'Credit'
                GROUP BY month
            )
            SELECT
                month,
                revenue,
                LAG(revenue) OVER(
                    ORDER BY first_date
                ) AS prev_month_revenue,
                ROUND(
                    revenue - LAG(revenue)
                    OVER(ORDER BY first_date),
                2) AS growth_amount,
                CASE
                    WHEN LAG(revenue)
                        OVER(ORDER BY first_date)
                        IS NULL
                        THEN 'First Month'
                    WHEN revenue > LAG(revenue)
                        OVER(ORDER BY first_date)
                        THEN '📈 Growth'
                    WHEN revenue < LAG(revenue)
                        OVER(ORDER BY first_date)
                        THEN '📉 Decline'
                    ELSE '➡️ Stable'
                END AS trend
            FROM monthly_revenue
            ORDER BY first_date
        """)

    def customer_segmentation(self):
        """
        Segment customers — Platinum/Gold/Silver/Basic
        """
        return self.db.query("""
            WITH customer_volume AS (
                SELECT
                    customer_name,
                    account_no,
                    COUNT(*)              AS total_txns,
                    ROUND(SUM(amount), 2) AS total_volume,
                    ROUND(AVG(amount), 2) AS avg_txn,
                    SUM(CASE WHEN status = 'Failed'
                        THEN 1 ELSE 0 END) AS failed_txns
                FROM transactions
                GROUP BY customer_name, account_no
            ),
            ranked AS (
                SELECT *,
                    NTILE(4) OVER(
                        ORDER BY total_volume DESC
                    ) AS quartile
                FROM customer_volume
            )
            SELECT
                customer_name,
                account_no,
                total_txns,
                total_volume,
                avg_txn,
                failed_txns,
                CASE quartile
                    WHEN 1 THEN '💎 Platinum'
                    WHEN 2 THEN '🥇 Gold'
                    WHEN 3 THEN '🥈 Silver'
                    WHEN 4 THEN '🥉 Basic'
                END AS segment,
                RANK() OVER(
                    ORDER BY total_volume DESC
                ) AS overall_rank
            FROM ranked
            ORDER BY total_volume DESC
        """)

    def running_balance(self):
        """
        Running balance per account — like passbook!
        """
        return self.db.query("""
            SELECT
                account_no,
                customer_name,
                date,
                type,
                amount,
                SUM(
                    CASE WHEN type = 'Credit'
                        THEN amount
                        ELSE -amount
                    END
                ) OVER(
                    PARTITION BY account_no
                    ORDER BY date, id
                    ROWS BETWEEN
                        UNBOUNDED PRECEDING
                        AND CURRENT ROW
                ) AS running_balance
            FROM transactions
            WHERE status = 'Success'
            ORDER BY account_no, date
        """)

    def peak_transaction_hours(self):
        """
        Busiest days per month
        """
        return self.db.query("""
            WITH daily_stats AS (
                SELECT
                    month,
                    day,
                    COUNT(*)              AS txn_count,
                    ROUND(SUM(amount), 2) AS daily_volume
                FROM transactions
                WHERE status = 'Success'
                GROUP BY month, day
            )
            SELECT
                month,
                day,
                txn_count,
                daily_volume,
                RANK() OVER(
                    PARTITION BY month
                    ORDER BY daily_volume DESC
                ) AS rank_in_month
            FROM daily_stats
            ORDER BY month, rank_in_month
        """)

    def fraud_pattern_analysis(self):
        """
        Multi signal fraud detection!
        Like ICICI fraud team!
        """
        return self.db.query("""
            WITH account_patterns AS (
                SELECT
                    account_no,
                    customer_name,
                    COUNT(*)              AS total_txns,
                    ROUND(AVG(amount), 2) AS avg_amount,
                    ROUND(MAX(amount), 2) AS max_amount,
                    SUM(CASE WHEN status = 'Failed'
                        THEN 1 ELSE 0 END) AS failed_count,
                    COUNT(DISTINCT day)   AS active_days
                FROM transactions
                GROUP BY account_no, customer_name
            ),
            global_avg AS (
                SELECT ROUND(AVG(amount), 2) AS avg
                FROM transactions
                WHERE status = 'Success'
            ),
            scored AS (
                SELECT
                    p.*,
                    g.avg AS global_avg,
                    CASE WHEN p.max_amount > g.avg * 3
                        THEN 30 ELSE 0
                    END AS large_txn_risk,
                    CASE WHEN p.total_txns > 50
                        THEN 25 ELSE 0
                    END AS high_freq_risk,
                    CASE WHEN p.failed_count > 3
                        THEN 25 ELSE 0
                    END AS failure_risk,
                    CASE WHEN p.avg_amount > g.avg * 2
                        THEN 20 ELSE 0
                    END AS amount_risk
                FROM account_patterns p, global_avg g
            )
            SELECT
                account_no,
                customer_name,
                total_txns,
                avg_amount,
                max_amount,
                failed_count,
                large_txn_risk + high_freq_risk
                    + failure_risk + amount_risk
                    AS risk_score,
                CASE
                    WHEN large_txn_risk + high_freq_risk
                        + failure_risk + amount_risk >= 50
                        THEN '🚨 Critical'
                    WHEN large_txn_risk + high_freq_risk
                        + failure_risk + amount_risk >= 30
                        THEN '🔴 High Risk'
                    WHEN large_txn_risk + high_freq_risk
                        + failure_risk + amount_risk >= 15
                        THEN '🟡 Medium Risk'
                    ELSE '🟢 Low Risk'
                END AS risk_level
            FROM scored
            ORDER BY risk_score DESC
        """)

    def top_n_per_month(self, n=3):
        """
        Top N customers per month
        Fixed for SQLite — uses subquery!
        """
        return self.db.query(f"""
            SELECT month, customer_name,
                   monthly_volume, monthly_txns,
                   monthly_rank
            FROM (
                SELECT
                    month,
                    customer_name,
                    ROUND(SUM(amount), 2) AS monthly_volume,
                    COUNT(*)              AS monthly_txns,
                    ROW_NUMBER() OVER(
                        PARTITION BY month
                        ORDER BY SUM(amount) DESC
                    ) AS monthly_rank
                FROM transactions
                WHERE status = 'Success'
                GROUP BY month, customer_name
            )
            WHERE monthly_rank <= {n}
            ORDER BY month, monthly_rank
        """)

    def dormant_accounts(self):
        """
        Dormant account detection!
        """
        return self.db.query("""
            WITH last_activity AS (
                SELECT
                    account_no,
                    customer_name,
                    MAX(date)    AS last_txn_date,
                    COUNT(*)     AS total_txns,
                    SUM(CASE WHEN type = 'Credit'
                        THEN amount ELSE -amount
                        END)     AS net_balance
                FROM transactions
                WHERE status = 'Success'
                GROUP BY account_no, customer_name
            )
            SELECT
                account_no,
                customer_name,
                last_txn_date,
                total_txns,
                ROUND(net_balance, 2) AS net_balance,
                CASE
                    WHEN last_txn_date < '2025-06-01'
                        THEN '😴 Dormant'
                    WHEN last_txn_date < '2025-10-01'
                        THEN '💤 Inactive'
                    ELSE '✅ Active'
                END AS account_status
            FROM last_activity
            ORDER BY last_txn_date ASC
        """)
