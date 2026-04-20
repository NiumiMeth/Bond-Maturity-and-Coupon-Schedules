import io
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = FastAPI()


def generate_full_coupon_schedule(maturity_date: datetime, coupon_payment: float):
    """
    Generate ALL coupon dates going backwards from maturity in 6-month steps.
    The coupon day stays the same as the maturity day (1st, 15th, or irregular).
    Lower bound is year 2000 — no Sri Lanka T-bond was issued before that.
    """
    dates = []
    current = maturity_date
    while current.year >= 2000:
        dates.append({
            "Date": current,
            "Coupon Payment": coupon_payment
        })
        current -= relativedelta(months=6)
    return dates


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):

    # Read the uploaded CSV file
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    # Drop empty rows
    df.dropna(subset=['Maturity Date'], inplace=True)

    # Parse maturity date
    df['Maturity Date'] = pd.to_datetime(df['Maturity Date'])

    # Clean Face Value — remove commas
    df['Face Value (Rs Mn)'] = (
        df['Face Value (Rs Mn)']
        .astype(str)
        .str.replace(',', '', regex=False)
        .astype(float)
    )

    # Clean Coupon Rate — remove % sign
    df['Coupon Rate'] = (
        df['Coupon Rate']
        .astype(str)
        .str.replace('%', '', regex=False)
        .astype(float) / 100
    )

    # Clean Semiannual Coupon Payment — remove commas if any
    df['Semiannual Coupon Payment'] = (
        df['Semiannual Coupon Payment']
        .astype(str)
        .str.replace(',', '', regex=False)
        .astype(float)
    )

    rows = []

    for _, row in df.iterrows():
        maturity       = row['Maturity Date']
        coupon_payment = row['Semiannual Coupon Payment']  # use pre-calculated column
        isin           = row['ISIN']
        series         = row['Series']

        schedule = generate_full_coupon_schedule(maturity, coupon_payment)

        for entry in schedule:
            rows.append({
                "Date":           entry["Date"],
                "Month-Year":     entry["Date"].strftime("%b-%Y"),
                "Day":            entry["Date"].day,
                "Coupon Payment": entry["Coupon Payment"],
                "Maturity Date":  maturity.strftime("%d-%b-%Y"),
                "ISIN":           isin,
                "Series":         series
            })

    expanded_df = pd.DataFrame(rows)

    # Sort by actual date before grouping
    expanded_df.sort_values("Date", inplace=True)

    # Group by date and sum coupon payments
    result = (
        expanded_df
        .groupby(["Date", "Month-Year", "Day"], as_index=False)
        .agg(
            Total_Coupon_Payment=("Coupon Payment", "sum"),
            Bonds=("Maturity Date", lambda x: sorted(set(x)))  # which bonds pay on this date
        )
    )

    # Format date nicely for output
    result["Date"] = result["Date"].dt.strftime("%d-%b-%Y")

    # Round total coupon payment to 2 decimal places
    result["Total_Coupon_Payment"] = result["Total_Coupon_Payment"].round(2)

    return JSONResponse(content=result.to_dict(orient="records"))