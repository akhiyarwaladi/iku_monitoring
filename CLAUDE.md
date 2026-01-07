# Dokumentasi Sistem Visualisasi IKU Fakultas Sains & Teknologi

## Versi 2.0 - Modular Architecture

**Last Updated**: 2026-01-07
**Version**: 2.0 (Modular)

---

## Mapping IKU (Sesuai Dokumen Resmi)

| PDF IKU | Dashboard IKU | Excel IKU | Deskripsi | Target |
|---------|---------------|-----------|-----------|--------|
| **IKU 1.1** | IKU 1 | 1 (11+12+13) | Lulusan Bekerja/Studi/Wiraswasta | **60%** |
| **IKU 1.2** | IKU 2 | 2 (21+22+23) | Mahasiswa di Luar Prodi/Prestasi | **30%** |
| **IKU 2.1** | IKU 3 | 3 (31+33) | Dosen Tridharma/Praktisi/Bimbingan | **25%** |
| **IKU 2.2** | IKU 4 | 4 (41+42) | Dosen Sertifikat DUDI/Pengajar Praktisi | **20.14%** |

---

## Arsitektur Sistem (Modular v2.0)

### Struktur File

```
iku_monitoring/
├── CLAUDE.md                    # Dokumentasi ini
├── config.py                    # Konfigurasi, warna, metadata
├── utils.py                     # Fungsi utility (I/O, setup style)
├── processors.py                # Fungsi pemrosesan data per IKU
├── visualizations.py            # Fungsi visualisasi (charts)
├── main_visualize_iku.py        # Script utama (orchestration)
├── target/                      # Dokumen referensi
│   ├── target_iku.pdf           # Target IKU resmi
│   └── Dashboard _ UNJA.pdf     # Dashboard UNJA
├── monitoring-iku-*.xlsx        # File data Excel
└── output/                      # Hasil visualisasi
    ├── png/                     # Format PNG (300 DPI)
    └── svg/                     # Format SVG (vector)
```

### Diagram Arsitektur

```
┌─────────────────────────────────────────────────────────────────┐
│                        config.py                                 │
│   - CONFIG (settings)                                           │
│   - COLORS, JURUSAN_COLORS                                      │
│   - IKU_METADATA, IKU_EXPANSION                                 │
│   - ALL_IKU                                                     │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                         utils.py                                 │
│   - setup_publication_style()                                    │
│   - read_excel_iku()                                            │
│   - save_figure()                                               │
│   - cleanup_output_folder()                                     │
│   - sort_by_jurusan(), assign_colors_by_jurusan()              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                      processors.py                               │
│   - process_iku_11/12/13() - Lulusan                            │
│   - process_iku_21/22/23() - Mahasiswa                          │
│   - process_iku_31/33()    - Dosen Tridharma                    │
│   - process_iku_41/42()    - Dosen DUDI                         │
│   - process_iku_1/2/3/4_combined() - Gabungan                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                   visualizations.py                              │
│   - create_horizontal_bar_chart()                               │
│   - create_vertical_bar_chart()                                 │
│   - create_summary_dashboard()                                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                  main_visualize_iku.py                          │
│   - process_single_iku()                                        │
│   - main()                                                      │
│   - parse_arguments()                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Panduan Penggunaan

### Menjalankan Visualisasi

```bash
# Generate semua IKU
python main_visualize_iku.py

# Generate IKU tertentu
python main_visualize_iku.py --iku 1              # IKU 1 (gabungan 11,12,13)
python main_visualize_iku.py --iku 31 33          # IKU 31 dan 33 saja
python main_visualize_iku.py --iku 4              # IKU 4 (gabungan 41,42)

# Opsi tambahan
python main_visualize_iku.py --iku 1 --no-breakdown --no-dashboard --no-cleanup
```

### Parameter Command Line

| Parameter | Deskripsi |
|-----------|-----------|
| `--iku` / `-i` | Pilih IKU yang akan di-generate (default: semua) |
| `--no-breakdown` | Skip pembuatan breakdown charts |
| `--no-dashboard` | Skip pembuatan summary dashboard |
| `--no-cleanup` | Jangan hapus file output sebelumnya |

### Contoh Output

```
======================================================================
SISTEM VISUALISASI IKU FAKULTAS SAINS & TEKNOLOGI
Standar Publikasi Internasional (Modular v2.0)
======================================================================

