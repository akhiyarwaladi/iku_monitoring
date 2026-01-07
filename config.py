"""
============================================================================
KONFIGURASI SISTEM VISUALISASI IKU
============================================================================

Modul ini berisi semua konfigurasi global untuk sistem visualisasi IKU
Fakultas Sains & Teknologi, Universitas Jambi.

Author: Tim IKU FST
Version: 2.0 (Modular)
Last Updated: 2026-01-07
============================================================================
"""

from pathlib import Path

# Daftar semua IKU yang tersedia
# Note: 51 and 62 are number-based, only processed through combined 5 and 6
ALL_IKU = ['1', '11', '12', '13', '2', '21', '22', '23', '3', '31', '33', '4', '41', '42', '5', '6', '7', '71', '8', '81']

# ============================================================================
# KONFIGURASI GLOBAL
# ============================================================================

CONFIG = {
    # Paths
    'base_path': Path(__file__).parent,
    'output_dir': 'output',

    # Publication settings
    'dpi': 300,  # Publication quality (300 DPI is standard for journals)
    'font_size': 9,
    'font_family': 'sans-serif',
    'font_name': ['Arial', 'Helvetica', 'DejaVu Sans'],

    # Export formats
    'export_png': True,
    'export_svg': False,  # Vector format - set to True when needed for publication

    # Line widths (publication standard)
    'axes_linewidth': 0.75,
    'grid_linewidth': 0.5,
    'bar_linewidth': 0.75,

    # Figure sizes (inches)
    'figsize_horizontal': (10, 6),
    'figsize_vertical': (12, 6),
    'figsize_dashboard': (15, 5),

    # Target values (berdasarkan PDF target_iku.pdf)
    'show_target_line': True,  # Aktifkan garis target
    'target_values': {
        # IKU 1.1 PDF (Lulusan): Target 60%
        '1': 60,
        '11': 60,
        '12': 60,
        '13': 60,
        # IKU 1.2 PDF (Mahasiswa di luar prodi / prestasi): Target 30%
        '2': 30,
        '21': 30,
        '22': 30,
        '23': 30,
        # IKU 2.1 PDF (Dosen Tridharma & Bimbingan): Target 25%
        '3': 25,
        '31': 25,
        '33': 25,
        # IKU 2.2 PDF (Dosen DUDI & Praktisi): Target 20.14%
        '4': 20.14,
        '41': 20.14,
        '42': 20.14,
        # IKU 5 (Luaran Dosen Rekognisi Internasional): Target 5%
        '5': 5,
        '51': 5,
        # IKU 6 (Kerjasama per Prodi): Target 2 per prodi
        '6': 2,
        '62': 2,
        # IKU 7 (Mata Kuliah PJBL/Case Method): Target 50%
        '7': 50,
        '71': 50,
        # IKU 8 (Prodi Akreditasi Internasional): Target 10%
        '8': 10,
        '81': 10,
    },

    # Target line style
    'target_linewidth': 3.0,  # Ketebalan garis target

    # Color settings
    'color_palette': 'colorblind',  # colorblind, vibrant, pastel
}

# ============================================================================
# COLOR PALETTES
# ============================================================================

# Colorblind-friendly palette (ColorBrewer)
COLORS = {
    'primary': '#0173B2',      # Blue
    'secondary': '#DE8F05',    # Orange
    'success': '#029E73',      # Teal green
    'target': '#D55E00',       # Vermillion
    'warning': '#ECE133',      # Yellow
    'neutral': '#999999',      # Gray
}

# Mapping Program Studi ke Jurusan
PRODI_TO_JURUSAN = {
    # Jurusan MIPA
    'Matematika': 'MIPA',
    'Biologi': 'MIPA',
    'Fisika': 'MIPA',
    'Kimia': 'MIPA',

    # Jurusan Teknik Geologi
    'Teknik Geofisika': 'Teknik Geologi',
    'Teknik Geologi': 'Teknik Geologi',

    # Jurusan Teknik Kimia
    'Teknik Kimia': 'Teknik Kimia',
    'Teknik Lingkungan': 'Teknik Kimia',

    # Jurusan Teknik Sipil
    'Teknik Sipil': 'Teknik Sipil',
    'Teknik Pertambangan': 'Teknik Sipil',

    # Jurusan Teknik Elektro
    'Teknik Elektro': 'Teknik Elektro',
    'Sistem Informasi': 'Teknik Elektro',
    'Informatika': 'Teknik Elektro',

    # Program D3
    'Analis Kimia (D3)': 'D3',
    'Kimia Industri (D3)': 'D3',
}

# Urutan Jurusan untuk tampilan
JURUSAN_ORDER = ['MIPA', 'Teknik Geologi', 'Teknik Kimia', 'Teknik Sipil', 'Teknik Elektro', 'D3']

