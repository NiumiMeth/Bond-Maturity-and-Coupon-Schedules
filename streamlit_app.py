import streamlit as st
st.set_page_config(layout="wide", page_title="Coupon Schedules", page_icon="🏛️")

import pandas as pd
import numpy as np
import io
import re
import json
from datetime import date, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=JetBrains+Mono:wght@400;500&family=Outfit:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; background:#09100F; color:#D4E5D0; }
.stApp { background: radial-gradient(ellipse at 20% 0%, #0f1e14 0%, #09100F 55%, #060d0b 100%); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top:2rem; padding-bottom:3rem; max-width:1400px; }

.page-header { border-bottom:1px solid #2A4A3044; padding-bottom:1.5rem; margin-bottom:2.5rem; }
.page-header h1 { font-family:'Cormorant Garamond',serif; font-size:2.6rem; font-weight:700;
  color:#A8D5A2; letter-spacing:.01em; margin:0; line-height:1.1; }
.page-header .sub { font-size:.8rem; color:#3D6B45; letter-spacing:.18em;
  text-transform:uppercase; margin-top:.4rem; }
.page-header .ts { font-family:'JetBrains Mono',monospace; font-size:.75rem;
  color:#2A4A30; margin-top:.25rem; }

/* tabs */
.stTabs [data-baseweb="tab-list"] { background:#0d1a10; border-radius:8px 8px 0 0;
  border:1px solid #1a3020; border-bottom:none; gap:0; }
.stTabs [data-baseweb="tab"] { font-family:'JetBrains Mono',monospace !important;
  font-size:.76rem !important; letter-spacing:.12em !important; text-transform:uppercase !important;
  color:#3D6B45 !important; padding:.7rem 1.5rem !important; }
.stTabs [aria-selected="true"] { color:#A8D5A2 !important;
  border-bottom:2px solid #A8D5A2 !important; background:transparent !important; }
.stTabs [data-baseweb="tab-panel"] { background:#0d1a10; border:1px solid #1a3020;
  border-top:none; border-radius:0 0 8px 8px; padding:1.2rem; }

/* upload */
[data-testid="stFileUploader"] { background:#070f09; border:1px dashed #2A4A3066;
  border-radius:6px; padding:.5rem; }
[data-testid="stFileUploader"]:hover { border-color:#A8D5A288; }
[data-testid="stFileUploaderDropzone"] p { color:#3D6B45; }

/* metrics */
.metric-row { display:flex; gap:1.2rem; margin-bottom:2.5rem; flex-wrap:wrap; }
.mc { flex:1; min-width:160px; background:linear-gradient(135deg,#0f1e14,#0d1a10);
  border:1px solid #1a3020; border-top:2px solid #A8D5A2; border-radius:8px;
  padding:1.2rem 1.5rem; }
.mc.warn { border-top-color:#E8A44A; }
.mc.danger { border-top-color:#E85A4A; }
.mc .lbl { font-size:.7rem; font-weight:500; letter-spacing:.16em; text-transform:uppercase;
  color:#3D6B45; margin-bottom:.5rem; }
.mc .val { font-family:'JetBrains Mono',monospace; font-size:1.55rem; font-weight:500;
  color:#A8D5A2; line-height:1; }
.mc.warn .val { color:#E8A44A; }
.mc.danger .val { color:#E85A4A; }
.mc .sub { font-size:.73rem; color:#2A4A30; margin-top:.4rem; }

.sec-title { font-family:'Cormorant Garamond',serif; font-size:1.2rem; color:#A8D5A2;
  letter-spacing:.04em; margin-bottom:1rem; padding-bottom:.5rem;
  border-bottom:1px solid #1a3020; }

/* badge */
.badge { display:inline-block; font-family:'JetBrains Mono',monospace; font-size:.68rem;
  padding:.18rem .6rem; border-radius:3px; font-weight:500; letter-spacing:.06em; }
.bg { background:#A8D5A222; color:#A8D5A2; border:1px solid #A8D5A244; }
.bw { background:#E8A44A22; color:#E8A44A; border:1px solid #E8A44A44; }
.br { background:#E85A4A22; color:#E85A4A; border:1px solid #E85A4A44; }
.bb { background:#5A9BD422; color:#93C5FD; border:1px solid #5A9BD444; }

/* table */
.tbl-wrap { border-radius:6px; overflow:hidden; border:1px solid #1a3020; margin-bottom:.5rem; }
.tbl { width:100%; border-collapse:collapse; font-size:.84rem; }
.tbl thead th { background:#0a1610; color:#3D6B45; font-size:.66rem; font-weight:500;
  letter-spacing:.16em; text-transform:uppercase; padding:.65rem 1rem;
  text-align:left; border-bottom:1px solid #1a3020; }
.tbl thead th.num { text-align:right; }
.tbl tbody tr { border-bottom:1px solid #0f1e14; transition:background .15s; }
.tbl tbody tr:last-child { border-bottom:none; }
.tbl tbody tr:hover { background:#0f1e14; }
.tbl tbody td { padding:.65rem 1rem; color:#B8D4B4; }
.tbl tbody td.mono { font-family:'JetBrains Mono',monospace; font-size:.8rem; color:#93C5FD; }
.tbl tbody td.dt { font-family:'JetBrains Mono',monospace; font-size:.8rem; color:#7A9B80; }
.tbl tbody td.amt { font-family:'JetBrains Mono',monospace; text-align:right; color:#A8D5A2; }
.tbl tbody td.warn { color:#E8A44A; font-family:'JetBrains Mono',monospace; }
.tbl tfoot tr { background:#0a1610; border-top:1px solid #A8D5A233; }
.tbl tfoot td { padding:.7rem 1rem; font-family:'JetBrains Mono',monospace;
  font-size:.82rem; font-weight:500; color:#A8D5A2; letter-spacing:.08em; }
.tbl tfoot td.ta { text-align:right; font-size:.92rem; }

.info-box { background:#0d1a10; border:1px dashed #1a3020; border-radius:8px;
  padding:3rem 2rem; text-align:center; color:#1E3B25; }
.info-box .ico { font-size:2.5rem; margin-bottom:1rem; }
.info-box p { margin:0; font-size:.9rem; letter-spacing:.05em; }

.warn-box { background:#1a1208; border:1px solid #92400e44;
  border-left:3px solid #E8A44A; border-radius:6px; padding:.9rem 1.2rem;
  font-size:.83rem; color:#FCD34D; margin:.8rem 0; }
.step-banner { background:#1a1008; border:1px solid #E85A4A44;
  border-left:3px solid #E85A4A; border-radius:6px; padding:1rem 1.2rem;
  margin:1rem 0; font-size:.83rem; color:#FCA5A5; }
.step-banner strong { color:#E85A4A; }

.grp-lbl { font-size:.68rem; letter-spacing:.18em; text-transform:uppercase;
  color:#3D6B45; margin:1rem 0 .5rem 0; display:flex; align-items:center; gap:.5rem; }
.grp-lbl::after { content:''; flex:1; height:1px; background:#1a3020; }

[data-testid="stExpander"] { background:#0d1a10 !important; border:1px solid #1a3020 !important;
  border-radius:8px !important; margin-bottom:.7rem !important; }
[data-testid="stExpander"] summary { font-family:'Outfit',sans-serif; font-weight:500;
  font-size:.92rem; color:#8BB888 !important; letter-spacing:.06em;
  text-transform:uppercase; padding:.85rem 1.2rem !important; }
[data-testid="stExpander"] summary:hover { color:#A8D5A2 !important; }

.stDownloadButton button { background:transparent !important;
  border:1px solid #A8D5A266 !important; color:#A8D5A2 !important;
  font-family:'JetBrains Mono',monospace !important; font-size:.76rem !important;
  letter-spacing:.12em !important; text-transform:uppercase !important;
  border-radius:4px !important; padding:.5rem 1.2rem !important; }
.stDownloadButton button:hover { background:#A8D5A211 !important; border-color:#A8D5A2AA !important; }
</style>
""", unsafe_allow_html=True)

# ─── CALCULATION LOGIC ────────────────────────────────────────────────────────

REF_DATE = date(2026, 3, 31)
APR_BASE = date(2026, 4, 1)
MAY_BASE = date(2026, 5, 1)


def parse_series(series: str):
    """
    Return (bond_type, rates_list) where bond_type is 'normal','step2','step3'
    and rates_list is list of floats (e.g. [0.09] or [0.12, 0.09] or [0.12,0.09,0.07])
    """
    series = str(series).strip()
    pcts = re.findall(r'(\d{1,2}\.\d{2})%', series)
    if not pcts:
        pcts = re.findall(r'(\d{1,2}(?:\.\d+)?)%', series)

    rates = [float(p) / 100 for p in pcts]

    if len(rates) == 0:
        return 'normal', [0.0]
    elif len(rates) == 1:
        return 'normal', rates
    elif len(rates) == 2:
        return 'step2', rates
    else:
        return 'step3', rates


def calc_remaining_coupons(maturity: date) -> float:
    """Validated formula: months from Apr/May 2026 base to maturity ÷ 6"""
    base = APR_BASE if maturity.day >= 15 else MAY_BASE
    months = (maturity.year - base.year) * 12 + (maturity.month - base.month)
    return round(months / 6, 2)


def calc_coupon_rate_from_series(series: str) -> float:
    """Extract current (final/active) coupon rate from series string."""
    bond_type, rates = parse_series(series)
    return rates[-1] if rates else 0.0


def process_row(row: dict) -> dict:
    """
    Given a row with Maturity Date, ISIN, Series, Face Value,
    calculate all derived columns.
    """
    mat_raw = row.get('Maturity Date')
    if isinstance(mat_raw, str):
        for fmt in ['%d-%b-%y', '%d-%b-%Y', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
            try:
                mat = datetime.strptime(mat_raw.strip(), fmt).date()
                break
            except:
                pass
        else:
            mat = None
    elif isinstance(mat_raw, (datetime,)):
        mat = mat_raw.date()
    elif isinstance(mat_raw, date):
        mat = mat_raw
    elif pd.notna(mat_raw):
        try:
            mat = pd.to_datetime(mat_raw).date()
        except:
            mat = None
    else:
        mat = None

    series = str(row.get('Series', ''))
    face   = float(str(row.get('Face Value (Rs Mn)', 0)).replace(',', '')) if pd.notna(row.get('Face Value (Rs Mn)')) else 0.0

    bond_type, rates = parse_series(series)
    current_rate     = rates[-1] if rates else 0.0

    remaining   = calc_remaining_coupons(mat) if mat else None
    semi_coupon = round(face * current_rate / 2, 5) if face and current_rate else None
    total_pay   = round(semi_coupon * remaining, 4) if semi_coupon and remaining else None

    if bond_type == 'normal':
        coupon_rate_str = f"{current_rate*100:.2f}%"
    else:
        coupon_rate_str = '/'.join(f"{r*100:.2f}%" for r in rates)

    return {
        'Maturity Date':              mat.strftime('%d-%b-%y') if mat else str(mat_raw),
        'ISIN':                       row.get('ISIN', ''),
        'Series':                     series,
        'Face Value (Rs Mn)':         face,
        'Coupon Rate':                coupon_rate_str,
        'Current Rate':               current_rate,
        'Remaining Coupons':          remaining,
        'Semiannual Coupon Payment':  semi_coupon,
        'Total Payment Until Maturity': total_pay,
        'Bond Type':                  bond_type,
        'All Rates':                  rates,
        '_mat':                       mat,
    }


def parse_uploaded_file(uploaded_file):
    """
    Robustly parse Excel, CSV with potential header noise.
    Finds the row containing the 4 key columns and reads from there.
    """
    name = uploaded_file.name.lower()
    raw_bytes = uploaded_file.read()

    REQUIRED = ['maturity date', 'isin', 'series', 'face value']

    def find_header_row(df_raw):
        for i, row in df_raw.iterrows():
            vals = [str(v).lower().strip() for v in row.values]
            matches = sum(any(req in v for v in vals) for req in REQUIRED)
            if matches >= 3:
                return i
        return None

    if name.endswith('.csv'):
        df_raw = pd.read_csv(io.BytesIO(raw_bytes), header=None)
        hrow   = find_header_row(df_raw)
        if hrow is not None:
            df = pd.read_csv(io.BytesIO(raw_bytes), skiprows=hrow)
        else:
            df = pd.read_csv(io.BytesIO(raw_bytes))

    elif name.endswith(('.xlsx', '.xls')):
        df_raw = pd.read_excel(io.BytesIO(raw_bytes), header=None)
        hrow   = find_header_row(df_raw)
        if hrow is not None:
            df = pd.read_excel(io.BytesIO(raw_bytes), skiprows=hrow)
        else:
            df = pd.read_excel(io.BytesIO(raw_bytes))

    elif name.endswith('.pdf'):
        return None, "pdf"
    else:
        return None, "unsupported"

    col_map = {}
    mapped_targets = set()
    for col in df.columns:
        cl = str(col).lower().strip()
        target = None
        if 'maturity' in cl or ('date' in cl and 'mat' in cl):
            target = 'Maturity Date'
        elif cl == 'isin' or 'isin' in cl:
            target = 'ISIN'
        elif 'series' in cl:
            target = 'Series'
        elif 'face' in cl or ('value' in cl and 'face' in cl):
            target = 'Face Value (Rs Mn)'
        
        if target and target not in mapped_targets:
            col_map[col] = target
            mapped_targets.add(target)
    
    df.rename(columns=col_map, inplace=True)

    if 'Maturity Date' in df.columns:
        df = df[df['Maturity Date'].notna()]
        df = df[df['Maturity Date'].astype(str).str.strip() != '']
        df = df[df['Maturity Date'].astype(str).str.strip().str.lower() != 'maturity date']

    return df, "ok"


def extract_pdf_directly(pdf_bytes: bytes):
    """Extract bond data directly from PDF using pdfplumber (no AI needed)."""
    import pdfplumber
    import io
    
    records = []
    
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            # Try to extract tables from the page
            tables = page.extract_tables()
            
            if not tables:
                continue
            
            for table in tables:
                if not table:
                    continue
                
                # Find header row by looking for key column names
                header_row_idx = None
                for idx, row in enumerate(table):
                    row_lower = [str(cell).lower().strip() if cell else '' for cell in row]
                    if any('maturity' in cell for cell in row_lower) and \
                       any('isin' in cell for cell in row_lower):
                        header_row_idx = idx
                        break
                
                if header_row_idx is None:
                    # Try to infer header as first row if it looks like headers
                    if table[0]:
                        header_row_idx = 0
                    else:
                        continue
                
                # Map column indices to our required fields
                header = table[header_row_idx]
                col_map = {}
                
                for col_idx, cell in enumerate(header):
                    if cell is None:
                        continue
                    cell_lower = str(cell).lower().strip()
                    
                    if 'maturity' in cell_lower or ('date' in cell_lower and 'mat' in cell_lower):
                        col_map['maturity_date'] = col_idx
                    elif 'isin' in cell_lower:
                        col_map['isin'] = col_idx
                    elif 'series' in cell_lower:
                        col_map['series'] = col_idx
                    elif 'face' in cell_lower or ('value' in cell_lower and 'face' in cell_lower):
                        col_map['face_value'] = col_idx
                
                # Extract data rows (skip header and empty rows)
                for row_idx in range(header_row_idx + 1, len(table)):
                    row = table[row_idx]
                    
                    # Skip empty or incomplete rows
                    if not row or all(cell is None or str(cell).strip() == '' for cell in row):
                        continue
                    
                    # Try to extract required fields
                    try:
                        record = {}
                        
                        if 'maturity_date' in col_map:
                            record['Maturity Date'] = row[col_map['maturity_date']]
                        if 'isin' in col_map:
                            record['ISIN'] = row[col_map['isin']]
                        if 'series' in col_map:
                            record['Series'] = row[col_map['series']]
                        if 'face_value' in col_map:
                            fv = row[col_map['face_value']]
                            # Clean up face value (remove commas, convert to float)
                            if fv:
                                fv_str = str(fv).replace(',', '').strip()
                                try:
                                    record['Face Value (Rs Mn)'] = float(fv_str)
                                except:
                                    record['Face Value (Rs Mn)'] = fv
                        
                        # Only add if we have at least Maturity Date
                        if 'Maturity Date' in record and record['Maturity Date']:
                            records.append(record)
                    except Exception as e:
                        continue
    
    return records


# ─── EXCEL EXPORT ─────────────────────────────────────────────────────────────

def build_excel(results: list) -> bytes:
    wb  = Workbook()

    DARK  = "1A2E1A"
    MID   = "2A4A30"
    LIGHT = "A8D5A2"
    WARN  = "E8A44A"
    RED   = "E85A4A"
    WHITE = "FFFFFF"
    ALT1  = "0F1E14"
    ALT2  = "0D1A10"
    YBG   = "2A1F0A"
    RBGC  = "2A0F0A"

    def s(style='thin', color="2A4A30"):
        return Side(style=style, color=color)
    def tb():
        return Border(left=s(), right=s(), top=s(), bottom=s())
    def mb():
        return Border(left=s('medium', DARK), right=s('medium', DARK),
                      top=s('medium', DARK), bottom=s('medium', DARK))

    normal = [r for r in results if r['Bond Type'] == 'normal']
    step2  = [r for r in results if r['Bond Type'] == 'step2']
    step3  = [r for r in results if r['Bond Type'] == 'step3']

    sheet_data = [("All Bonds", results), ("Normal Bonds", normal)]
    if step2: sheet_data.append(("2-Step Bonds", step2))
    if step3: sheet_data.append(("3-Step Bonds", step3))

    first = True
    for sheet_name, data in sheet_data:
        if first:
            ws = wb.active
            ws.title = sheet_name
            first = False
        else:
            ws = wb.create_sheet(sheet_name)

        ws.merge_cells('A1:I1')
        c = ws['A1']
        c.value = f"Treasury Bonds Outstanding — As at 31 March 2026 ({sheet_name})"
        c.font = Font(name='Arial', bold=True, size=12, color=LIGHT)
        c.fill = PatternFill('solid', fgColor=DARK)
        c.alignment = Alignment(horizontal='center', vertical='center')
        ws.row_dimensions[1].height = 26

        if sheet_name != "Normal Bonds" and (step2 or step3):
            ws.merge_cells('A2:I2')
            c = ws['A2']
            stepped = [r for r in data if r['Bond Type'] != 'normal']
            if stepped and sheet_name == "All Bonds":
                c.value = (f"⚠  {len(step2)} two-step bond(s) and {len(step3)} three-step bond(s) flagged. "
                           f"Calculations use current/final coupon rate only — verify step dates.")
            elif sheet_name in ("2-Step Bonds", "3-Step Bonds"):
                c.value = "⚠  Stepped coupon bonds — calculations use current/final rate only. Step dates required for full accuracy."
            c.font = Font(name='Arial', size=9, color="FCD34D")
            c.fill = PatternFill('solid', fgColor="1A1208")
            c.alignment = Alignment(horizontal='center', vertical='center')
            ws.row_dimensions[2].height = 18
            hdr_row = 3
        else:
            hdr_row = 2

        headers = ["Maturity Date", "ISIN", "Series", "Face Value (Rs Mn)",
                   "Coupon Rate", "Bond Type", "Remaining Coupons",
                   "Semiannual Coupon Payment", "Total Payment Until Maturity"]

        ws.row_dimensions[hdr_row].height = 32
        for ci, h in enumerate(headers, 1):
            c = ws.cell(row=hdr_row, column=ci, value=h)
            c.font = Font(name='Arial', bold=True, size=9, color=WHITE)
            c.fill = PatternFill('solid', fgColor=MID)
            c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            c.border = tb()

        for ri, row in enumerate(data):
            er  = ri + hdr_row + 1
            bt  = row['Bond Type']
            bg  = YBG if bt == 'step2' else (RBGC if bt == 'step3' else (ALT1 if ri % 2 == 0 else ALT2))
            fc  = WARN if bt == 'step2' else (RED if bt == 'step3' else WHITE)
            fill = PatternFill('solid', fgColor=bg)

            vals = [
                row['Maturity Date'], row['ISIN'], row['Series'],
                row['Face Value (Rs Mn)'], row['Coupon Rate'],
                {'normal':'Normal','step2':'2-Step ⚠','step3':'3-Step ⚠⚠'}.get(bt, bt),
                row['Remaining Coupons'],
                row['Semiannual Coupon Payment'],
                row['Total Payment Until Maturity'],
            ]
            for ci, val in enumerate(vals, 1):
                c = ws.cell(row=er, column=ci, value=val)
                c.fill = fill
                c.border = tb()
                c.font = Font(name='Arial', size=9, color=fc)
                if ci == 4:
                    c.number_format = '#,##0.00'
                    c.alignment = Alignment(horizontal='right')
                elif ci == 5:
                    c.alignment = Alignment(horizontal='center')
                elif ci == 7:
                    c.number_format = '0.00'
                    c.alignment = Alignment(horizontal='center')
                elif ci in (8, 9):
                    c.number_format = '#,##0.000'
                    c.alignment = Alignment(horizontal='right')
                else:
                    c.alignment = Alignment(horizontal='center' if ci == 1 else 'left')

        tr = hdr_row + len(data) + 1
        ws.merge_cells(f'A{tr}:C{tr}')
        c = ws.cell(row=tr, column=1, value="TOTAL")
        c.font = Font(name='Arial', bold=True, size=9, color=LIGHT)
        c.fill = PatternFill('solid', fgColor=DARK)
        c.alignment = Alignment(horizontal='center')
        c.border = mb()

        for ci, col_idx in [(4, 4), (8, 8), (9, 9)]:
            cl = get_column_letter(ci)
            c = ws.cell(row=tr, column=ci)
            c.value = f'=SUM({cl}{hdr_row+1}:{cl}{tr-1})'
            c.font = Font(name='Arial', bold=True, size=9, color=LIGHT)
            c.fill = PatternFill('solid', fgColor=DARK)
            c.border = mb()
            c.alignment = Alignment(horizontal='right')
            c.number_format = '#,##0.00' if ci == 4 else '#,##0.000'

        for ci in (5, 6, 7):
            c = ws.cell(row=tr, column=ci)
            c.value = ''
            c.fill = PatternFill('solid', fgColor=DARK)
            c.border = mb()

        for ci, w in enumerate([13, 18, 24, 16, 20, 12, 14, 22, 24], 1):
            ws.column_dimensions[get_column_letter(ci)].width = w

        ws.freeze_panes = f'A{hdr_row+1}'

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ─── DASHBOARD RENDER ─────────────────────────────────────────────────────────

def make_table(rows, show_step_col=False):
    cols = ["ISIN", "Series", "Maturity Date", "Face Value (Rs Mn)",
            "Coupon Rate", "Remaining Coupons", "Semiannual Coupon Payment",
            "Total Payment Until Maturity"]
    if show_step_col:
        cols = ["Bond Type"] + cols

    hdr = "".join(
        f'<th class="num">{c}</th>' if c in ("Face Value (Rs Mn)", "Semiannual Coupon Payment",
                                             "Total Payment Until Maturity", "Remaining Coupons")
        else f'<th>{c}</th>' for c in cols
    )

    body = ""
    for r in rows:
        bt = r['Bond Type']
        row_cls = ' class="step-row"' if bt != 'normal' else ''
        body += f"<tr{row_cls}>"
        for c in cols:
            v = r.get(c, '')
            if c == "Bond Type":
                badge = {'normal':'<span class="badge bg">Normal</span>',
                         'step2': '<span class="badge bw">2-Step ⚠</span>',
                         'step3': '<span class="badge br">3-Step ⚠⚠</span>'}.get(bt, bt)
                body += f'<td>{badge}</td>'
            elif c == "ISIN":
                body += f'<td class="mono">{v}</td>'
            elif c == "Maturity Date":
                body += f'<td class="dt">{v}</td>'
            elif c in ("Face Value (Rs Mn)", "Semiannual Coupon Payment", "Total Payment Until Maturity"):
                try:
                    body += f'<td class="amt">{float(v):,.3f}</td>'
                except:
                    body += f'<td class="amt">{v}</td>'
            elif c == "Remaining Coupons":
                try:
                    body += f'<td class="amt">{float(v):.2f}</td>'
                except:
                    body += f'<td class="amt">{v}</td>'
            elif c == "Coupon Rate" and bt != 'normal':
                body += f'<td class="warn">{v}</td>'
            else:
                body += f'<td>{v}</td>'
        body += "</tr>"

    total_pay = sum(r.get('Total Payment Until Maturity') or 0 for r in rows)
    n = len(rows)
    ncols = len(cols)
    foot = f'<td colspan="{ncols-1}">Total · {n} bond{"s" if n!=1 else ""}</td><td class="ta">{total_pay:,.3f}</td>'

    return f"""
<div class="tbl-wrap">
<table class="tbl">
<thead><tr>{hdr}</tr></thead>
<tbody>{body}</tbody>
<tfoot><tr>{foot}</tr></tfoot>
</table>
</div>"""


def render_dashboard(results: list, key_suffix: str = "xl"):
    normal = [r for r in results if r['Bond Type'] == 'normal']
    step2  = [r for r in results if r['Bond Type'] == 'step2']
    step3  = [r for r in results if r['Bond Type'] == 'step3']
    stepped = step2 + step3

    total_pay  = sum(r.get('Total Payment Until Maturity') or 0 for r in results)
    total_face = sum(r.get('Face Value (Rs Mn)') or 0 for r in results)
    n_stepped  = len(stepped)
    n_normal   = len(normal)

    if stepped:
        types = []
        if step2: types.append(f"<strong>{len(step2)} two-step</strong>")
        if step3: types.append(f"<strong>{len(step3)} three-step</strong>")
        st.markdown(f"""
        <div class="step-banner">
          ⚠ &nbsp; {' and '.join(types)} bond{'s' if n_stepped>1 else ''} detected in this file.
          These bonds have <strong>multiple coupon rates</strong> — calculations use the <strong>current/final rate only</strong>.
          Step dates are required for full accuracy. They are flagged separately below.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-row">
      <div class="mc">
        <div class="lbl">Total Bonds</div>
        <div class="val">{len(results)}</div>
        <div class="sub">{n_normal} normal · {n_stepped} stepped</div>
      </div>
      <div class="mc">
        <div class="lbl">Total Face Value</div>
        <div class="val">Rs {total_face:,.0f}Mn</div>
        <div class="sub">Aggregate outstanding</div>
      </div>
      <div class="mc">
        <div class="lbl">Total Coupon Payments</div>
        <div class="val">Rs {total_pay:,.0f}Mn</div>
        <div class="sub">Sum of total payments</div>
      </div>
      {"" if not stepped else f'<div class="mc warn"><div class="lbl">Stepped Bonds</div><div class="val">{n_stepped}</div><div class="sub">Require step-date verification</div></div>'}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Normal Bonds — Schedule by Maturity Month</div>', unsafe_allow_html=True)
    if normal:
        for r in normal:
            if r['_mat']:
                r['_month'] = r['_mat'].strftime('%B')
                r['_monthnum'] = r['_mat'].month
            else:
                r['_month'] = 'Unknown'
                r['_monthnum'] = 99

        months = sorted(set((r['_monthnum'], r['_month']) for r in normal), key=lambda x: x[0])

        for mnum, mname in months:
            month_rows = [r for r in normal if r['_monthnum'] == mnum]
            mtotal = sum(r.get('Total Payment Until Maturity') or 0 for r in month_rows)
            with st.expander(f"{mname}  ·  Rs {mtotal:,.0f} Mn  ·  {len(month_rows)} bond{'s' if len(month_rows)!=1 else ''}"):
                first_rows = [r for r in month_rows if r['_mat'] and r['_mat'].day == 1]
                fif_rows   = [r for r in month_rows if r['_mat'] and r['_mat'].day == 15]
                other_rows = [r for r in month_rows if r['_mat'] and r['_mat'].day not in (1, 15)]

                if first_rows:
                    st.markdown('<div class="grp-lbl"><span class="badge bg">1st</span></div>', unsafe_allow_html=True)
                    st.markdown(make_table(first_rows), unsafe_allow_html=True)
                if fif_rows:
                    st.markdown('<div class="grp-lbl"><span class="badge bb">15th</span></div>', unsafe_allow_html=True)
                    st.markdown(make_table(fif_rows), unsafe_allow_html=True)
                if other_rows:
                    st.markdown('<div class="grp-lbl"><span class="badge bw">Other Date</span></div>', unsafe_allow_html=True)
                    st.markdown(make_table(other_rows), unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box"><div class="ico">📋</div><p>No normal bonds found.</p></div>', unsafe_allow_html=True)

    if step2:
        st.markdown('<div class="sec-title" style="color:#E8A44A">2-Step Bonds ⚠</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="warn-box">
          These bonds have <strong>two coupon rates</strong> (e.g. 12.00%→09.00%).
          The calculations below use the <strong>current/final rate</strong> only.
          To calculate accurately, provide the step-down date so coupons at each rate can be counted separately.
        </div>
        """, unsafe_allow_html=True)
        st.markdown(make_table(step2, show_step_col=True), unsafe_allow_html=True)

    if step3:
        st.markdown('<div class="sec-title" style="color:#E85A4A">3-Step Bonds ⚠⚠</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="warn-box" style="border-left-color:#E85A4A;color:#FCA5A5">
          These bonds have <strong>three coupon rates</strong> and require both step dates for accurate calculation.
          Figures shown use the <strong>final/lowest rate</strong> only.
        </div>
        """, unsafe_allow_html=True)
        st.markdown(make_table(step3, show_step_col=True), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    xlsx = build_excel(results)
    st.download_button(
        label="⬇  Download Complete Excel",
        data=xlsx,
        file_name="T_Bonds_Calculated.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"dl_excel_{key_suffix}"
    )


# ─── MAIN UI ──────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="page-header">
  <div class="sub">Central Bank of Sri Lanka · Fixed Income Operations</div>
  <h1>Bond Maturity and Coupon Schedules</h1>
  <div class="ts">Upload a file with Maturity Date, ISIN, Series, Face Value → all other columns calculated automatically</div>
</div>
""", unsafe_allow_html=True)

tab_xl, tab_csv, tab_pdf = st.tabs(["📊  Excel Upload", "📋  CSV Upload", "📄  PDF Upload"])

def handle_df(df):
    """Process a dataframe into results."""
    results = []
    for _, row in df.iterrows():
        try:
            r = process_row(row.to_dict())
            results.append(r)
        except Exception as e:
            st.warning(f"Skipped a row due to error: {e}")
    return results

with tab_xl:
    xl_file = st.file_uploader("Upload Excel file", type=["xlsx","xls"],
                                label_visibility="collapsed", key="xl_up")
    st.caption("Required columns: **Maturity Date**, **ISIN**, **Series**, **Face Value (Rs Mn)** · Extra columns/headers are ignored automatically")
    if xl_file:
        df, status = parse_uploaded_file(xl_file)
        if status == "ok" and df is not None:
            results = handle_df(df)
            if results:
                render_dashboard(results, key_suffix="xl")
            else:
                st.markdown('<div class="warn-box">⚠ No valid bond rows found. Check column names.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warn-box">⚠ Could not parse file: {status}</div>', unsafe_allow_html=True)

with tab_csv:
    csv_file = st.file_uploader("Upload CSV file", type=["csv"],
                                 label_visibility="collapsed", key="csv_up")
    st.caption("Required columns: **Maturity Date**, **ISIN**, **Series**, **Face Value (Rs Mn)** · Extra columns/headers are ignored automatically")
    if csv_file:
        df, status = parse_uploaded_file(csv_file)
        if status == "ok" and df is not None:
            results = handle_df(df)
            if results:
                render_dashboard(results, key_suffix="csv")
            else:
                st.markdown('<div class="warn-box">⚠ No valid bond rows found. Check column names.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warn-box">⚠ Could not parse file: {status}</div>', unsafe_allow_html=True)

with tab_pdf:
    st.markdown("""
    <div style="background:#0a1610;border:1px solid #1a3020;border-left:3px solid #A8D5A2;
    border-radius:6px;padding:.9rem 1.2rem;margin-bottom:1rem;font-size:.83rem;color:#A8D5A2">
      📄 &nbsp; Extract bond data from PDF tables automatically —
      works with settlement schedules, bond registers, Central Bank circulars, and term sheets.
    </div>
    """, unsafe_allow_html=True)
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"],
                                 label_visibility="collapsed", key="pdf_up")
    st.caption("Extracts Maturity Date, ISIN, Series, and Face Value from PDF tables")
    if pdf_file:
        cache_key = f"pdf_{pdf_file.name}_{pdf_file.size}"
        if cache_key not in st.session_state:
            with st.spinner("Extracting bond data from PDF…"):
                try:
                    bonds = extract_pdf_directly(pdf_file.read())
                    st.session_state[cache_key] = (bonds, None)
                except Exception as e:
                    st.session_state[cache_key] = (None, str(e))
        bonds, err = st.session_state[cache_key]
        if err:
            st.markdown(f'<div class="warn-box">⚠ Extraction error: {err}</div>', unsafe_allow_html=True)
        elif bonds:
            df_pdf = pd.DataFrame(bonds)
            results = handle_df(df_pdf)
            if results:
                st.success(f"✓ Extracted {len(results)} bonds from PDF")
                render_dashboard(results, key_suffix="pdf")
        else:
            st.markdown('<div class="warn-box">⚠ No bond data found in PDF.</div>', unsafe_allow_html=True)

if not (tab_xl or tab_csv or tab_pdf):
    st.markdown("""
    <div class="info-box" style="margin-top:2rem">
      <div class="ico">🏛️</div>
      <p>Upload an <strong>Excel</strong>, <strong>CSV</strong>, or <strong>PDF</strong> file above<br>
      with Maturity Date · ISIN · Series · Face Value</p>
    </div>
    """, unsafe_allow_html=True)