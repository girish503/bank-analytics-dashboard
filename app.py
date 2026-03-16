# app.py — Full Professional Version
# Run: streamlit run app.py

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from src.analyzer import BankAnalyzer
from src.charts import (
    monthly_revenue_chart,
    transaction_type_pie,
    top_customers_chart,
    daily_heatmap,
    amount_distribution,
    customer_scatter
)
from src.database_handler import DatabaseHandler

# ── Page Config ───────────────────────────────
st.set_page_config(
    page_title="BankIQ Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #0a0e1a; }
#MainMenu {visibility: hidden;}
footer    {visibility: hidden;}
header    {visibility: hidden;}
.kpi-green {
    background: linear-gradient(135deg,#0d2b1f,#0f3d2a);
    border-left: 4px solid #00d4aa;
    border-radius: 12px; padding: 20px;
    text-align: center; margin-bottom: 10px;
}
.kpi-red {
    background: linear-gradient(135deg,#2b0d0d,#3d1010);
    border-left: 4px solid #ff4b4b;
    border-radius: 12px; padding: 20px;
    text-align: center; margin-bottom: 10px;
}
.kpi-blue {
    background: linear-gradient(135deg,#0d1b2b,#0f2a3d);
    border-left: 4px solid #4b8bff;
    border-radius: 12px; padding: 20px;
    text-align: center; margin-bottom: 10px;
}
.kpi-gold {
    background: linear-gradient(135deg,#2b2000,#3d2f00);
    border-left: 4px solid #ffd700;
    border-radius: 12px; padding: 20px;
    text-align: center; margin-bottom: 10px;
}
.kpi-purple {
    background: linear-gradient(135deg,#1a0d2b,#2a0f3d);
    border-left: 4px solid #9b59b6;
    border-radius: 12px; padding: 20px;
    text-align: center; margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────
analyzer = BankAnalyzer()
db       = DatabaseHandler()
all_txns = db.query("SELECT * FROM transactions")

# ── KPI Card Function ─────────────────────────
def kpi_card(label, value, color="green", icon="💰"):
    st.markdown(f"""
        <div class="kpi-{color}">
            <h1 style="color:white;margin:0;
                font-size:26px;">{icon}</h1>
            <h2 style="color:white;margin:5px 0;
                font-size:20px;">{value}</h2>
            <p style="color:#aaa;margin:0;
                font-size:12px;">{label}</p>
        </div>
    """, unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/bank.png",
        width=60
    )
    st.title("🏦 BankIQ Analytics")
    st.caption("v3.0 — Enterprise Edition")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Customers",
            "Transactions",
            "Risk Center",
            "Growth Analysis",
            "Fraud Detection",
            "Account Monitor",
            "Reports"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.subheader("🔍 Global Filters")
    month_list = list(
        db.query(
            "SELECT DISTINCT month "
            "FROM transactions ORDER BY month"
        )["month"]
    )
    selected_months = st.multiselect(
        "Filter by Month",
        options=month_list,
        default=[]
    )
    st.caption("Empty = show all months")

# ── Apply Global Filter ───────────────────────
if selected_months:
    filtered_txns = all_txns[
        all_txns["month"].isin(selected_months)
    ]
else:
    filtered_txns = all_txns


# ════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ════════════════════════════════════════════
if page == "Overview":

    st.title("📊 Executive Overview")
    summary = analyzer.monthly_summary()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        kpi_card("Total Transactions",
            int(summary["total_transactions"].sum()),
            "blue", "💳")
    with col2:
        kpi_card("Total Volume",
            f"₹{summary['total_volume'].sum():,.0f}",
            "green", "💰")
    with col3:
        kpi_card("Total Credits",
            f"₹{summary['total_credits'].sum():,.0f}",
            "green", "⬆️")
    with col4:
        kpi_card("Total Debits",
            f"₹{summary['total_debits'].sum():,.0f}",
            "red", "⬇️")
    with col5:
        success = all_txns[all_txns["status"]=="Success"]
        rate = round(len(success)/len(all_txns)*100, 1)
        kpi_card("Success Rate",
            f"{rate}%", "gold", "✅")

    st.divider()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📈 Monthly Credits vs Debits")
        fig = monthly_revenue_chart(summary)
        st.pyplot(fig)
    with col2:
        st.subheader("🔵 Transaction Split")
        fig = transaction_type_pie(filtered_txns)
        st.pyplot(fig)

    st.divider()

    st.subheader("🔥 Activity Heatmap")
    fig = daily_heatmap(filtered_txns)
    st.pyplot(fig)

    st.divider()

    st.subheader("📊 Amount Distribution")
    fig = amount_distribution(filtered_txns)
    st.pyplot(fig)

    st.divider()

    st.subheader("📋 Monthly Breakdown")
    st.dataframe(summary, use_container_width=True,
                 hide_index=True)


# ════════════════════════════════════════════
# PAGE 2 — CUSTOMERS
# ════════════════════════════════════════════
elif page == "Customers":

    st.title("👥 Customer Analysis")

    top  = analyzer.top_customers(10)
    segs = analyzer.customer_segmentation()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        plat = len(segs[segs["segment"]=="💎 Platinum"])
        kpi_card("Platinum Customers",
                 plat, "purple", "💎")
    with col2:
        gold = len(segs[segs["segment"]=="🥇 Gold"])
        kpi_card("Gold Customers", gold, "gold", "🥇")
    with col3:
        silv = len(segs[segs["segment"]=="🥈 Silver"])
        kpi_card("Silver Customers", silv, "blue", "🥈")
    with col4:
        basic = len(segs[segs["segment"]=="🥉 Basic"])
        kpi_card("Basic Customers", basic, "green", "🥉")

    st.divider()

    st.subheader("🏆 Top Customers by Volume")
    fig = top_customers_chart(top)
    st.pyplot(fig)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Customer Segments")
        st.dataframe(segs, use_container_width=True,
                     hide_index=True)
    with col2:
        st.subheader("🔵 Intelligence Map")
        fig = customer_scatter(top)
        st.pyplot(fig)

    st.divider()

    st.subheader("🏛️ Account Balance Summary")
    st.dataframe(analyzer.account_summary(),
                 use_container_width=True,
                 hide_index=True)


# ════════════════════════════════════════════
# PAGE 3 — TRANSACTIONS
# ════════════════════════════════════════════
elif page == "Transactions":

    st.title("💳 Transaction Details")

    col1, col2, col3 = st.columns(3)
    with col1:
        status_f = st.selectbox(
            "Status", ["All","Success","Failed"])
    with col2:
        type_f = st.selectbox(
            "Type", ["All","Credit","Debit"])
    with col3:
        month_opts = ["All"] + list(
            all_txns["month"].dropna().unique())
        month_f = st.selectbox("Month", month_opts)

    filtered = all_txns.copy()
    if status_f != "All":
        filtered = filtered[
            filtered["status"]==status_f]
    if type_f != "All":
        filtered = filtered[
            filtered["type"]==type_f]
    if month_f != "All":
        filtered = filtered[
            filtered["month"]==month_f]

    st.caption(
        f"Showing {len(filtered)} of "
        f"{len(all_txns)} transactions"
    )
    st.dataframe(filtered, use_container_width=True,
                 hide_index=True)

    st.divider()

    if len(filtered) > 0:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            kpi_card("Count", len(filtered),
                     "blue","🔢")
        with col2:
            kpi_card("Total",
                f"₹{filtered['amount'].sum():,.0f}",
                "green","💰")
        with col3:
            kpi_card("Average",
                f"₹{filtered['amount'].mean():,.0f}",
                "gold","📊")
        with col4:
            kpi_card("Highest",
                f"₹{filtered['amount'].max():,.0f}",
                "red","⬆️")


# ════════════════════════════════════════════
# PAGE 4 — RISK CENTER
# ════════════════════════════════════════════
elif page == "Risk Center":

    st.title("⚠️ Risk & Alerts Center")

    suspicious = analyzer.suspicious_transactions()
    failed     = analyzer.failed_transactions()

    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_card("Suspicious", len(suspicious),
                 "red","🚨")
    with col2:
        kpi_card("Failed", len(failed), "red","❌")
    with col3:
        risk = 0
        if len(suspicious) > 0:
            risk += suspicious["amount"].sum()
        if len(failed) > 0:
            risk += failed["amount"].sum()
        kpi_card("Total Risk Amount",
                 f"₹{risk:,.0f}", "gold","⚠️")

    st.divider()

    st.subheader("🔴 Suspicious Transactions")
    if len(suspicious) > 0:
        st.error(f"🚨 {len(suspicious)} detected!")
        st.dataframe(suspicious,
                     use_container_width=True,
                     hide_index=True)
    else:
        st.success("✅ None found!")

    st.divider()

    st.subheader("❌ Failed Transactions")
    if len(failed) > 0:
        st.warning(f"⚠️ {len(failed)} found!")
        st.dataframe(failed,
                     use_container_width=True,
                     hide_index=True)
    else:
        st.success("✅ None found!")


# ════════════════════════════════════════════
# PAGE 5 — GROWTH ANALYSIS
# ════════════════════════════════════════════
elif page == "Growth Analysis":

    st.title("📈 Growth Analysis")
    st.caption(
        "Month over month trends "
        "like SBI quarterly reports!"
    )

    growth = analyzer.month_over_month_growth()

    positive = len(growth[growth["trend"]=="📈 Growth"])
    decline  = len(growth[growth["trend"]=="📉 Decline"])

    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_card("Growth Months",
                 positive, "green","📈")
    with col2:
        kpi_card("Decline Months",
                 decline, "red","📉")
    with col3:
        kpi_card("Months Tracked",
                 len(growth), "blue","📅")

    st.divider()

    # ── Growth Chart ──────────────────────────
    st.subheader("📊 Revenue Growth Trend")
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor("#1e2130")
    ax.set_facecolor("#1e2130")

    ax.plot(growth["month"], growth["revenue"],
            color="#00d4aa", marker="o",
            linewidth=2.5, label="Revenue",
            zorder=3)

    colors = [
        "#00d4aa" if t == "📈 Growth"
        else "#ff4b4b"
        for t in growth["trend"]
    ]
    ax.bar(growth["month"], growth["revenue"],
           color=colors, alpha=0.3, zorder=2)

    ax.tick_params(colors="white")
    ax.set_title("Month over Month Revenue",
                 color="white", fontweight="bold")

    # ✅ Clean single formatter — no duplicate!
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(
            lambda x, _: f"₹{x:,.0f}"
        )
    )
    ax.legend(facecolor="#1e2130",
              labelcolor="white")
    plt.xticks(rotation=30)
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()

    st.subheader("📋 Growth Details Table")
    st.dataframe(growth, use_container_width=True,
                 hide_index=True)

    st.divider()

    st.subheader("🏆 Top 3 Per Month")
    top_monthly = analyzer.top_n_per_month(3)
    st.dataframe(top_monthly,
                 use_container_width=True,
                 hide_index=True)


# ════════════════════════════════════════════
# PAGE 6 — FRAUD DETECTION
# ════════════════════════════════════════════
elif page == "Fraud Detection":

    st.title("🔍 Fraud Detection System")
    st.caption(
        "Multi signal fraud scoring "
        "like ICICI fraud team!"
    )

    fraud = analyzer.fraud_pattern_analysis()

    critical = len(fraud[fraud["risk_level"]=="🚨 Critical"])
    high     = len(fraud[fraud["risk_level"]=="🔴 High Risk"])
    medium   = len(fraud[fraud["risk_level"]=="🟡 Medium Risk"])
    low      = len(fraud[fraud["risk_level"]=="🟢 Low Risk"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("Critical Risk",
                 critical, "red","🚨")
    with col2:
        kpi_card("High Risk", high, "red","🔴")
    with col3:
        kpi_card("Medium Risk",
                 medium, "gold","🟡")
    with col4:
        kpi_card("Low Risk", low, "green","🟢")

    st.divider()

    st.subheader("📊 Risk Score Distribution")
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor("#1e2130")
    ax.set_facecolor("#1e2130")

    risk_colors = {
        "🚨 Critical":   "#ff0000",
        "🔴 High Risk":  "#ff4b4b",
        "🟡 Medium Risk":"#ffd700",
        "🟢 Low Risk":   "#00d4aa"
    }
    bar_colors = [
        risk_colors.get(r, "#4b8bff")
        for r in fraud["risk_level"]
    ]

    ax.barh(
        fraud["customer_name"],
        fraud["risk_score"],
        color=bar_colors,
        edgecolor="white",
        linewidth=0.3
    )
    ax.tick_params(colors="white")
    ax.set_xlabel("Risk Score", color="white")
    ax.set_title("Account Risk Scores",
                 color="white", fontweight="bold")
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()

    st.subheader("📋 Full Fraud Analysis Table")
    st.dataframe(fraud, use_container_width=True,
                 hide_index=True)


# ════════════════════════════════════════════
# PAGE 7 — ACCOUNT MONITOR
# ════════════════════════════════════════════
elif page == "Account Monitor":

    st.title("🏛️ Account Monitor")
    st.caption(
        "Running balance + dormant accounts "
        "like bank passbook system!"
    )

    accounts = list(all_txns["account_no"].unique())
    selected_acc = st.selectbox(
        "Select Account to Monitor",
        accounts
    )

    running  = analyzer.running_balance()
    acc_data = running[
        running["account_no"] == selected_acc
    ]

    if len(acc_data) > 0:
        customer = acc_data["customer_name"].iloc[0]
        balance  = acc_data["running_balance"].iloc[-1]

        col1, col2, col3 = st.columns(3)
        with col1:
            kpi_card("Account",
                     selected_acc, "blue","🏦")
        with col2:
            kpi_card("Customer",
                     customer, "gold","👤")
        with col3:
            color = "green" if balance > 0 else "red"
            kpi_card("Current Balance",
                f"₹{balance:,.0f}", color,"💰")

        st.divider()

        st.subheader("📈 Running Balance Over Time")
        fig, ax = plt.subplots(figsize=(12, 4))
        fig.patch.set_facecolor("#1e2130")
        ax.set_facecolor("#1e2130")

        ax.plot(
            range(len(acc_data)),
            acc_data["running_balance"],
            color="#00d4aa",
            linewidth=2,
            marker="o",
            markersize=4
        )
        ax.fill_between(
            range(len(acc_data)),
            acc_data["running_balance"],
            alpha=0.2,
            color="#00d4aa"
        )
        ax.axhline(y=0, color="#ff4b4b",
                   linestyle="--", linewidth=1)
        ax.tick_params(colors="white")
        ax.set_title(
            f"Balance History — {customer}",
            color="white", fontweight="bold"
        )
        ax.yaxis.set_major_formatter(
            mticker.FuncFormatter(
                lambda x, _: f"₹{x:,.0f}"
            )
        )
        plt.tight_layout()
        st.pyplot(fig)

        st.divider()

        st.subheader("📋 Transaction History")
        st.dataframe(
            acc_data[["date","type",
                       "amount","running_balance"]],
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader("😴 Dormant Account Detection")
    dormant = analyzer.dormant_accounts()
    st.dataframe(dormant, use_container_width=True,
                 hide_index=True)


# ════════════════════════════════════════════
# PAGE 8 — REPORTS
# ════════════════════════════════════════════
elif page == "Reports":

    st.title("📈 Executive Reports")

    # ── Cashflow Analysis ─────────────────────
    st.subheader("💰 Cashflow Analysis")
    cashflow = analyzer.cashflow_analysis()
    st.dataframe(cashflow, use_container_width=True,
                 hide_index=True)

    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor("#1e2130")
    ax.set_facecolor("#1e2130")

    ax.plot(cashflow["month"], cashflow["credits"],
            color="#00d4aa", marker="o",
            linewidth=2.5, label="Credits")
    ax.plot(cashflow["month"], cashflow["debits"],
            color="#ff4b4b", marker="o",
            linewidth=2.5, label="Debits")
    ax.fill_between(cashflow["month"],
                    cashflow["credits"],
                    cashflow["debits"],
                    alpha=0.15, color="#00d4aa")
    ax.tick_params(colors="white")
    ax.set_title("Credits vs Debits Over Time",
                 color="white", fontweight="bold")

    # ✅ Clean formatter added here too!
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(
            lambda x, _: f"₹{x:,.0f}"
        )
    )
    ax.legend(facecolor="#1e2130",
              labelcolor="white")
    plt.xticks(rotation=30)
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()

    # ── Account Health ────────────────────────
    st.subheader("🏥 Account Health Scores")
    health = analyzer.account_health_score()
    st.dataframe(health, use_container_width=True,
                 hide_index=True)

    st.divider()

    # ── Transaction Velocity ──────────────────
    st.subheader("⚡ Transaction Velocity")
    velocity = analyzer.transaction_velocity()
    st.dataframe(velocity, use_container_width=True,
                 hide_index=True)
