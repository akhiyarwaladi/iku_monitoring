# IKU Monitoring - Fakultas Sains & Teknologi

Sistem visualisasi untuk monitoring Indikator Kinerja Utama (IKU) Fakultas Sains & Teknologi, Universitas Jambi.

## Deskripsi

Project ini menghasilkan visualisasi berkualitas publikasi untuk 4 IKU utama:

- **IKU 31**: Dosen Tetap Berkualifikasi Akademik S3 dan Guru Besar yang Melakukan Kegiatan Tridharma di PT Lain
- **IKU 33**: Dosen yang Membimbing Mahasiswa Luar Program Studi
- **IKU 41**: Dosen Tetap yang Memiliki Sertifikat Kompetensi/Profesi dari DUDI
- **IKU 42**: Pengajar dari Kalangan Praktisi Profesional, Dunia Industri, dan Dunia Kerja

## Fitur

✅ Visualisasi berkualitas publikasi (300 DPI)
✅ Export ke PNG dan SVG
✅ Breakdown charts dengan detail informatif
✅ Text wrapping otomatis untuk labels panjang
✅ Color-coded berdasarkan jurusan
✅ Annotated charts dengan nama dosen

## Struktur Project

```
iku_monitoring/
├── README.md
├── CLAUDE.md                       # Dokumentasi lengkap
├── visualization_config.py          # Konfigurasi & utilities
├── main_visualize_iku.py           # Script utama
├── breakdown/                      # Breakdown charts per IKU
│   ├── iku_31_breakdown.py
│   ├── iku_33_breakdown.py
│   ├── iku_41_breakdown.py
│   └── iku_42_breakdown.py
├── monitoring-iku-*.xlsx           # Data Excel
└── output/                         # Hasil visualisasi
    ├── png/
    └── svg/
```

## Instalasi

```bash
pip install pandas matplotlib seaborn openpyxl
```

## Cara Penggunaan

### Generate Semua Visualisasi

```bash
python main_visualize_iku.py
```

### Generate Breakdown Terpisah

```bash
python breakdown/iku_31_breakdown.py
python breakdown/iku_33_breakdown.py
python breakdown/iku_41_breakdown.py
python breakdown/iku_42_breakdown.py
```

## Output

Hasil visualisasi akan tersimpan di folder `output/`:
- `output/png/` - Format PNG (300 DPI)
- `output/svg/` - Format SVG (vector)

## Dokumentasi

Lihat [CLAUDE.md](CLAUDE.md) untuk dokumentasi lengkap meliputi:
- Analisis struktur data
- Standar visualisasi publikasi
- Best practices
- Troubleshooting

## Update Terakhir

**Version**: 2.0
**Date**: 2025-12-23
**Changes**:
- ✅ Hapus duplikasi chart distribusi geografis dari breakdown
- ✅ Tambah text wrapping untuk labels panjang
- ✅ Ganti dimensi breakdown dengan yang lebih informatif
- ✅ Tambah annotated chart dengan nama dosen (IKU 42)
- ✅ Tambah Paket Program detail (IKU 33)
- ✅ Optimasi layout dan margins

## Dependencies

- Python 3.8+
- pandas
- matplotlib
- seaborn
- openpyxl
- textwrap (built-in)

## Author

Fakultas Sains & Teknologi
Universitas Jambi
