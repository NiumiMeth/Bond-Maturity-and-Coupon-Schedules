# Nipuna Bond Maturity

A FastAPI-based application for processing Sri Lanka Treasury bond maturity and coupon schedules from uploaded CSV files.

## Features
- Upload CSV files containing bond maturity data
- Generate full coupon payment schedules for each bond
- API endpoints for file upload and data processing

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

## Setup
1. Clone the repository or download the project files.
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix/Mac:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App
Start the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```
The app will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API Endpoints
- `POST /upload/` — Upload a CSV file with bond data

## Example CSV Format
```
Maturity Date,Coupon Payment
2028-03-15,1000
2029-09-15,1500
```

## Notes
- The app currently does not provide a frontend UI; interact via API tools like Postman or Swagger UI (`/docs`).
- Coupon schedules are generated in 6-month intervals backward from the maturity date.

## License
MIT License
