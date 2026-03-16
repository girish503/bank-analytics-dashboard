# src/charts.py
# Purpose: All chart functions using Matplotlib & Seaborn

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd

# ── Global Style Setup ─────────────────────────
# Set once — applies to ALL charts!
sns.set_theme(
    style="darkgrid",
    palette="husl",
    font_scale=1.1
)

COLORS = {
    "green":  "#00d4aa",
    "red":    "#ff4b4b",
    "blue":   "#4b8bff",
    "yellow": "#ffd700",
    "purple": "#9b59b6",
    "orange": "#e67e22",
    "bg":     "#1e2130",
    "text":   "#ffffff"
}


def style_chart(fig, ax, title):
    """Apply consistent dark theme to any chart"""
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])
    ax.set_title(
        title,
        color=COLORS["text"],
        fontsize=14,
        fontweight="bold",
        pad=15
    )
    ax.tick_params(colors=COLORS["text"])
    ax.xaxis.label.set_color(COLORS["text"])
    ax.yaxis.label.set_color(COLORS["text"])
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")
    plt.tight_layout()
    return fig


# ══════════════════════════════════════════════
# CHART 1 — Monthly Revenue Bar Chart
# ══════════════════════════════════════════════
def monthly_revenue_chart(df):
    """
    Bar chart showing monthly transaction volume
    Credits in green, Debits in red!
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    x      = range(len(df))
    width  = 0.35

    # Two bars side by side
    bars1 = ax.bar(
        [i - width/2 for i in x],
        df["total_credits"],
        width,
        label="Credits",
        color=COLORS["green"],
        alpha=0.85,
        edgecolor="white",
        linewidth=0.5
    )
    bars2 = ax.bar(
        [i + width/2 for i in x],
        df["total_debits"],
        width,
        label="Debits",
        color=COLORS["red"],
        alpha=0.85,
        edgecolor="white",
        linewidth=0.5
    )

    # Add value labels on top of bars
    for bar in bars1:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1000,
            f"₹{bar.get_height():,.0f}",
            ha="center",
            va="bottom",
            color=COLORS["text"],
            fontsize=8
        )
    for bar in bars2:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1000,
            f"₹{bar.get_height():,.0f}",
            ha="center",
            va="bottom",
            color=COLORS["text"],
            fontsize=8
        )

    ax.set_xticks(list(x))
    ax.set_xticklabels(df["month"], rotation=15)
    ax.set_ylabel("Amount (₹)")
    ax.legend(
        facecolor=COLORS["bg"],
        labelcolor=COLORS["text"]
    )

    # Format y axis with ₹
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(
            lambda val, _: f"₹{val:,.0f}"
        )
    )

    return style_chart(fig, ax, "Monthly Credits vs Debits")


# ══════════════════════════════════════════════
# CHART 2 — Transaction Type Pie Chart
# ══════════════════════════════════════════════
def transaction_type_pie(df):
    """
    Pie chart showing Credit vs Debit split
    """
    fig, ax = plt.subplots(figsize=(6, 6))

    type_counts = df.groupby("type")["amount"].sum()

    wedges, texts, autotexts = ax.pie(
        type_counts,
        labels=type_counts.index,
        autopct="%1.1f%%",
        colors=[COLORS["green"], COLORS["red"]],
        startangle=90,
        explode=(0.05, 0.05),
        shadow=True,
        textprops={"color": COLORS["text"]}
    )

    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])
    ax.set_title(
        "Credit vs Debit Split",
        color=COLORS["text"],
        fontsize=14,
        fontweight="bold"
    )
    plt.tight_layout()
    return fig


# ══════════════════════════════════════════════
# CHART 3 — Top Customers Horizontal Bar
# ══════════════════════════════════════════════
def top_customers_chart(df):
    """
    Horizontal bar chart — top customers by volume
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Sort and take top 8
    df_sorted = df.nlargest(8, "total_volume")

    bars = ax.barh(
        df_sorted["customer_name"],
        df_sorted["total_volume"],
        color=sns.color_palette("husl", len(df_sorted)),
        edgecolor="white",
        linewidth=0.5,
        height=0.6
    )

    # Add value labels
    for bar in bars:
        ax.text(
            bar.get_width() + 2000,
            bar.get_y() + bar.get_height() / 2,
            f"₹{bar.get_width():,.0f}",
            va="center",
            color=COLORS["text"],
            fontsize=9,
            fontweight="bold"
        )

    ax.set_xlabel("Total Volume (₹)")
    ax.invert_yaxis()

    return style_chart(fig, ax, "Top Customers by Transaction Volume")


