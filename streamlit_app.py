import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


# No need for generate_full_coupon_schedule anymore

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


    # Add Month column for grouping
    df['Month'] = df['Maturity Date'].dt.strftime('%B')
    months = df['Month'].unique()
    months_sorted = pd.to_datetime(months, format='%B').month.argsort()
    months = [months[i] for i in months_sorted]

    st.write("### Bonds Maturing Grouped by Month")
    for month in months:
        month_df = df[df['Month'] == month]
        with st.expander(f"{month}"):
            # Show table of ISIN, Maturity Date, Coupon Payment
            show_cols = [col for col in ['ISIN', 'Maturity Date', 'Coupon Payment'] if col in month_df.columns]
            st.table(month_df[show_cols].reset_index(drop=True))

    # Optionally, allow download of the grouped data as JSON
    import json
    output_json = []
    for month in months:
        month_df = df[df['Month'] == month]
        bonds = month_df[[col for col in ['ISIN', 'Maturity Date', 'Coupon Payment'] if col in month_df.columns]].to_dict(orient="records")
        output_json.append({
            "Month": month,
            "Bonds": bonds
        })
    st.download_button(
        label="Download Grouped Data as JSON",
        data=json.dumps(output_json, indent=2, default=str),
        file_name="bonds_grouped_by_month.json",
        mime="application/json"
    )
else:
    st.info("Awaiting CSV file upload.")
