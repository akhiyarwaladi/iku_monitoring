# IKU Monitoring - Fakultas Sains & Teknologi

Sistem visualisasi untuk monitoring Indikator Kinerja Utama (IKU) Fakultas Sains & Teknologi, Universitas Jambi.

## 🎯 Deskripsi

Project ini menghasilkan visualisasi berkualitas publikasi untuk 4 IKU utama:

- **IKU 31**: Dosen Tetap Berkualifikasi Akademik S3 dan Guru Besar yang Melakukan Kegiatan Tridharma di PT Lain
- **IKU 33**: Dosen yang Membimbing Mahasiswa Luar Program Studi
- **IKU 41**: Dosen Tetap yang Memiliki Sertifikat Kompetensi/Profesi dari DUDI
- **IKU 42**: Pengajar dari Kalangan Praktisi Profesional, Dunia Industri, dan Dunia Kerja

## ✨ Fitur

✅ **Modular & Maintainable** - Kode terorganisir dengan baik, mudah di-maintain
✅ **Publication Quality** - Visualisasi 300 DPI sesuai standar publikasi internasional
✅ **Dual Format Export** - PNG (300 DPI) dan SVG (vector)
✅ **Shared Utilities** - Fungsi-fungsi umum di-centralize, tidak ada duplikasi
✅ **Color-coded** - Warna berdasarkan jurusan untuk kemudahan identifikasi
✅ **Annotated Charts** - Bar charts dengan nama dosen untuk detail informasi
✅ **Configurable** - Semua styling constants terpusat di satu tempat

## 📁 Struktur Project

```
iku_monitoring/
├── README.md                          # Dokumentasi utama
├── CLAUDE.md                          # Dokumentasi teknis lengkap
│
├── generate_all.py                    # 🎯 MASTER SCRIPT - Run semua visualisasi
├── main_visualize_iku.py              # Main visualizations (summary per prodi)
├── visualization_config.py            # 🔧 Konfigurasi & utilities terpusat
│
├── breakdown/                         # Breakdown charts per IKU
│   ├── breakdown_utils.py             # 🔧 Shared utilities untuk breakdown
│   ├── iku_31_breakdown.py            # IKU 31: Tridharma di PT Lain
│   ├── iku_33_breakdown.py            # IKU 33: Bimbingan Luar Prodi
│   ├── iku_41_breakdown.py            # IKU 41: Sertifikat DUDI
│   └── iku_42_breakdown.py            # IKU 42: Praktisi Profesional
│
├── monitoring-iku-*.xlsx              # Data Excel
│
└── output/                            # Hasil visualisasi
    ├── png/                           # PNG files (300 DPI)
    └── svg/                           # SVG vector files
```

## 🚀 Instalasi

```bash
pip install pandas matplotlib seaborn openpyxl numpy
```

## 📊 Cara Penggunaan

### Generate SEMUA Visualisasi (Recommended)

```bash
python generate_all.py
```

Script ini akan generate:
- ✅ Main visualizations (horizontal & vertical bar charts)
- ✅ Summary dashboard
- ✅ Semua breakdown charts (IKU 31, 33, 41, 42)

**Output**: 14 charts (7 PNG + 7 SVG files)

### Generate Main Visualizations Saja

```bash
python main_visualize_iku.py
```

Output:
- IKU 31, 33, 41, 42: Horizontal & Vertical bar charts
- Summary dashboard

### Generate Breakdown Terpisah

```bash
python breakdown/iku_31_breakdown.py
python breakdown/iku_33_breakdown.py
python breakdown/iku_41_breakdown.py
python breakdown/iku_42_breakdown.py
```

## 🎨 Konfigurasi

Semua konfigurasi styling terpusat di `visualization_config.py`:

### Global Config
```python
CONFIG = {
    'dpi': 300,                      # Resolution
    'font_size': 9,                  # Base font size
    'export_png': True,              # Export PNG
    'export_svg': True,              # Export SVG
}
```

### Breakdown Styling
```python
BREAKDOWN_STYLE = {
    'prodi_label_size': 14,          # Program Studi labels
    'faculty_name_size': 12,         # Faculty names
    'bar_height': 0.7,               # Bar height
    'text_wrap_width': 60,           # Text wrapping
    'x_axis_multiplier': 1.3,        # X-axis expansion
}
```

## 📈 Output Charts

### Main Visualizations (per Prodi)
- `IKU_31_horizontal.png/svg` - Horizontal bar chart
- `IKU_31_vertical.png/svg` - Vertical bar chart
- `IKU_33_horizontal.png/svg`
- `IKU_33_vertical.png/svg`
- `IKU_41_horizontal.png/svg`
- `IKU_41_vertical.png/svg`
- `IKU_42_horizontal.png/svg`
- `IKU_42_vertical.png/svg`
- `IKU_summary_dashboard.png/svg` - Summary semua IKU

### Breakdown Charts (Detail)
- `IKU_31_breakdown_dosen_annotated.png/svg` - Dosen aktif dengan nama
- `IKU_31_breakdown_statistik.png/svg` - Top kegiatan & jenis
- `IKU_33_breakdown_statistik.png/svg` - Program & paket program
- `IKU_41_breakdown_statistik.png/svg` - Top lembaga & bidang
- `IKU_42_breakdown_praktisi_annotated.png/svg` - Praktisi dengan nama

## 🏗️ Arsitektur Modular

### Shared Utilities

**`visualization_config.py`**
- Konfigurasi global (DPI, fonts, colors)
- Styling constants (BREAKDOWN_STYLE)
- Utility functions (save_figure, read_excel_iku)
- Color palettes (JURUSAN_COLORS)

**`breakdown/breakdown_utils.py`**
- `create_annotated_bar_chart()` - Bar chart dengan nama annotated
- `create_dual_bar_chart()` - Dual chart side-by-side

### Keuntungan Modular Approach

✅ **No Code Duplication** - Shared functions digunakan oleh semua breakdown
✅ **Easy Maintenance** - Ubah sekali di utils, semua chart terupdate
✅ **Consistent Styling** - Semua chart menggunakan constants yang sama
✅ **Easy to Extend** - Tinggal panggil shared functions untuk chart baru

## 📝 Update Terakhir

**Version**: 3.0 (Modular Refactor)
**Date**: 2025-12-23
**Changes**:
- ✅ Full modular refactor - shared utilities
- ✅ Centralized styling constants
- ✅ Created breakdown_utils.py
- ✅ Reduced code duplication by ~70%
- ✅ Added generate_all.py master script
- ✅ Font size increased untuk readability (14pt prodi, 12pt names)
- ✅ Removed italic style untuk bolder appearance

## 🛠️ Dependencies

- Python 3.8+
- pandas
- matplotlib
- numpy
- seaborn
- openpyxl
- textwrap (built-in)

## 📚 Dokumentasi

Lihat [CLAUDE.md](CLAUDE.md) untuk dokumentasi teknis lengkap meliputi:
- Analisis struktur data
- Standar visualisasi publikasi
- Best practices
- Troubleshooting
- Architectural decisions

## 👥 Author

Fakultas Sains & Teknologi
Universitas Jambi

---

**Repository**: https://github.com/akhiyarwaladi/iku_monitoring
