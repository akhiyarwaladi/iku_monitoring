# Dokumentasi Sistem Visualisasi IKU Fakultas Sains & Teknologi

## Rangkuman Penelusuran

### 1. Analisis Struktur Data Excel

Setelah membaca dengan detail semua file Excel, ditemukan struktur sebagai berikut:

#### Struktur File
- **Baris 0**: Judul IKU (deskripsi indikator)
- **Baris 1**: Header kolom
- **Baris 2 dst**: Data aktual

#### File Penyebut (Total Dosen)
- **Jumlah**: 206 dosen total di Fakultas Sains & Teknologi
- **Kolom Utama**:
  - Nama
  - NIP
  - Program Studi
  - Jurusan
  - Fakultas
  - Status Keaktifan Pegawai
  - Status Kepegawaian

#### File Pembilang (Dosen yang Memenuhi Kriteria)
Struktur berbeda untuk setiap IKU:

**IKU 31 (Tridharma di PT Lain)**: 123 dosen
- Kolom: Nama, NIP, Jenis, Kegiatan, Tanggal Selesai, Lokasi, Jumlah Anggota

**IKU 33 (Membimbing Mahasiswa Luar Prodi)**: 56 dosen
- 11 kolom termasuk NIP dan Semester

**IKU 41 (Sertifikat DUDI)**: 33 dosen
- 11 kolom termasuk NIP dan Gelar

### 2. Program Studi di Fakultas Sains & Teknologi

Dari analisis data ditemukan 15 program studi:
1. Matematika
2. Biologi
3. Fisika
4. Kimia
5. Teknik Geofisika
6. Teknik Geologi
7. Teknik Kimia
8. Teknik Lingkungan
9. Teknik Pertambangan
10. Teknik Sipil
11. Sistem Informasi
12. Informatika
13. Teknik Elektro
14. Analis Kimia (D3)
15. Kimia Industri (D3)

### 3. Standar Visualisasi Jurnal Internasional

Berdasarkan riset dari sumber-sumber bereputasi internasional:

#### Prinsip Utama (Ten Guidelines for Effective Data Visualization)
1. **Maximize Data-Ink Ratio**: Minimalkan elemen dekoratif, maksimalkan representasi data
2. **Colorblind-Friendly Palettes**: Gunakan palette dari ColorBrewer2.org
3. **Avoid Red-Green Combinations**: Hindari kombinasi warna yang sulit dibedakan oleh colorblind
4. **Clear Typography**: Font yang jelas dan readable
5. **Consistent Styling**: Konsistensi dalam semua visualisasi

#### Spesifikasi Teknis Publikasi
- **Font Size**: 9pt untuk body text, 10-12pt untuk labels
- **Font Family**: Arial, Helvetica (sans-serif untuk kemudahan baca)
- **Line Width**: 0.5-0.75pt untuk axes dan borders
- **Resolution**: Minimal 300 DPI, optimal 600 DPI
- **Figure Size**:
  - Single column: ~3.5 inch width
  - Double column: ~7 inch width
- **Grid Lines**: Subtle, dotted/dashed, alpha < 0.5
- **Color Palette**: Maximum 8 distinguishable colors
- **Legend**: Frame dengan alpha 0.9-0.95, minimal padding