# ══════════════════════════════════════════════
# CHART 4 — Daily Transaction Heatmap
# ══════════════════════════════════════════════
def daily_heatmap(df):
    """
    Seaborn heatmap — transactions by day and month
    """
    # Pivot table: rows = day, columns = month
    pivot = df.pivot_table(
        values="amount",
        index="day",
        columns="month",
        aggfunc="sum",
        fill_value=0
    )

    # Order days correctly
    day_order = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]
    pivot = pivot.reindex(
        [d for d in day_order if d in pivot.index]
    )

    fig, ax = plt.subplots(figsize=(16, 5))
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])

    sns.heatmap(
        pivot,
        annot=True,
        fmt=".0f",
        annot_kws={"size": 7},
        cmap="YlOrRd",
        linewidths=0.5,
        linecolor="#333333",
        ax=ax,
        cbar_kws={"shrink": 0.8}
    )

    ax.set_title(
        "Transaction Volume Heatmap (Day × Month)",
        color=COLORS["text"],
        fontsize=14,
        fontweight="bold",
        pad=15
    )
    ax.tick_params(colors=COLORS["text"])
    ax.set_xlabel("Month", color=COLORS["text"])
    ax.set_ylabel("Day", color=COLORS["text"])
    plt.tight_layout()
    return fig


# ══════════════════════════════════════════════
# CHART 5 — Amount Distribution Histogram
# ══════════════════════════════════════════════
def amount_distribution(df):
    """
    Seaborn histogram showing how amounts are distributed
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    sns.histplot(
        data=df,
        x="amount",
        hue="type",
        bins=20,
        palette={
            "Credit": COLORS["green"],
            "Debit":  COLORS["red"]
        },
        alpha=0.7,
        ax=ax,
        edgecolor="white",
        linewidth=0.5
    )

    ax.set_xlabel("Transaction Amount (₹)")
    ax.set_ylabel("Number of Transactions")
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(
            lambda val, _: f"₹{val:,.0f}"
        )
    )
    ax.legend(
        title="Type",
        facecolor=COLORS["bg"],
        labelcolor=COLORS["text"],
        title_fontsize=10
    )

    return style_chart(
        fig, ax,
        "Transaction Amount Distribution"
    )


# ══════════════════════════════════════════════
# CHART 6 — Customer Scatter Plot
# ══════════════════════════════════════════════
def customer_scatter(df):
    """
    Seaborn scatter — total volume vs transaction count
    Bigger bubble = higher average transaction!
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(
        df["total_txns"],
        df["total_volume"],
        s=df["avg_txn"] / 500,     # bubble size!
        c=df["total_volume"],
        cmap="YlOrRd",
        alpha=0.8,
        edgecolors="white",
        linewidth=0.5
    )

    # Add customer name labels
    for _, row in df.iterrows():
        ax.annotate(
            row["customer_name"].split()[0],
            (row["total_txns"], row["total_volume"]),
            textcoords="offset points",
            xytext=(8, 4),
            color=COLORS["text"],
            fontsize=8
        )

    plt.colorbar(
        scatter,
        ax=ax,
        label="Total Volume"
    )

    ax.set_xlabel("Number of Transactions")
    ax.set_ylabel("Total Volume (₹)")

    return style_chart(
        fig, ax,
        "Customer: Volume vs Transaction Count\n"
        "(bubble size = avg transaction amount)"
    )