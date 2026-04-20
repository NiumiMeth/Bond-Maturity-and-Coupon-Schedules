import streamlit as st

# Set Streamlit page config to wide mode
st.set_page_config(layout="wide")
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

    st.write("### Bonds Maturing Grouped by Month and Coupon Day")
    for month in months:
        month_df = df[df['Month'] == month]
        # Add Day column
        month_df = month_df.copy()
        month_df['Day'] = month_df['Maturity Date'].dt.day
        show_cols = [col for col in ['ISIN', 'Maturity Date', 'Coupon Payment'] if col in month_df.columns]
        with st.expander(f"{month}"):
            # 1st Coupons
            first_df = month_df[month_df['Day'] == 1]
            if not first_df.empty:
                st.subheader("1st Coupons")
                st.table(first_df[show_cols].reset_index(drop=True))
                st.write(f"**Total Coupon Payment (1st):** {first_df['Coupon Payment'].sum():,.2f}")
            # 15th Coupons
            fifteenth_df = month_df[month_df['Day'] == 15]
            if not fifteenth_df.empty:
                st.subheader("15th Coupons")
                st.table(fifteenth_df[show_cols].reset_index(drop=True))
                st.write(f"**Total Coupon Payment (15th):** {fifteenth_df['Coupon Payment'].sum():,.2f}")
            # Special Dates
            special_df = month_df[~month_df['Day'].isin([1, 15])]
            if not special_df.empty:
                st.subheader("Special Date Coupons")
                # Add a column to show the day for clarity
                special_cols = show_cols + ['Day'] if 'Day' not in show_cols else show_cols
                st.table(special_df[special_cols].reset_index(drop=True))
                st.write(f"**Total Coupon Payment (Special Dates):** {special_df['Coupon Payment'].sum():,.2f}")

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
