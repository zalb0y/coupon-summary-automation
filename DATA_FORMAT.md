# 📊 Sample Data Guide

## Excel File Format

Your Excel file should have these columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Corp | Text | Company code | LSI |
| SaleDy | Integer | Sale date (YYYYMMDD) | 20260118 |
| StrCd | Integer | Store code | 6001 |
| StrNm | Text | Store name | PASAR REBO |
| PosNo | Integer | POS number | 1 |
| TrdNo | Integer | Transaction number | 12345 |
| CancelFg | Integer | Cancel flag (0/1) | 0 |
| CpnNo | Integer | Coupon number | 101 |
| CpnNm | Text | Coupon name | MKT_006 TM POT 3K |
| Amt | Integer | Amount | 30000 |
| **Qty** | Float | **Quantity (main metric)** | **5.0** |
| DcAmt | Integer | Discount amount | 150000 |
| LtvCardNo | Float | Loyalty card number | (optional) |

## Important Notes

### 1. Date Format
- **SaleDy** must be in format: `YYYYMMDD`
- Example: January 18, 2026 = `20260118`
- The app will auto-convert to datetime

### 2. Coupon Names (CpnNm)
The default filter looks for coupons containing:
- `tm` (case insensitive)
- `new regis` (case insensitive)
- `dormant` (case insensitive)

Examples that will be included:
- ✅ MKT_006 TM POT 3K
- ✅ MKT_001 NEW REGIS POT 20.5K
- ✅ MKT_002 DORMANT PROF 20K MIN 300K
- ✅ MKT_006 TM POT 5K MIN 100K

### 3. Required Columns
At minimum, you need:
- `SaleDy` (date)
- `StrCd` (store code)
- `StrNm` (store name)
- `CpnNm` (coupon name)
- `Qty` (quantity - this is what gets analyzed)

### 4. Store Codes
Standard store codes (StrCd):
- 6001 - PASAR REBO
- 6002 - SIDOARJO, SURABAYA
- 6003 - KELAPA GADING
- 6004 - MERUYA
- 6005 - BANDUNG
- ... (up to 6039)

## Sample Data Structure

```
Corp | SaleDy   | StrCd | StrNm      | CpnNm              | Qty
-----|----------|-------|------------|--------------------|----- 
LSI  | 20260118 | 6001  | PASAR REBO | MKT_006 TM POT 3K | 5.0
LSI  | 20260118 | 6002  | SIDOARJO   | MKT_001 NEW REGIS | 1.0
LSI  | 20260119 | 6001  | PASAR REBO | MKT_002 DORMANT   | 3.0
```

## Creating Test Data

If you need to create test data for development:

```python
import pandas as pd
from datetime import datetime, timedelta

# Generate sample data
data = {
    'Corp': ['LSI'] * 100,
    'SaleDy': [20260118] * 50 + [20260119] * 50,
    'StrCd': [6001, 6002, 6003] * 33 + [6001],
    'StrNm': ['PASAR REBO', 'SIDOARJO', 'KELAPA GADING'] * 33 + ['PASAR REBO'],
    'PosNo': range(1, 101),
    'TrdNo': range(1000, 1100),
    'CancelFg': [0] * 100,
    'CpnNo': [101, 102, 103] * 33 + [101],
    'CpnNm': ['MKT_006 TM POT 3K', 'MKT_001 NEW REGIS POT 20.5K', 'MKT_002 DORMANT PROF 20K'] * 33 + ['MKT_006 TM POT 3K'],
    'Amt': [30000] * 100,
    'Qty': [1.0, 2.0, 3.0] * 33 + [1.0],
    'DcAmt': [30000, 60000, 90000] * 33 + [30000],
    'LtvCardNo': [None] * 100
}

df = pd.DataFrame(data)
df.to_excel('sample_data.xlsx', index=False)
```

## Common Issues

### Issue: "KeyError: 'Qty'"
**Solution:** Make sure your Excel has a column named exactly `Qty` (case sensitive)

### Issue: "No data after filtering"
**Solution:** 
- Check if your CpnNm values contain the filter keywords
- Try selecting specific coupons instead of using keywords

### Issue: "Date parsing error"
**Solution:** Ensure SaleDy is in YYYYMMDD format (e.g., 20260118, not 2026-01-18)

### Issue: "Chart not showing"
**Solution:**
- Ensure you have at least 2 different dates
- Check that Qty values are numeric (not text)
- Verify you have at least 1 coupon after filtering

## Data Quality Tips

1. **Remove duplicates:**
   ```python
   df = df.drop_duplicates()
   ```

2. **Check for missing values:**
   ```python
   df.isnull().sum()
   ```

3. **Verify data types:**
   ```python
   df.dtypes
   ```

4. **Check date range:**
   ```python
   df['SaleDy'].min(), df['SaleDy'].max()
   ```

## Example Excel File

You can download a sample Excel file from:
- [Sample Data Template](https://github.com/YOUR_REPO/sample_data.xlsx)

Or use the data from your original file:
- `LSI_CouponStatistic20260119_143725.xlsx`
