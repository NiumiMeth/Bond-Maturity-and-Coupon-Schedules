import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def generate_full_coupon_schedule(maturity_date: datetime, coupon_payment: float):
    dates = []
    current = maturity_date
    while current.year >= 2000:
        dates.append({
            "Date": current,
            "Coupon Payment": coupon_payment
        })
        current -= relativedelta(months=6)
    return dates

st.title("Sri Lanka Bond Maturity & Coupon Schedules")
st.write("Upload a CSV file with bond data to generate coupon schedules.")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data", df)

    # Clean and parse columns
    df['Maturity Date'] = pd.to_datetime(df['Maturity Date'])

    # Accept both 'Coupon Payment' and 'Semiannual Coupon Payment'
    coupon_col = None
    if 'Coupon Payment' in df.columns:
        coupon_col = 'Coupon Payment'
    elif 'Semiannual Coupon Payment' in df.columns:
        coupon_col = 'Semiannual Coupon Payment'
        df.rename(columns={'Semiannual Coupon Payment': 'Coupon Payment'}, inplace=True)
    else:
        st.error("CSV must contain a 'Coupon Payment' or 'Semiannual Coupon Payment' column.")
        st.stop()

    df['Coupon Payment'] = df['Coupon Payment'].astype(float)

    all_schedules = []
    for _, row in df.iterrows():
        maturity = row['Maturity Date']
        coupon = row['Coupon Payment']
        # Use ISIN or Maturity Date as bond identifier
        bond_id = row['ISIN'] if 'ISIN' in df.columns else str(maturity.date())
        schedule = generate_full_coupon_schedule(maturity, coupon)
        for entry in schedule:
            all_schedules.append({
                "Date": entry["Date"].strftime("%d-%b-%Y"),
                "Month-Year": entry["Date"].strftime("%b-%Y"),
                "Day": entry["Date"].day,
                "Coupon Payment": entry["Coupon Payment"],
                "Bond": bond_id
            })

    schedule_df = pd.DataFrame(all_schedules)

    # Add Month column for grouping
    schedule_df['Month'] = pd.to_datetime(schedule_df['Date'], format='%d-%b-%Y').dt.strftime('%B')
    months = schedule_df['Month'].unique()
    months_sorted = pd.to_datetime(months, format='%B').month.argsort()
    months = [months[i] for i in months_sorted]

    st.write("### Coupon Payments Grouped by Month")
    for month in months:
        month_df = schedule_df[schedule_df['Month'] == month]
        with st.expander(f"{month}"):
            # Group by Date within the month
            for date, group in month_df.groupby('Date'):
                total_coupon = group["Coupon Payment"].sum()
                bonds_table = group[["Bond", "Coupon Payment"]].reset_index(drop=True)
                st.write(f"**Date:** {date}  |  **Total Coupon Payment:** {total_coupon:,.2f}")
                st.table(bonds_table)

    # Optionally, allow download of the grouped data as JSON
    import json
    output_json = []
    for month in months:
        month_df = schedule_df[schedule_df['Month'] == month]
        month_entry = {"Month": month, "Dates": []}
        for date, group in month_df.groupby('Date'):
            total_coupon = group["Coupon Payment"].sum()
            bonds = group[["Bond", "Coupon Payment"]].to_dict(orient="records")
            month_entry["Dates"].append({
                "Date": date,
                "Total_Coupon_Payment": round(total_coupon, 2),
                "Bonds": bonds
            })
        output_json.append(month_entry)
    st.download_button(
        label="Download Grouped Data as JSON",
        data=json.dumps(output_json, indent=2),
        file_name="coupon_schedules_grouped_by_month.json",
        mime="application/json"
    )
else:
    st.info("Awaiting CSV file upload.")
