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
        schedule = generate_full_coupon_schedule(maturity, coupon)
        for entry in schedule:
            entry['Bond Maturity'] = maturity.date()
            all_schedules.append(entry)

    schedule_df = pd.DataFrame(all_schedules)
    st.write("### Full Coupon Schedules", schedule_df)
    st.download_button(
        label="Download Schedules as CSV",
        data=schedule_df.to_csv(index=False),
        file_name="coupon_schedules.csv",
        mime="text/csv"
    )
else:
    st.info("Awaiting CSV file upload.")
