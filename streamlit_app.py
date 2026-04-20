import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Treasury Bond Dashboard",
    page_icon="🏛️"
)

import pandas as pd
from datetime import datetime
import json

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0D1117;
    color: #E0E6F0;
}
.stApp {
    background: linear-gradient(135deg, #0D1117 0%, #111827 60%, #0f1922 100%);
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px; }

/* ── Page header ── */
.treasury-header {
    border-bottom: 1px solid #C9A84C44;
    padding-bottom: 1.5rem;
    margin-bottom: 2.5rem;
}
.treasury-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #E8D5A3;
    letter-spacing: 0.02em;
    margin: 0;
    line-height: 1.2;
}
.treasury-header .subtitle {
    font-size: 0.85rem;
    color: #6B7FA3;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.treasury-header .timestamp {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #4B5E7A;
    margin-top: 0.2rem;
}

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    background: #131D2B;
    border: 1px dashed #C9A84C55;
    border-radius: 8px;
    padding: 1rem;
}
[data-testid="stFileUploader"]:hover {
    border-color: #C9A84CAA;
}
[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
}
[data-testid="stFileUploaderDropzone"] p {
    color: #6B7FA3;
}

/* ── Metric cards ── */
.metric-row {
    display: flex;
    gap: 1.2rem;
    margin-bottom: 2.5rem;
}
.metric-card {
    flex: 1;
    background: linear-gradient(135deg, #131D2B, #0F1820);
    border: 1px solid #1E2E42;
    border-top: 2px solid #C9A84C;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
}
.metric-card .label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #5A7095;
    margin-bottom: 0.5rem;
}
.metric-card .value {
    font-family: 'DM Mono', monospace;
    font-size: 1.6rem;
    font-weight: 500;
    color: #E8D5A3;
    line-height: 1;
}
.metric-card .sub {
    font-size: 0.75rem;
    color: #4B5E7A;
    margin-top: 0.4rem;
}

/* ── Section header ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    color: #C9A84C;
    letter-spacing: 0.04em;
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #1E2E42;
}

/* ── Month expander ── */
[data-testid="stExpander"] {
    background: #0F1820 !important;
    border: 1px solid #1E2E42 !important;
    border-radius: 8px !important;
    margin-bottom: 0.7rem !important;
}
[data-testid="stExpander"] summary {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.95rem;
    color: #C4D4E8 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.9rem 1.2rem !important;
}
[data-testid="stExpander"] summary:hover {
    color: #E8D5A3 !important;
}

/* ── Badge ── */
.badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    padding: 0.2rem 0.65rem;
    border-radius: 3px;
    font-weight: 500;
    letter-spacing: 0.06em;
}
.badge-gold {
    background: #C9A84C22;
    color: #C9A84C;
    border: 1px solid #C9A84C44;
}
.badge-blue {
    background: #3B82F622;
    color: #93C5FD;
    border: 1px solid #3B82F633;
}
.badge-teal {
    background: #14B8A622;
    color: #5EEAD4;
    border: 1px solid #14B8A633;
}

/* ── Group label ── */
.group-label {
    font-size: 0.7rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #5A7095;
    margin: 1rem 0 0.6rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.group-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1E2E42;
}

/* ── Data table ── */
.styled-table-wrap {
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid #1E2E42;
    margin-bottom: 0.5rem;
}
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.86rem;
}
.styled-table thead th {
    background: #111827;
    color: #5A7095;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.7rem 1rem;
    text-align: left;
    border-bottom: 1px solid #1E2E42;
}
.styled-table thead th.num {
    text-align: right;
}
.styled-table tbody tr {
    border-bottom: 1px solid #141F2D;
    transition: background 0.15s;
}
.styled-table tbody tr:last-child {
    border-bottom: none;
}
.styled-table tbody tr:hover {
    background: #131D2B;
}
.styled-table tbody td {
    padding: 0.7rem 1rem;
    color: #C4D4E8;
}
.styled-table tbody td.isin {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: #93C5FD;
    letter-spacing: 0.04em;
}
.styled-table tbody td.date {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: #94A3B8;
}
.styled-table tbody td.amount {
    font-family: 'DM Mono', monospace;
    text-align: right;
    color: #E8D5A3;
}
.styled-table tfoot tr {
    background: #111827;
    border-top: 1px solid #C9A84C44;
}
.styled-table tfoot td {
    padding: 0.75rem 1rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.84rem;
    font-weight: 500;
    color: #C9A84C;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.styled-table tfoot td.total-amt {
    text-align: right;
    font-size: 0.95rem;
}