IKU 1: IKU 1.1: Lulusan Bekerja/Studi Lanjut/Wiraswasta
  [1/3] Menggabungkan data IKU 11, 12, 13...
    - IKU 11 (Bekerja): 256 lulusan
    - IKU 12 (Studi Lanjut): 19 lulusan
    - IKU 13 (Wiraswasta): 43 lulusan
    - Gabungan unik: 318 lulusan
  [2/3] Statistik gabungan:
        Pembilang: 318 lulusan
        Penyebut: 460 lulusan
        Persentase: 69.13%
  [3/3] Membuat visualisasi (vertical only)...
    ✓ PNG: png/IKU_1_vertical.png
    ✓ SVG: svg/IKU_1_vertical.svg
  ✅ IKU 1 (Gabungan) selesai diproses
```

---

## Konfigurasi

### Edit `config.py` untuk mengubah:

```python
CONFIG = {
    'dpi': 300,                    # Resolution output (300 = publication quality)
    'font_size': 9,                # Font size
    'show_target_line': True,      # Tampilkan garis target
    'target_values': {             # Target untuk setiap IKU
        '1': 60, '11': 60, '12': 60, '13': 60,      # IKU 1.1 PDF
        '2': 30, '21': 30, '22': 30, '23': 30,      # IKU 1.2 PDF
        '3': 25, '31': 25, '33': 25,                 # IKU 2.1 PDF
        '4': 20.14, '41': 20.14, '42': 20.14,       # IKU 2.2 PDF
    },
    'target_linewidth': 3.0,       # Ketebalan garis target
    'output_dir': 'output',        # Folder output
}
```

---

## Hasil Pencapaian IKU (2025)

### IKU 1.1 (Lulusan) - Target 60%
| Komponen | Capaian | Status |
|----------|---------|--------|
| Gabungan (1) | 69.13% (318/460) | ✅ Di atas target |
| Bekerja (11) | 55.65% (256/460) | |
| Studi Lanjut (12) | 4.13% (19/460) | |
| Wiraswasta (13) | 9.35% (43/460) | |

### IKU 1.2 (Mahasiswa) - Target 30%
| Komponen | Capaian | Status |
|----------|---------|--------|
| Gabungan (2) | 6.03% (276/4576) | ❌ Di bawah target |
| MBKM (21) | 4.11% (188/4576) | |
| Prestasi (22) | 3.23% (148/4576) | |
| HKI (23) | 0.04% (2/4576) | |

### IKU 2.1 (Dosen Tridharma) - Target 25%
| Komponen | Capaian | Status |
|----------|---------|--------|
| Gabungan (3) | 67.96% (140/206) | ✅ Di atas target |
| Tridharma di PT Lain (31) | 59.71% (123/206) | |
| Membimbing Mahasiswa (33) | 27.18% (56/206) | |

### IKU 2.2 (Dosen DUDI) - Target 20.14%
| Komponen | Capaian | Status |
|----------|---------|--------|
| Gabungan (4) | 51.46% (106/206) | ✅ Di atas target |
| Sertifikat DUDI (41) | 20.39% (42/206) | |
| Pengajar Praktisi (42) | 31.07% (64/206) | |

---

## Best Practices

### 1. Modifikasi Konfigurasi
Edit `config.py` untuk mengubah target, warna, atau metadata IKU.

### 2. Menambah Processor Baru
Tambahkan fungsi baru di `processors.py` dan daftarkan di `IKU_PROCESSORS`.

### 3. Modifikasi Visualisasi
Edit fungsi di `visualizations.py` untuk mengubah tampilan chart.

### 4. Testing
Selalu jalankan dengan `--iku` untuk test satu IKU sebelum generate semua.

---

## Troubleshooting

### Error: 'Program Studi' not found
**Penyebab**: File pembilang tidak memiliki kolom Program Studi
**Solusi**: Processor otomatis melakukan join dengan file penyebut

### Error: Missing NIP/NIM
**Penyebab**: Data di file Excel tidak lengkap
**Solusi**: Periksa konsistensi identifier di kedua file

### Visualisasi tidak sesuai
**Solusi**: Edit konfigurasi di `config.py` atau fungsi di `visualizations.py`

---

## Dependencies

```bash
pip install pandas matplotlib seaborn openpyxl
```

- Python 3.8+
- pandas
- matplotlib
- seaborn
- openpyxl

---

## Kontak & Support

**Tim IKU Fakultas Sains & Teknologi**
Universitas Jambi
