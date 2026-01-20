# 🚀 QUICK START - LSI Coupon Dashboard

## 📦 Files Yang Sudah Dibuat:

```
streamlit_app/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── DEPLOYMENT_GUIDE.md    # Step-by-step deployment
├── DATA_FORMAT.md         # Data format specification
└── .gitignore            # Git ignore file
```

---

## ⚡ 3 Steps untuk Deploy:

### 1️⃣ Upload ke GitHub

```bash
# Buat repository baru di GitHub
# Nama: lsi-coupon-dashboard

# Di terminal, masuk ke folder streamlit_app
cd streamlit_app

# Initialize git
git init
git add .
git commit -m "Initial commit: LSI Coupon Dashboard"

# Connect ke GitHub (ganti YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/lsi-coupon-dashboard.git
git branch -M main
git push -u origin main
```

### 2️⃣ Deploy di Streamlit Cloud

1. Buka: https://share.streamlit.io
2. Login dengan GitHub
3. Click **"New app"**
4. Settings:
   - Repository: `YOUR_USERNAME/lsi-coupon-dashboard`
   - Branch: `main`
   - Main file: `app.py`
5. Click **"Deploy"**

### 3️⃣ Done! 🎉

URL dashboard: `https://YOUR-APP-NAME.streamlit.app`

---

## 🧪 Test Locally Dulu (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py

# Buka browser: http://localhost:8501
```

---

## 📊 Cara Pakai Dashboard:

### Sidebar (Filters):
1. **Upload Excel** - File dengan format yang benar
2. **Date Range** - Pilih range tanggal
3. **Store Filter** - Select all atau pilih spesifik
4. **Coupon Filter** - Keywords (tm, new regis, dormant) atau specific

### Tabs:
- **Tab 1:** Line chart + data table
- **Tab 2:** Pivot table (StrCd | StrNm | Coupons | Total)
- **Tab 3:** Data detail (raw filtered data)
- **Tab 4:** Export (Excel multi-sheet atau CSV)

---

## ✅ Features:

✅ **Interactive line chart** dengan data labels
✅ **Data table** di bawah chart (aligned dengan tanggal)
✅ **Pivot table** format: Store × Coupon
✅ **Dynamic filters** yang sync sempurna
✅ **Export Excel** (multiple sheets) dan CSV
✅ **Metrics cards** (Total, Qty, Stores, Coupons)
✅ **Legend di kanan** untuk chart
✅ **Responsive** design

---

## 📝 File Format:

Excel harus punya kolom:
- `SaleDy` (YYYYMMDD format)
- `StrCd` (Store code)
- `StrNm` (Store name)
- `CpnNm` (Coupon name)
- `Qty` (Quantity - main metric)

Lihat **DATA_FORMAT.md** untuk detail lengkap.

---

## 🔧 Troubleshooting:

### "Module not found"
→ Check `requirements.txt` lengkap

### "File upload error"
→ Check file format Excel (.xlsx)

### "No data after filter"
→ Check CpnNm contains keywords

### "Chart not showing"
→ Check data has 2+ dates

Lihat **DEPLOYMENT_GUIDE.md** untuk troubleshooting lengkap.

---

## 📚 Documentation:

- **README.md** - Overview & features
- **DEPLOYMENT_GUIDE.md** - Complete deployment steps
- **DATA_FORMAT.md** - Data specification

---

## 🎯 Next Steps:

1. ✅ Test locally
2. ✅ Push to GitHub
3. ✅ Deploy to Streamlit Cloud
4. ✅ Share URL dengan team
5. ✅ Monitor & update as needed

---

**Happy Deploying! 🚀**