/* ── Info box ── */
.info-box {
    background: #131D2B;
    border: 1px dashed #1E2E42;
    border-radius: 8px;
    padding: 3rem 2rem;
    text-align: center;
    color: #3D5070;
}
.info-box .icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}
.info-box p {
    margin: 0;
    font-size: 0.9rem;
    letter-spacing: 0.05em;
}

/* ── Download btn ── */
.stDownloadButton button {
    background: transparent !important;
    border: 1px solid #C9A84C66 !important;
    color: #C9A84C !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton button:hover {
    background: #C9A84C11 !important;
    border-color: #C9A84CAA !important;
}

/* ── Uploaded data table override ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1E2E42 !important;
    border-radius: 6px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="treasury-header">
    <div class="subtitle">Central Bank of Sri Lanka · Fixed Income Operations</div>
    <h1>Bond Maturity &amp; Coupon Dashboard</h1>
    <div class="timestamp">Generated {datetime.now().strftime('%d %B %Y  ·  %H:%M')} (Colombo Time)</div>
</div>
""", unsafe_allow_html=True)


# ── File Upload ───────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("Upload bond portfolio CSV", type=["csv"], label_visibility="collapsed")

def make_table_html(rows_df, show_cols):
    """Render a styled HTML table with a totals footer."""
    header_cells = ""
    for col in show_cols:
        cls = "num" if col == "Coupon Payment" else ""
        label = col if col != "Coupon Payment" else "Coupon Payment (LKR)"
        header_cells += f'<th class="{cls}">{label}</th>'

    body_rows = ""
    for _, row in rows_df.iterrows():
        body_rows += "<tr>"
        for col in show_cols:
            if col == "ISIN":
                body_rows += f'<td class="isin">{row[col]}</td>'
            elif col == "Maturity Date":
                body_rows += f'<td class="date">{pd.to_datetime(row[col]).strftime("%d %b %Y")}</td>'
            elif col == "Coupon Payment":
                body_rows += f'<td class="amount">{row[col]:,.2f}</td>'
            else:
                body_rows += f'<td>{row[col]}</td>'
        body_rows += "</tr>"

    total = rows_df["Coupon Payment"].sum()
    count = len(rows_df)

    return f"""
<div class="styled-table-wrap">
  <table class="styled-table">
    <thead><tr>{header_cells}</tr></thead>
    <tbody>{body_rows}</tbody>
    <tfoot>
      <tr>
        <td colspan="{len(show_cols)-1}">Total · {count} bond{'s' if count!=1 else ''}</td>
        <td class="total-amt">{total:,.2f}</td>
      </tr>
    </tfoot>
  </table>
</div>
"""


if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ── Column handling ────────────────────────────────────────────────────────
    if "Coupon Payment" in df.columns:
        pass
    elif "Semiannual Coupon Payment" in df.columns:
        df.rename(columns={"Semiannual Coupon Payment": "Coupon Payment"}, inplace=True)
    else:
        st.error("CSV must contain a 'Coupon Payment' or 'Semiannual Coupon Payment' column.")
        st.stop()

    df["Maturity Date"] = pd.to_datetime(df["Maturity Date"])
    df["Coupon Payment"] = df["Coupon Payment"].astype(float)
    df["Month"] = df["Maturity Date"].dt.strftime("%B")
    df["MonthNum"] = df["Maturity Date"].dt.month
    df["Day"] = df["Maturity Date"].dt.day

    # ── KPI cards ──────────────────────────────────────────────────────────────
    total_bonds   = len(df)
    total_coupon  = df["Coupon Payment"].sum()
    unique_months = df["Month"].nunique()
    avg_coupon    = df["Coupon Payment"].mean()

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card">
        <div class="label">Total Bonds</div>
        <div class="value">{total_bonds}</div>
        <div class="sub">Instruments in portfolio</div>
      </div>
      <div class="metric-card">
        <div class="label">Total Coupon Obligations</div>
        <div class="value">LKR {total_coupon:,.0f}</div>
        <div class="sub">Aggregate semiannual outflow</div>
      </div>
      <div class="metric-card">
        <div class="label">Active Months</div>
        <div class="value">{unique_months}</div>
        <div class="sub">Months with coupon events</div>
      </div>
      <div class="metric-card">
        <div class="label">Avg Coupon / Bond</div>
        <div class="value">LKR {avg_coupon:,.0f}</div>
        <div class="sub">Mean per instrument</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Month Schedule ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Coupon Schedule by Month &amp; Settlement Date</div>', unsafe_allow_html=True)

    months_order = df.sort_values("MonthNum")["Month"].unique()
    show_cols = [c for c in ["ISIN", "Maturity Date", "Coupon Payment"] if c in df.columns]

    for month in months_order:
        month_df = df[df["Month"] == month].copy()
        month_total = month_df["Coupon Payment"].sum()
        bond_count  = len(month_df)

        with st.expander(f"{month}  ·  LKR {month_total:,.0f}  ·  {bond_count} bond{'s' if bond_count!=1 else ''}"):

            first_df   = month_df[month_df["Day"] == 1]
            fifteen_df = month_df[month_df["Day"] == 15]
            special_df = month_df[~month_df["Day"].isin([1, 15])]

            if not first_df.empty:
                st.markdown('<div class="group-label"><span class="badge badge-gold">1st</span> Settlement</div>', unsafe_allow_html=True)
                st.markdown(make_table_html(first_df, show_cols), unsafe_allow_html=True)

            if not fifteen_df.empty:
                st.markdown('<div class="group-label"><span class="badge badge-blue">15th</span> Settlement</div>', unsafe_allow_html=True)
                st.markdown(make_table_html(fifteen_df, show_cols), unsafe_allow_html=True)

            if not special_df.empty:
                st.markdown('<div class="group-label"><span class="badge badge-teal">Special Date</span> Settlement</div>', unsafe_allow_html=True)
                special_show = show_cols + (["Day"] if "Day" not in show_cols else [])
                st.markdown(make_table_html(special_df, special_show), unsafe_allow_html=True)

    # ── Raw data ───────────────────────────────────────────────────────────────
    with st.expander("View Raw Uploaded Data"):
        st.dataframe(df.drop(columns=["Month", "MonthNum", "Day"], errors="ignore"), use_container_width=True)

    # ── Download ───────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    output_json = []
    for month in months_order:
        month_df = df[df["Month"] == month]
        bonds = month_df[show_cols].copy()
        bonds["Maturity Date"] = bonds["Maturity Date"].dt.strftime("%Y-%m-%d")
        output_json.append({"Month": month, "TotalCoupon": round(month_df["Coupon Payment"].sum(), 2), "Bonds": bonds.to_dict(orient="records")})

    st.download_button(
        label="⬇  Export Portfolio JSON",
        data=json.dumps(output_json, indent=2, default=str),
        file_name="bond_portfolio_schedule.json",
        mime="application/json"
    )

else:
    st.markdown("""
    <div class="info-box">
      <div class="icon">🏛️</div>
      <p>Upload a CSV file containing your bond portfolio to begin.<br>
      Required columns: <strong>ISIN</strong>, <strong>Maturity Date</strong>, <strong>Coupon Payment</strong></p>
    </div>
    """, unsafe_allow_html=True)