#### Referensi Sumber
1. [Ten Guidelines for Effective Data Visualization in Scientific Publications](https://www.sciencedirect.com/science/article/abs/pii/S1364815210003270) - Environmental Modelling & Software
2. [Making Publication-Quality Figures with Matplotlib](https://www.jesshamrick.com/post/2016-04-13-reproducible-plots/) - Jessica Hamrick
3. [Nature Cell Biology Practice-Oriented Checklist](https://phys.org/news/2025-07-checklist-scientific-visualization.html) - Dr. Helena Jambor, 2025
4. [ColorBrewer2.org](http://colorbrewer2.org) - Colorblind-safe color schemes

### 4. Metodologi Perhitungan IKU

Formula yang digunakan:
```
Persentase IKU per Prodi = (Pembilang / Penyebut) × 100%

Dimana:
- Pembilang = Jumlah dosen yang memenuhi kriteria IKU di prodi tersebut
- Penyebut = Total dosen di prodi tersebut
```

**Teknik Matching Data**:
- Join antara file pembilang dan penyebut menggunakan kolom NIP
- Agregasi per Program Studi
- Handling missing values (fillna dengan 0)

### 5. Hasil Visualisasi IKU 31

**Pencapaian Keseluruhan**: 59.71% (123/206 dosen)

**Top 5 Program Studi**:
1. Matematika: 90.91% (10/11 dosen)
2. Fisika: 87.50% (14/16 dosen)
3. Informatika: 85.71% (6/7 dosen)
4. Biologi: 76.47% (13/17 dosen)
5. Teknik Lingkungan: 61.54% (8/13 dosen)

**Bottom 5 Program Studi**:
1. Analis Kimia (D3): 25.00% (2/8 dosen)
2. Teknik Elektro: 25.00% (5/20 dosen)
3. Teknik Geofisika: 33.33% (3/9 dosen)
4. Teknik Kimia: 40.00% (6/15 dosen)
5. Teknik Sipil: 41.18% (7/17 dosen)

---

## Arsitektur Sistem

### Prinsip Desain

**PENTING**: Semua script harus terpusat dalam satu file utama untuk:
- ✅ Kemudahan maintenance
- ✅ Konsistensi konfigurasi
- ✅ Menghindari duplikasi kode
- ✅ Version control yang lebih baik
- ✅ Debugging yang lebih mudah

### Struktur File

```
iku_monitoring/
├── CLAUDE.md                              # Dokumentasi ini
├── main_visualize_iku.py                  # ⭐ SCRIPT UTAMA (SATU-SATUNYA)
├── monitoring-iku-31-pembilang.xlsx
├── monitoring-iku-31-penyebut.xlsx
├── monitoring-iku-33-pembilang.xlsx
├── monitoring-iku-33-penyebut.xlsx
├── monitoring-iku-41-pembilang.xlsx
├── monitoring-iku-41-penyebut.xlsx
└── output/                                # Folder hasil visualisasi
    ├── IKU_31_per_prodi_horizontal.png
    ├── IKU_31_per_prodi_vertical.png
    ├── IKU_33_per_prodi_horizontal.png
    ├── IKU_33_per_prodi_vertical.png
    ├── IKU_41_per_prodi_horizontal.png
    ├── IKU_41_per_prodi_vertical.png
    └── IKU_summary_dashboard.png
```

### Arsitektur Script Utama

File: `main_visualize_iku.py`

```
┌─────────────────────────────────────────┐
│   KONFIGURASI GLOBAL                    │
│   - Publication settings                │
│   - Color palettes                      │
│   - Path configurations                 │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│   FUNGSI UTILITY                        │
│   - read_iku_data()                     │
│   - process_iku_31()                    │
│   - process_iku_33()                    │
│   - process_iku_41()                    │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│   FUNGSI VISUALISASI                    │
│   - create_horizontal_bar_chart()       │
│   - create_vertical_bar_chart()         │
│   - create_summary_dashboard()          │
│   - create_trend_analysis()             │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│   MAIN FUNCTION                         │
│   - Orchestrate semua proses            │
│   - Error handling                      │
│   - Logging                             │
└─────────────────────────────────────────┘
```

---

## Panduan Penggunaan

### Menjalankan Visualisasi

```bash
# Dari terminal/command prompt
cd "C:\Users\MyPC PRO\Documents\iku_monitoring"
python main_visualize_iku.py
```

### Opsi Konfigurasi

Edit bagian `CONFIG` di file `main_visualize_iku.py`:

```python
CONFIG = {
    'dpi': 600,                    # Resolution output
    'font_size': 9,                # Font size
    'show_target_line': True,      # Tampilkan garis target
    'target_values': {             # Target untuk setiap IKU
        '31': 60,
        '33': 50,
        '41': 30
    },
    'output_dir': 'output',        # Folder output
    'color_palette': 'colorblind'  # Palette: colorblind, vibrant, pastel
}
```

### Modifikasi Visualisasi

Semua fungsi visualisasi ada di satu file. Untuk memodifikasi:

1. Cari fungsi yang relevan (misal: `create_horizontal_bar_chart()`)
2. Edit parameter styling sesuai kebutuhan
3. Jalankan ulang script

**JANGAN** membuat file Python baru. Semua modifikasi dilakukan dalam `main_visualize_iku.py`.

---

## Troubleshooting

### Error: 'Program Studi' not found
**Penyebab**: File pembilang tidak memiliki kolom Program Studi
**Solusi**: Script otomatis melakukan join dengan file penyebut berdasarkan NIP

### Error: Missing NIP in pembilang
**Penyebab**: Data di file Excel tidak lengkap
**Solusi**: Periksa konsistensi NIP di kedua file (pembilang dan penyebut)

### Visualisasi terlalu ramai
**Solusi**: Edit `CONFIG['font_size']` atau `figsize` di fungsi visualisasi

### Warna tidak sesuai
**Solusi**: Edit `PRODI_COLORS` atau `COLORS` dictionary di bagian konfigurasi

---

## Best Practices

### 1. Jangan Membuat Script Baru
❌ **SALAH**: Membuat `fix_iku_33.py`, `update_charts.py`, `new_visualization.py`
✅ **BENAR**: Edit `main_visualize_iku.py` dan tambahkan fungsi baru di dalamnya

### 2. Gunakan Fungsi Modular
```python
# Setiap IKU punya fungsi processing tersendiri dalam file yang sama
def process_iku_31(df_pembilang, df_penyebut):
    # Logic khusus IKU 31
    pass

def process_iku_33(df_pembilang, df_penyebut):
    # Logic khusus IKU 33
    pass
```

### 3. Konsistensi Styling
Semua chart harus menggunakan konfigurasi dari `CONFIG` dictionary.

### 4. Documentation
Setiap fungsi harus memiliki docstring yang jelas:
```python
def create_horizontal_bar_chart(data, iku_number, title, target=None):
    """
    Membuat horizontal bar chart berkualitas publikasi

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    iku_number : str
        Nomor IKU (31, 33, atau 41)
    title : str
        Judul chart
    target : float, optional
        Nilai target untuk garis horizontal

    Returns:
    --------
    str : Path file output
    """
```

### 5. Error Handling
Gunakan try-except yang informatif:
```python
try:
    data = process_iku_31(pembilang, penyebut)
except Exception as e:
    print(f"❌ Error processing IKU 31: {e}")
    logging.error(f"IKU 31 error: {e}", exc_info=True)
```

---

## Roadmap Pengembangan

### Phase 1 (Completed) ✅
- [x] Riset standar visualisasi internasional
- [x] Analisis struktur data Excel
- [x] Implementasi visualisasi IKU 31
- [x] Setup konfigurasi publikasi

### Phase 2 (In Progress) 🔄
- [ ] Fix visualisasi IKU 33
- [ ] Fix visualisasi IKU 41
- [ ] Implementasi dashboard summary yang lengkap
- [ ] Validasi konsistensi warna

### Phase 3 (Planned) 📋
- [ ] Trend analysis (jika ada data historis)
- [ ] Export ke berbagai format (PDF, SVG, EPS)
- [ ] Automated reporting
- [ ] Interactive dashboard (Plotly/Dash)

---

## Kontak & Support

**Tim IKU Fakultas Sains & Teknologi**
Universitas Jambi

**Tools & Dependencies**:
- Python 3.8+
- pandas
- matplotlib
- seaborn
- openpyxl

**Last Updated**: 2025-12-23
**Version**: 1.0