# Warna soft tapi tetap tegas per Jurusan (soft professional palette)
JURUSAN_COLORS = {
    'MIPA': {
        'base': '#5B9BD5',      # Soft Blue
        'light': '#9DC3E6',
        'dark': '#2E75B6'
    },
    'Teknik Geologi': {
        'base': '#ED7D31',      # Soft Orange
        'light': '#F4B183',
        'dark': '#C65911'
    },
    'Teknik Kimia': {
        'base': '#70AD47',      # Soft Green
        'light': '#A8D08D',
        'dark': '#548235'
    },
    'Teknik Sipil': {
        'base': '#9966CC',      # Soft Purple
        'light': '#C5A8E0',
        'dark': '#7030A0'
    },
    'Teknik Elektro': {
        'base': '#E85D75',      # Soft Red/Pink
        'light': '#F4A6B7',
        'dark': '#C13552'
    },
    'D3': {
        'base': '#7F8C8D',      # Soft Gray
        'light': '#BDC3C7',
        'dark': '#5D6D7E'
    }
}

# ============================================================================
# IKU METADATA
# ============================================================================
# Naming convention mengikuti dokumen resmi:
# - PDF IKU 1.1 = Dashboard IKU 1 = Excel IKU 1 (gabungan 11,12,13)
# - PDF IKU 1.2 = Dashboard IKU 2 = Excel IKU 2 (gabungan 21,22,23)
# - PDF IKU 2.1 = Dashboard IKU 3 = Excel IKU 3 (gabungan 31,33)
# - PDF IKU 2.2 = Dashboard IKU 4 = Excel IKU 4 (gabungan 41,42)

