# Deployment Guide

## For Streamlit Cloud (Recommended)

1. **Push to GitHub** (ensure you've already done this)
   ```bash
   git add .
   git commit -m "Ready for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository: `NiumiMeth/Bond-Maturity-and-Coupon-Schedules`
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Add Secrets (if using PDF extraction)**
   - In Streamlit Cloud dashboard, go to your app → Settings → Secrets
   - Add your API key:
     ```
     GOOGLE_API_KEY = "your-gemini-api-key-here"
     ```

## Environment Variables

The app needs one of these set for PDF extraction to work:
- `GOOGLE_API_KEY` (preferred)
- `GEMINI_API_KEY` (alternative)

Get your API key from: https://aistudio.google.com/apikey

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Create .streamlit/secrets.toml with your API key
echo 'GOOGLE_API_KEY = "your-key"' > .streamlit/secrets.toml

# Run the app
streamlit run streamlit_app.py
```

## Troubleshooting

- If you see "No Gemini API key found", set the environment variable
- If PDF extraction fails, verify your API key is valid
- For Streamlit Cloud issues, check the app logs in your dashboard
