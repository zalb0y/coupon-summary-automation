# 📊 LSI Coupon Statistics Dashboard

Interactive dashboard untuk analisis statistik coupon LSI menggunakan Streamlit.

## 🎯 Features

- **📈 Interactive Line Chart** - Trend coupon usage per hari dengan data labels
- **📊 Data Table** - Tabel dengan kolom per tanggal di bawah chart
- **🔄 Pivot Table** - View data per toko dengan kolom per coupon
- **🔍 Dynamic Filters** - Filter by store, coupon, dan date range
- **💾 Export** - Download hasil analisis ke Excel atau CSV
- **📱 Responsive** - Berfungsi di desktop dan mobile

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/lsi-coupon-dashboard.git
cd lsi-coupon-dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
streamlit run app.py
```

Dashboard akan terbuka di browser: `http://localhost:8501`

## 📦 Deploy ke Streamlit Cloud

### Step 1: Push ke GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Deploy di Streamlit Cloud

1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Login dengan GitHub
3. Click **"New app"**
4. Pilih repository: `YOUR_USERNAME/lsi-coupon-dashboard`
5. Main file path: `app.py`
6. Click **"Deploy"**

Dashboard akan live dalam beberapa menit! 🎉

## 📊 Data Format

Upload file Excel (.xlsx) dengan kolom:

- `Corp` - Kode perusahaan
- `SaleDy` - Tanggal (format: YYYYMMDD)
- `StrCd` - Kode toko
- `StrNm` - Nama toko
- `PosNo` - Nomor POS
- `TrdNo` - Nomor transaksi
- `CancelFg` - Flag cancel
- `CpnNo` - Nomor coupon
- `CpnNm` - Nama coupon
- `Amt` - Amount
- `Qty` - Quantity (digunakan untuk analisis)
- `DcAmt` - Discount amount
- `LtvCardNo` - Loyalty card number

## 🎨 Dashboard Layout

### Sidebar
- 📂 File uploader
- 📅 Date range picker
- 🏪 Store filter (multiselect)
- 🎫 Coupon filter (keywords atau specific)

### Main Dashboard

**Tab 1: Line Chart & Table**
- Line chart dengan multiple lines per coupon
- Data labels di setiap point
- Legend di kanan
- Tabel data di bawah chart dengan kolom per tanggal

**Tab 2: Pivot Table**
- Struktur: `StrCd | StrNm | [Coupon Columns] | TOTAL`
- Grand total di baris terakhir
- Download CSV

**Tab 3: Data Detail**
- Raw data yang sudah difilter
- Sortable columns
- Download CSV

**Tab 4: Export**
- Excel multi-sheet export
- Individual CSV exports

## 🔧 Configuration

### Filter Modes

**Keywords Mode:**
- Default: `tm, new regis, dormant`
- Filter coupon yang mengandung kata kunci (case insensitive)

**Specific Coupons Mode:**
- Pilih coupon spesifik dari dropdown

### Customization

Edit `app.py` untuk customize:
- Colors: Line 161-162 (colors list)
- Chart height: Line 239 (height parameter)
- Table column widths: Line 217-218

## 📱 Screenshots

### Line Chart with Data Table
![Line Chart](docs/screenshot1.png)

### Pivot Table View
![Pivot Table](docs/screenshot2.png)

## 🛠️ Tech Stack

- **Streamlit** - Web framework
- **Pandas** - Data processing
- **Plotly** - Interactive charts
- **OpenPyXL** - Excel handling

## 📄 License

MIT License - feel free to use and modify

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

## 📧 Contact

Untuk pertanyaan atau bantuan, silakan buat issue di GitHub.

---

**Developed by Dafha**