IKU_METADATA = {
    # === IKU 1.1 PDF (Dashboard IKU 1): Lulusan ===
    # Target: 60%
    '1': {
        'title': 'IKU 1.1: Lulusan Bekerja/Studi Lanjut/Wiraswasta',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 60%',
        'description': 'Persentase lulusan S1 dan D4/D3 yang berhasil memiliki pekerjaan; melanjutkan studi; atau menjadi wiraswasta'
    },
    '11': {
        'title': 'IKU 1.1a: Lulusan yang Memiliki Pekerjaan',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 60%',
        'description': 'Persentase lulusan S1 dan D4/D3 yang memiliki pekerjaan'
    },
    '12': {
        'title': 'IKU 1.1b: Lulusan yang Melanjutkan Studi',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 60%',
        'description': 'Persentase lulusan S1 dan D4/D3 yang melanjutkan studi'
    },
    '13': {
        'title': 'IKU 1.1c: Lulusan yang Berwiraswasta',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 60%',
        'description': 'Persentase lulusan S1 dan D4/D3 yang menjadi wiraswasta'
    },
    # === IKU 1.2 PDF (Dashboard IKU 2): Mahasiswa ===
    # Target: 30%
    '2': {
        'title': 'IKU 1.2: Mahasiswa Berkegiatan di Luar Prodi/Meraih Prestasi',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 30%',
        'description': 'Persentase mahasiswa S1 dan D4/D3 yang menjalankan kegiatan pembelajaran di luar program studi atau meraih prestasi'
    },
    '21': {
        'title': 'IKU 1.2a: Mahasiswa Mengikuti Kegiatan MBKM',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 30%',
        'description': 'Persentase mahasiswa S1 dan D4/D3 yang menjalankan kegiatan pembelajaran di luar program studi (kegiatan MBKM)'
    },
    '22': {
        'title': 'IKU 1.2b: Mahasiswa Meraih Prestasi Kompetisi',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 30%',
        'description': 'Persentase mahasiswa S1 dan D4/D3 yang meraih prestasi dalam kompetisi peringkat 1 s.d harapan III'
    },
    '23': {
        'title': 'IKU 1.2c: Mahasiswa Memiliki Karya/HKI',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 30%',
        'description': 'Persentase mahasiswa S1 dan D4/D3 yang memiliki karya yang digunakan masyarakat/DUDI'
    },
    # === IKU 2.1 PDF (Dashboard IKU 3): Dosen Tridharma/Praktisi/Bimbingan ===
    # Target: 25%
    '3': {
        'title': 'IKU 2.1: Dosen Tridharma di PT Lain/Praktisi/Membimbing',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 25%',
        'description': 'Persentase dosen yang berkegiatan tridharma di perguruan tinggi lain, bekerja sebagai praktisi di DUDI, atau membimbing mahasiswa berkegiatan di luar program studi'
    },
    '31': {
        'title': 'IKU 2.1a: Dosen Berkegiatan Tridharma di PT Lain',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 25%',
        'description': 'Persentase dosen yang berkegiatan tridharma di perguruan tinggi lain (Pendidikan, Penelitian, Pengabdian)'
    },
    '33': {
        'title': 'IKU 2.1b: Dosen Membimbing Mahasiswa di Luar Prodi',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 25%',
        'description': 'Persentase dosen yang membimbing mahasiswa berkegiatan di luar program studi (MBKM, ProIDE, PKM, PMW, dll)'
    },
    # === IKU 2.2 PDF (Dashboard IKU 4): Kualifikasi Dosen/Pengajar ===
    # Target: 20.14%
    '4': {
        'title': 'IKU 2.2: Dosen Sertifikat DUDI/Pengajar Praktisi',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 20.14%',
        'description': 'Persentase dosen yang memiliki sertifikat kompetensi/profesi yang diakui DUDI atau pengajar yang berasal dari kalangan praktisi profesional'
    },
    '41': {
        'title': 'IKU 2.2a: Dosen Memiliki Sertifikat Kompetensi DUDI',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 20.14%',
        'description': 'Persentase dosen yang memiliki sertifikat kompetensi/profesi yang diakui oleh dunia usaha dan dunia industri'
    },
    '42': {
        'title': 'IKU 2.2b: Pengajar dari Kalangan Praktisi',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 20.14%',
        'description': 'Persentase pengajar yang berasal dari kalangan praktisi profesional, dunia usaha, atau dunia industri'
    },
    # === IKU 5 (Luaran Dosen Rekognisi Internasional) ===
    # Target: 5%
    '5': {
        'title': 'IKU 5: Luaran Dosen Rekognisi Internasional',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 5%',
        'description': 'Persentase dosen yang luarannya mendapat rekognisi internasional atau diterapkan oleh masyarakat/industri/pemerintah'
    },
    '51': {
        'title': 'IKU 5: Luaran Dosen Rekognisi Internasional',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 5%',
        'description': 'Persentase dosen yang luarannya mendapat rekognisi internasional atau diterapkan oleh masyarakat/industri/pemerintah'
    },
    # === IKU 6 (Kerjasama per Program Studi) ===
    # Target: 2 per prodi
    '6': {
        'title': 'IKU 6: Kerjasama per Program Studi',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 2 per prodi',
        'description': 'Jumlah kerjasama per program studi S1 dan D3/D4 dalam bentuk Implementation Agreement (IA)'
    },
    '62': {
        'title': 'IKU 6: Kerjasama per Program Studi',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 2 per prodi',
        'description': 'Jumlah kerjasama per program studi S1 dan D3/D4 dalam bentuk Implementation Agreement (IA)'
    },
    # === IKU 7 (Mata Kuliah PJBL/Case Method) ===
    # Target: 50%
    '7': {
        'title': 'IKU 7: Mata Kuliah PJBL/Case Method',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 50%',
        'description': 'Persentase mata kuliah S1 dan D3/D4 yang menggunakan metode pembelajaran PJBL/Case Method sebagai bagian dari bobot evaluasi'
    },
    '71': {
        'title': 'IKU 7: Mata Kuliah PJBL/Case Method',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 50%',
        'description': 'Persentase mata kuliah S1 dan D3/D4 yang menggunakan metode pembelajaran PJBL/Case Method sebagai bagian dari bobot evaluasi'
    },
    # === IKU 8 (Prodi Akreditasi Internasional) ===
    # Target: 10%
    '8': {
        'title': 'IKU 8: Prodi Akreditasi Internasional',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 10%',
        'description': 'Persentase program studi S1 dan D3/D4 yang memiliki akreditasi/sertifikat internasional yang diakui pemerintah'
    },
    '81': {
        'title': 'IKU 8: Prodi Akreditasi Internasional',
        'subtitle': 'Fakultas Sains & Teknologi 2025 | Target: 10%',
        'description': 'Persentase program studi S1 dan D3/D4 yang memiliki akreditasi/sertifikat internasional yang diakui pemerintah'
    }
}

# ============================================================================
# IKU EXPANSION MAPPING
# ============================================================================

# Mapping: IKU gabungan -> komponen-komponennya
IKU_EXPANSION = {
    '1': ['1', '11', '12', '13'],   # IKU 1.1 PDF: Lulusan
    '2': ['2', '21', '22', '23'],   # IKU 1.2 PDF: Mahasiswa
    '3': ['3', '31', '33'],          # IKU 2.1 PDF: Dosen Tridharma
    '4': ['4', '41', '42'],          # IKU 2.2 PDF: Dosen DUDI
    '5': ['5'],                      # IKU 5: Luaran Dosen Rekognisi (number-based)
    '6': ['6'],                      # IKU 6: Kerjasama per Prodi (number-based)
    '7': ['7', '71'],                # IKU 7: Mata Kuliah PJBL/Case Method
    '8': ['8', '81'],                # IKU 8: Prodi Akreditasi Internasional
}
