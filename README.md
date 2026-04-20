# Bond Maturity & Coupon Schedules Dashboard

A Streamlit-based application for analyzing Sri Lanka Treasury bond maturity and coupon payment schedules. Upload CSV files with bond data and view organized coupon payment schedules grouped by month and coupon day (1st, 15th, or special dates).

## 🚀 Live Demo

**[Access the app here →](https://bond-maturity-and-coupon-schedules.streamlit.app/)**

## ✨ Features

- **CSV Upload** — Upload bond maturity data with ISIN, maturity dates, and coupon payments
- **Monthly Grouping** — View bonds organized by maturity month across all years
- **Coupon Day Separation** — Automatically separates 1st, 15th, and special coupon payment dates
- **Total Calculations** — Calculates total coupon payments for each group
- **Wide Table Format** — Clear, readable tables with thousand separators
- **PDF Extraction** *(optional)* — Extract bond data from PDF documents using AI
- **Data Export** — Download summarized data as JSON
- **Professional Dashboard** — Treasury-focused UI with real-time timestamp

## 📋 Sample Data Format

```csv
Maturity Date,ISIN,Series,Face Value (Rs Mn),Coupon Rate,Semiannual Coupon Payment
15-May-26,LKB00426E154,22.50%2026A,"145,060.96",22.50%,16319.358
1-Jun-26,LKB01226F014,11.00%2026A,"229,046.39",11.00%,12597.55145
```

## 🏗️ Project Structure

```
d:\Nipuna Bond Maturity
├── streamlit_app.py          # Main Streamlit application
├── main.py                   # FastAPI backend (optional)
├── requirements.txt          # Python dependencies
├── sample_bonds.csv          # Sample bond data
├── README.md                 # This file
├── DEPLOYMENT.md             # Deployment instructions
└── .streamlit/               # Streamlit configuration
    └── config.toml
```

## 🛠️ Local Setup

### Requirements
- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/NiumiMeth/Bond-Maturity-and-Coupon-Schedules.git
   cd "Nipuna Bond Maturity"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run streamlit_app.py
   ```

The app will open at `http://localhost:8501`

## 🔧 Configuration

### Optional PDF Extraction

If you want to use the PDF extraction feature:

1. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Set the environment variable:
   ```bash
   # Windows
   set GOOGLE_API_KEY=your-key-here
   
   # Mac/Linux
   export GOOGLE_API_KEY=your-key-here
   ```

3. Upload PDF bond documents (settlement schedules, prospectuses, term sheets)

## 📊 How to Use

1. **Open the app** — Visit the [live demo](https://bond-maturity-and-coupon-schedules.streamlit.app/)
2. **Upload CSV** — Select and upload your bond data CSV file
3. **View Results** — Browse bonds grouped by month and coupon day
4. **Export Data** — Download the summarized data as JSON

## 🚀 Deployment

The app is deployed on **Streamlit Cloud**. To deploy your own:

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" and select your repository
4. Add API secrets in the app settings (if using PDF extraction)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📝 License

MIT License

## 👨‍💼 Author

**NiumiMeth** — Central Bank of Sri Lanka Fixed Income Operations
