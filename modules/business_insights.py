import streamlit as st
import pandas as pd

def show(df: pd.DataFrame, segments: pd.DataFrame):
    """Business Insights page. Every insight below is computed from the
    actual data, not hardcoded — so it stays correct if the underlying
    data changes."""
    st.title("💡 Business Insights & Recommendations")

    df = df.copy()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Month"] = df["InvoiceDate"].dt.to_period("M")
    df["CustomerID"] = df["CustomerID"].astype(int)
    segments = segments.copy()
    segments["CustomerID"] = segments["CustomerID"].astype(int)

    merged = df.merge(segments[["CustomerID", "Segment"]], on="CustomerID", how="left")

    # --- Headline numbers ---
    top_country = df.groupby("Country")["TotalPrice"].sum().idxmax()
    top_product = df.groupby("Description")["Quantity"].sum().idxmax()

    st.subheader("📊 Executive Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"🌍 Top Revenue Country: {top_country}")
    with col2:
        st.success(f"🛍️ Best Selling Product: {top_product}")

    st.subheader("👥 Revenue Concentration by Segment")

    rev_by_seg = merged.groupby("Segment")["TotalPrice"].sum().sort_values(ascending=False)
    cust_by_seg = segments["Segment"].value_counts()
    rev_pct = (rev_by_seg / rev_by_seg.sum() * 100).round(1)
    cust_pct = (cust_by_seg / cust_by_seg.sum() * 100).round(1)

    summary_table = pd.DataFrame({
        "Customers": cust_by_seg,
        "% of Customers": cust_pct,
        "Revenue": rev_by_seg.round(0),
        "% of Revenue": rev_pct,
    }).fillna(0)
    st.dataframe(summary_table, use_container_width=True)

    if "High-Value" in summary_table.index:
        hv = summary_table.loc["High-Value"]
        st.info(
            f"💎 Just **{hv['% of Customers']:.1f}%** of customers (High-Value) drive "
            f"**{hv['% of Revenue']:.1f}%** of total revenue. Losing even a few of these "
            f"customers has an outsized impact — prioritize account-level retention "
            f"(dedicated support, early access, loyalty perks) over broad promotions for this group."
        )

    if "At-Risk" in summary_table.index:
        ar = summary_table.loc["At-Risk"]
        st.warning(
            f"⚠️ **At-Risk** customers make up **{ar['% of Customers']:.1f}%** of the customer "
            f"base but only **{ar['% of Revenue']:.1f}%** of revenue — meaning most of them were "
            f"low-value even before going dormant. A broad, low-cost win-back email is a better use "
            f"of budget here than a high-cost personalized campaign."
        )

    if "Occasional" in summary_table.index:
        occ = summary_table.loc["Occasional"]
        st.info(
            f"📈 **Occasional** customers are the long tail: **{occ['% of Customers']:.1f}%** of "
            f"customers generating **{occ['% of Revenue']:.1f}%** of revenue. Converting even a small "
            f"share of this group into Regular buyers (e.g. a second-purchase discount) would move "
            f"the revenue needle more than optimizing the already-small High-Value segment."
        )

    st.subheader("📅 Revenue Trend")

    monthly = df.groupby("Month")["TotalPrice"].sum()
    partial_month = monthly.index[-1]
    is_partial = df[df["Month"] == partial_month]["InvoiceDate"].max().day < 25

    trend_series = monthly.iloc[:-1] if is_partial else monthly
    best_month = trend_series.idxmax()

    st.line_chart(trend_series)
    st.success(f"📅 Highest Revenue Month: {best_month} (${trend_series.max():,.0f})")
    if is_partial:
        st.caption(
            f"Note: {partial_month} is excluded from the trend above because the data only "
            f"covers a partial month (through day "
            f"{df[df['Month'] == partial_month]['InvoiceDate'].max().day}) — including it would "
            f"look like a revenue drop that hasn't actually happened yet."
        )

    st.subheader("📦 Product Concentration")
    prod_rev = df.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False)
    top10_share = prod_rev.head(10).sum() / prod_rev.sum() * 100
    st.info(
        f"📦 The top 10 products (out of {len(prod_rev):,}) account for only "
        f"**{top10_share:.1f}%** of revenue — this catalog has a long tail rather than "
        f"a few blockbuster SKUs, so stock breadth matters more than deep stock on a handful of items."
    )

    st.subheader("Business Recommendation")

    recommendations = []

    if "High-Value" in summary_table.index:
        hv = summary_table.loc["High-Value"]
        recommendations.append({
            "priority": "High",
            "title": "Protect the High-Value segment",
            "impact": f"{hv['% of Revenue']:.1f}% of revenue from only {hv['% of Customers']:.1f}% of customers",
            "action": (
                "Set up an account-level churn alert (e.g. no purchase in 60 days) and assign "
                "these customers a dedicated point of contact or early access to new stock. "
                "Losing even one of these customers is measurably expensive — retention here "
                "should be handled manually, not through mass email."
            ),
        })

    if "Occasional" in summary_table.index:
        occ = summary_table.loc["Occasional"]
        recommendations.append({
            "priority": "High",
            "title": "Convert Occasional buyers into repeat customers",
            "impact": f"{occ['% of Customers']:.1f}% of customers, {occ['% of Revenue']:.1f}% of revenue — the largest growth lever",
            "action": (
                "Trigger a time-limited second-purchase discount a few days after a customer's "
                "first order. Even a 5-10% lift in repeat-purchase rate here moves more total "
                "revenue than any change to the High-Value segment, simply due to volume."
            ),
        })

    if "At-Risk" in summary_table.index:
        ar = summary_table.loc["At-Risk"]
        recommendations.append({
            "priority": "Medium",
            "title": "Run a low-cost win-back campaign for At-Risk customers",
            "impact": f"{ar['% of Customers']:.1f}% of customers but only {ar['% of Revenue']:.1f}% of revenue",
            "action": (
                "Use automated, templated win-back emails rather than personalized outreach — "
                "this group's historical spend doesn't justify high-touch effort per customer, "
                "but the sheer headcount makes a cheap, broad campaign worthwhile."
            ),
        })

    recommendations.append({
        "priority": "Medium",
        "title": "Maintain broad inventory coverage",
        "impact": f"Top 10 of {len(prod_rev):,} products are only {top10_share:.1f}% of revenue",
        "action": (
            "This is a long-tail catalog, not a hits-driven one. Stockouts on lower-volume "
            "products carry more real revenue risk than they appear to — prioritize breadth "
            "of availability over deep stock on a handful of bestsellers."
        ),
    })

    recommendations.append({
        "priority": "Low",
        "title": f"Plan staffing and inventory around {best_month.strftime('%B') if hasattr(best_month, 'strftime') else best_month}",
        "impact": f"Highest revenue month observed (${trend_series.max():,.0f})",
        "action": (
            "Increase marketing spend and ensure fulfillment capacity is scaled up in the weeks "
            "leading into this period, based on the seasonal pattern in the data so far."
        ),
    })

    priority_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

    for rec in recommendations:
        with st.container(border=True):
            st.markdown(f"**{priority_colors[rec['priority']]} {rec['priority']} priority — {rec['title']}**")
            st.caption(f"Impact: {rec['impact']}")
            st.write(rec["action"])