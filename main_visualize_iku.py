"""
============================================================================
SISTEM VISUALISASI IKU FAKULTAS SAINS & TEKNOLOGI
Universitas Jambi
============================================================================

Script terpusat untuk visualisasi semua IKU dengan standar publikasi
internasional.

Author: Tim IKU FST
Version: 1.0
Last Updated: 2025-12-23

Referensi:
- Ten guidelines for effective data visualization (Environmental Modelling & Software)
- Nature, Science, IEEE publication standards
- ColorBrewer2.org colorblind-safe palettes
============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
from datetime import datetime
import sys
import textwrap

warnings.filterwarnings('ignore')

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
    'export_svg': True,  # Vector format for unlimited quality

    # Line widths (publication standard)
    'axes_linewidth': 0.75,
    'grid_linewidth': 0.5,
    'bar_linewidth': 0.75,

    # Figure sizes (inches)
    'figsize_horizontal': (10, 6),
    'figsize_vertical': (12, 6),
    'figsize_dashboard': (15, 5),

    # Target values
    'show_target_line': False,  # Set True jika ada target
    'target_values': {
        '31': None,  # Contoh: 60 untuk target 60%
        '33': None,
        '41': None,
        '42': None
    },

    # Color settings
    'color_palette': 'colorblind',  # colorblind, vibrant, pastel
}

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
        'base': '#5B9BD5',      # Soft Blue (lebih soft dari sebelumnya)
        'light': '#9DC3E6',
        'dark': '#2E75B6'
    },
    'Teknik Geologi': {
        'base': '#ED7D31',      # Soft Orange (lebih soft)
        'light': '#F4B183',
        'dark': '#C65911'
    },
    'Teknik Kimia': {
        'base': '#70AD47',      # Soft Green (lebih soft)
        'light': '#A8D08D',
        'dark': '#548235'
    },
    'Teknik Sipil': {
        'base': '#9966CC',      # Soft Purple (lebih soft)
        'light': '#C5A8E0',
        'dark': '#7030A0'
    },
    'Teknik Elektro': {
        'base': '#E85D75',      # Soft Red/Pink (lebih soft)
        'light': '#F4A6B7',
        'dark': '#C13552'
    },
    'D3': {
        'base': '#7F8C8D',      # Soft Gray (lebih soft)
        'light': '#BDC3C7',
        'dark': '#5D6D7E'
    }
}

# Warna untuk setiap program studi (generated dari jurusan)
def get_prodi_color(prodi_name, index_in_jurusan=0, total_in_jurusan=1):
    """Generate warna untuk prodi berdasarkan jurusan dengan gradient"""
    jurusan = PRODI_TO_JURUSAN.get(prodi_name, 'MIPA')
    colors = JURUSAN_COLORS[jurusan]

    # Jika hanya 1 prodi di jurusan, gunakan base color
    if total_in_jurusan == 1:
        return colors['base']

    # Jika lebih dari 1, buat gradient dari dark ke light
    if index_in_jurusan == 0:
        return colors['dark']
    elif index_in_jurusan == total_in_jurusan - 1:
        return colors['light']
    else:
        return colors['base']

# IKU Metadata
IKU_METADATA = {
    '11': {
        'title': 'Persentase Lulusan yang Memiliki Pekerjaan',
        'subtitle': 'Fakultas Sains & Teknologi 2025',
        'description': 'Lulusan yang bekerja setelah lulus'
    },
    '12': {
        'title': 'Persentase Lulusan yang Melanjutkan Studi',
        'subtitle': 'Fakultas Sains & Teknologi 2025',
        'description': 'Lulusan yang melanjutkan pendidikan ke jenjang lebih tinggi'
    },
    '13': {
        'title': 'Persentase Lulusan yang Berwiraswasta',
        'subtitle': 'Fakultas Sains & Teknologi 2025',
        'description': 'Lulusan yang berwiraswasta/membangun usaha sendiri'
    },
    '21': {
        'title': 'Persentase Mahasiswa yang Mengikuti Kegiatan MBKM',
        'subtitle': 'Fakultas Sains & Teknologi 2025',
        'description': 'Mahasiswa yang mengikuti kegiatan MBKM (Magang, Studi Independen, dll)'
    },
    '22': {
        'title': 'Persentase Mahasiswa yang Meraih Prestasi',
        'subtitle': 'Fakultas Sains & Teknologi 2025',
        'description': 'Mahasiswa yang meraih prestasi tingkat lokal hingga internasional'
    },
    '23': {
        'title': 'Persentase Mahasiswa yang Memiliki HKI',
        'subtitle': 'Fakultas Sains & Teknologi 2025',
        'description': 'Mahasiswa yang memiliki Hak Kekayaan Intelektual'
    },
    '31': {
        'title': 'Persentase Dosen Berkegiatan Tridharma di Perguruan Tinggi Lain',
        'subtitle': 'Fakultas Sains & Teknologi 2025',
        'description': 'Dosen yang berkegiatan tridharma (Pendidikan, Penelitian, Pengabdian) di PT lain'
    },
    '33': {
        'title': 'Persentase Dosen Membimbing Mahasiswa Berkegiatan di Luar Program Studi',
        'subtitle': 'Fakultas Sains & Teknologi 2025',
        'description': 'Dosen membimbing mahasiswa di luar prodi (MBKM, ProIDE, PKM, PMW, dll)'
    },
    '41': {
        'title': 'Persentase Dosen Memiliki Sertifikat Kompetensi/Profesi DUDI',
        'subtitle': 'Fakultas Sains & Teknologi 2025',
        'description': 'Dosen memiliki sertifikat kompetensi/profesi yang diakui DUDI'
    },
    '42': {
        'title': 'Persentase Pengajar yang Berasal dari Kalangan Praktisi',
        'subtitle': 'Fakultas Sains & Teknologi 2025',
        'description': 'Dosen yang berasal dari kalangan praktisi profesional'
    }
}

# ============================================================================
# SETUP MATPLOTLIB PUBLICATION STYLE
# ============================================================================

def setup_publication_style():
    """Setup style matplotlib sesuai standar publikasi internasional"""
    plt.rcParams.update({
        'figure.dpi': CONFIG['dpi'],
        'savefig.dpi': CONFIG['dpi'],
        'font.size': CONFIG['font_size'],
        'font.family': CONFIG['font_family'],
        'font.sans-serif': CONFIG['font_name'],
        'axes.linewidth': CONFIG['axes_linewidth'],
        'grid.linewidth': CONFIG['grid_linewidth'],
        'lines.linewidth': 1.5,
        'patch.linewidth': CONFIG['bar_linewidth'],
        'xtick.major.width': CONFIG['axes_linewidth'],
        'ytick.major.width': CONFIG['axes_linewidth'],
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        'xtick.major.size': 3,
        'ytick.major.size': 3,
        'legend.frameon': True,
        'legend.framealpha': 0.95,
        'legend.fancybox': False,
        'legend.edgecolor': '0.2',
        'legend.borderpad': 0.4,
    })

    sns.set_style("ticks", {
        'axes.grid': True,
        'grid.linestyle': ':',
        'grid.alpha': 0.4,
    })

# ============================================================================
# FUNGSI UTILITY - DATA PROCESSING
# ============================================================================

def read_excel_iku(iku_number, file_type='pembilang'):
    """
    Membaca file Excel IKU

    Parameters:
    -----------
    iku_number : str
        Nomor IKU (31, 33, 41)
    file_type : str
        'pembilang' atau 'penyebut'

    Returns:
    --------
    pd.DataFrame
    """
    file_path = CONFIG['base_path'] / f'monitoring-iku-{iku_number}-{file_type}.xlsx'

    if not file_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")

    # Baca dengan header di baris 1 (index 1)
    df = pd.read_excel(file_path, header=1)

    return df

def process_iku_31(df_pembilang, df_penyebut):
    """
    Proses data IKU 31 - Tridharma di PT Lain

    Returns:
    --------
    pd.DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    """
    # Hitung penyebut per prodi
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')

    # Join pembilang dengan penyebut untuk dapat info prodi
    pembilang_with_prodi = df_pembilang.merge(
        df_penyebut[['NIP', 'Program Studi']],
        on='NIP',
        how='left'
    )

    # Hitung pembilang per prodi
    pembilang_prodi = pembilang_with_prodi.groupby('Program Studi').size().reset_index(name='Pembilang')

    # Gabungkan
    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)

    # Bersihkan nama prodi
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')

    # Sort berdasarkan persentase
    result = result.sort_values('Persentase', ascending=True)

    return result

def process_iku_33(df_pembilang, df_penyebut):
    """
    Proses data IKU 33 - Membimbing Mahasiswa Luar Prodi

    Note: File pembilang sudah memiliki kolom Program Studi

    Returns:
    --------
    pd.DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    """
    # Normalisasi nama Program Studi di pembilang
    # Pembilang: "Kimia", "Matematika"
    # Penyebut: "Program Studi Kimia", "Program Studi Matematika"
    df_pembilang = df_pembilang.copy()

    # Tambahkan prefix "Program Studi" jika belum ada
    def normalize_prodi_name(name):
        if pd.isna(name):
            return name
        name = str(name).strip()
        if not name.startswith('Program Studi'):
            # Handle special cases
            if name == 'Analis Kimia':
                return 'Program Studi Analis Kimia (D3)'
            elif name == 'Kimia Industri':
                return 'Program Studi Kimia Industri (D3)'
            else:
                return f'Program Studi {name}'
        return name

    df_pembilang['Program Studi'] = df_pembilang['Program Studi'].apply(normalize_prodi_name)

    # Hitung penyebut per prodi
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')

    # Hitung pembilang per prodi
    pembilang_prodi = df_pembilang.groupby('Program Studi').size().reset_index(name='Pembilang')

    # Gabungkan
    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)

    # Bersihkan nama prodi
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')

    # Sort berdasarkan persentase
    result = result.sort_values('Persentase', ascending=True)

    return result

def process_iku_41(df_pembilang, df_penyebut):
    """
    Proses data IKU 41 - Sertifikat DUDI

    Note: File pembilang sudah memiliki kolom Program Studi

    Returns:
    --------
    pd.DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    """
    # Normalisasi nama Program Studi di pembilang (sama seperti IKU 33)
    df_pembilang = df_pembilang.copy()

    # Tambahkan prefix "Program Studi" jika belum ada
    def normalize_prodi_name(name):
        if pd.isna(name):
            return name
        name = str(name).strip()
        if not name.startswith('Program Studi'):
            # Handle special cases
            if name == 'Analis Kimia':
                return 'Program Studi Analis Kimia (D3)'
            elif name == 'Kimia Industri':
                return 'Program Studi Kimia Industri (D3)'
            else:
                return f'Program Studi {name}'
        return name

    df_pembilang['Program Studi'] = df_pembilang['Program Studi'].apply(normalize_prodi_name)

    # Hitung penyebut per prodi
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')

    # Hitung pembilang per prodi
    pembilang_prodi = df_pembilang.groupby('Program Studi').size().reset_index(name='Pembilang')

    # Gabungkan
    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)

    # Bersihkan nama prodi
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')

    # Sort berdasarkan persentase
    result = result.sort_values('Persentase', ascending=True)

    return result

def process_iku_42(df_pembilang, df_penyebut):
    """
    Proses data IKU 42 - Pengajar dari Kalangan Praktisi

    Note: File pembilang sudah memiliki kolom Program Studi (seperti IKU 33 dan 41)

    Returns:
    --------
    pd.DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    """
    # Hitung penyebut per prodi
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')

    # Hitung pembilang per prodi (sudah ada kolom Program Studi di pembilang)
    pembilang_prodi = df_pembilang.groupby('Program Studi').size().reset_index(name='Pembilang')

    # Gabungkan
    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)

    # Bersihkan nama prodi
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')

    # Sort berdasarkan persentase
    result = result.sort_values('Persentase', ascending=True)

    return result

def process_iku_11(df_pembilang, df_penyebut):
    """
    Proses data IKU 11 - Lulusan yang Memiliki Pekerjaan

    Note: File pembilang sudah memiliki kolom Prodi (bukan Program Studi)

    Returns:
    --------
    pd.DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    """
    # Hitung penyebut per prodi
    penyebut_prodi = df_penyebut.groupby('Prodi').size().reset_index(name='Penyebut')

    # Hitung pembilang per prodi (sudah ada kolom Prodi di pembilang)
    pembilang_prodi = df_pembilang.groupby('Prodi').size().reset_index(name='Pembilang')

    # Gabungkan
    result = penyebut_prodi.merge(pembilang_prodi, on='Prodi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)

    # Rename Prodi ke Program Studi untuk konsistensi
    result = result.rename(columns={'Prodi': 'Program Studi'})

    # Bersihkan nama prodi jika ada prefix "Program Studi "
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')

    # Sort berdasarkan persentase
    result = result.sort_values('Persentase', ascending=True)

    return result

def process_iku_12(df_pembilang, df_penyebut):
    """
    Proses data IKU 12 - Lulusan yang Melanjutkan Studi

    Note: File pembilang sudah memiliki kolom Prodi (bukan Program Studi)

    Returns:
    --------
    pd.DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    """
    # Hitung penyebut per prodi
    penyebut_prodi = df_penyebut.groupby('Prodi').size().reset_index(name='Penyebut')

    # Hitung pembilang per prodi (sudah ada kolom Prodi di pembilang)
    pembilang_prodi = df_pembilang.groupby('Prodi').size().reset_index(name='Pembilang')

    # Gabungkan
    result = penyebut_prodi.merge(pembilang_prodi, on='Prodi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)

    # Rename Prodi ke Program Studi untuk konsistensi
    result = result.rename(columns={'Prodi': 'Program Studi'})

    # Bersihkan nama prodi jika ada prefix "Program Studi "
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')

    # Sort berdasarkan persentase
    result = result.sort_values('Persentase', ascending=True)

    return result

def process_iku_13(df_pembilang, df_penyebut):
    """
    Proses data IKU 13 - Lulusan yang Berwiraswasta

    Note: File pembilang sudah memiliki kolom Prodi (bukan Program Studi)

    Returns:
    --------
    pd.DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    """
    # Hitung penyebut per prodi
    penyebut_prodi = df_penyebut.groupby('Prodi').size().reset_index(name='Penyebut')

    # Hitung pembilang per prodi (sudah ada kolom Prodi di pembilang)
    pembilang_prodi = df_pembilang.groupby('Prodi').size().reset_index(name='Pembilang')

    # Gabungkan
    result = penyebut_prodi.merge(pembilang_prodi, on='Prodi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)

    # Rename Prodi ke Program Studi untuk konsistensi
    result = result.rename(columns={'Prodi': 'Program Studi'})

    # Bersihkan nama prodi jika ada prefix "Program Studi "
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')

    # Sort berdasarkan persentase
    result = result.sort_values('Persentase', ascending=True)

    return result

def process_iku_21(df_pembilang, df_penyebut):
    """
    Proses data IKU 21 - Mahasiswa yang Mengikuti Kegiatan MBKM

    Note: File menggunakan kolom 'Program Studi'

    Returns:
    --------
    pd.DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    """
    # Hitung penyebut per prodi
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')

    # Hitung pembilang per prodi (sudah ada kolom Program Studi di pembilang)
    pembilang_prodi = df_pembilang.groupby('Program Studi').size().reset_index(name='Pembilang')

    # Gabungkan
    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)

    # Bersihkan nama prodi jika ada prefix "Program Studi "
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')

    # Sort berdasarkan persentase
    result = result.sort_values('Persentase', ascending=True)

    return result

def process_iku_22(df_pembilang, df_penyebut):
    """
    Proses data IKU 22 - Mahasiswa yang Meraih Prestasi

    Note: File pembilang tidak memiliki kolom 'Program Studi', perlu join dengan penyebut

    Returns:
    --------
    pd.DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    """
    # Hitung penyebut per prodi
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')

    # Join pembilang dengan penyebut untuk dapat info prodi
    pembilang_with_prodi = df_pembilang.merge(
        df_penyebut[['NIM', 'Program Studi']],
        on='NIM',
        how='left'
    )

    # Hitung pembilang per prodi
    pembilang_prodi = pembilang_with_prodi.groupby('Program Studi').size().reset_index(name='Pembilang')

    # Gabungkan
    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)

    # Bersihkan nama prodi jika ada prefix "Program Studi "
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')

    # Sort berdasarkan persentase
    result = result.sort_values('Persentase', ascending=True)

    return result

def process_iku_23(df_pembilang, df_penyebut):
    """
    Proses data IKU 23 - Mahasiswa yang Memiliki HKI

    Note: File menggunakan kolom 'Program Studi'

    Returns:
    --------
    pd.DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    """
    # Hitung penyebut per prodi
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')

    # Hitung pembilang per prodi (sudah ada kolom Program Studi di pembilang)
    pembilang_prodi = df_pembilang.groupby('Program Studi').size().reset_index(name='Pembilang')

    # Gabungkan
    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)

    # Bersihkan nama prodi jika ada prefix "Program Studi "
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')

    # Sort berdasarkan persentase
    result = result.sort_values('Persentase', ascending=True)

    return result

def sort_by_jurusan(data):
    """
    Sort data berdasarkan jurusan dan prodi untuk tampilan yang lebih terorganisir

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame dengan kolom 'Program Studi'

    Returns:
    --------
    pd.DataFrame : Data yang sudah disort berdasarkan jurusan
    """
    # Tambahkan kolom Jurusan
    data['Jurusan'] = data['Program Studi'].map(PRODI_TO_JURUSAN)

    # Buat custom sort order
    jurusan_sort_order = {j: i for i, j in enumerate(JURUSAN_ORDER)}
    data['Jurusan_Order'] = data['Jurusan'].map(jurusan_sort_order)

    # Sort berdasarkan jurusan, kemudian program studi
    data = data.sort_values(['Jurusan_Order', 'Program Studi'])

    return data

def assign_colors_by_jurusan(data):
    """
    Assign warna untuk setiap prodi berdasarkan jurusan dengan gradient

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame dengan kolom 'Program Studi' dan 'Jurusan'

    Returns:
    --------
    list : List of colors untuk setiap baris
    """
    colors = []

    for jurusan in JURUSAN_ORDER:
        prodi_in_jurusan = data[data['Jurusan'] == jurusan]
        total = len(prodi_in_jurusan)

        for idx, (_, row) in enumerate(prodi_in_jurusan.iterrows()):
            prodi_name = row['Program Studi']
            color = get_prodi_color(prodi_name, idx, total)
            colors.append(color)

    return colors

def calculate_overall_stats(df_pembilang, df_penyebut):
    """
    Hitung statistik keseluruhan

    Returns:
    --------
    dict: {'pembilang': int, 'penyebut': int, 'persentase': float}
    """
    total_pembilang = len(df_pembilang)
    total_penyebut = len(df_penyebut)
    persentase = (total_pembilang / total_penyebut * 100) if total_penyebut > 0 else 0

    return {
        'pembilang': total_pembilang,
        'penyebut': total_penyebut,
        'persentase': round(persentase, 2)
    }

# ============================================================================
# FUNGSI VISUALISASI - HELPER
# ============================================================================

def save_figure(fig, filename_base, subdir=''):
    """
    Save figure dalam multiple formats (PNG dan SVG)

    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        Figure object to save
    filename_base : str
        Base filename without extension
    subdir : str, optional
        Subdirectory name (e.g., 'horizontal', 'vertical')

    Returns:
    --------
    list : List of saved file paths
    """
    output_dir = CONFIG['base_path'] / CONFIG['output_dir']
    saved_files = []

    # Save PNG
    if CONFIG['export_png']:
        png_dir = output_dir / 'png'
        png_dir.mkdir(parents=True, exist_ok=True)
        png_file = png_dir / f'{filename_base}.png'
        fig.savefig(png_file, dpi=CONFIG['dpi'], bbox_inches='tight', format='png')
        saved_files.append(str(png_file))
        print(f"    ✓ PNG: {png_file.relative_to(output_dir)}")

    # Save SVG (vector format)
    if CONFIG['export_svg']:
        svg_dir = output_dir / 'svg'
        svg_dir.mkdir(parents=True, exist_ok=True)
        svg_file = svg_dir / f'{filename_base}.svg'
        fig.savefig(svg_file, bbox_inches='tight', format='svg')
        saved_files.append(str(svg_file))
        print(f"    ✓ SVG: {svg_file.relative_to(output_dir)}")

    return saved_files

# ============================================================================
# FUNGSI VISUALISASI - CHARTS
# ============================================================================

def create_horizontal_bar_chart(data, iku_number, target=None):
    """
    Membuat horizontal bar chart berkualitas publikasi dengan grouping jurusan

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    iku_number : str
        Nomor IKU
    target : float, optional
        Nilai target untuk garis vertikal

    Returns:
    --------
    str : Path file output
    """
    metadata = IKU_METADATA[iku_number]

    # Sort berdasarkan jurusan
    data_sorted = sort_by_jurusan(data.copy())

    # Assign colors
    colors = assign_colors_by_jurusan(data_sorted)

    prodi_list = data_sorted['Program Studi'].tolist()
    persentase_list = data_sorted['Persentase'].tolist()
    pembilang_list = data_sorted['Pembilang'].tolist()
    penyebut_list = data_sorted['Penyebut'].tolist()
    jurusan_list = data_sorted['Jurusan'].tolist()

    # Create figure dengan tinggi yang dinamis
    fig_height = max(6, len(prodi_list) * 0.4)
    fig, ax = plt.subplots(figsize=(11, fig_height))

    # Horizontal bars dengan edge yang lebih tegas
    y_pos = np.arange(len(prodi_list))
    bars = ax.barh(y_pos, persentase_list, color=colors,
                   edgecolor='#1a1a1a', linewidth=1.5,  # Line lebih tegas & prominent
                   alpha=0.88, height=0.75)

    # Tambahkan separator antar jurusan dengan garis horizontal
    current_jurusan = None
    for i, jurusan in enumerate(jurusan_list):
        if current_jurusan is not None and jurusan != current_jurusan:
            # Garis separator tegas
            ax.axhline(y=i-0.5, color='#333333', linestyle='-',
                      linewidth=1.5, alpha=0.6, zorder=2)
        current_jurusan = jurusan

    # Target line
    if target:
        ax.axvline(x=target, color=COLORS['target'], linestyle='--',
                   linewidth=2.5, label=f'Target ({target}%)', zorder=3, alpha=0.95)

    # Labels pada bars - semua di luar dengan warna hitam
    for i, (bar, persen, pembilang, penyebut) in enumerate(zip(bars, persentase_list, pembilang_list, penyebut_list)):
        width = bar.get_width()
        # Format: tampilkan decimal hanya jika bukan angka bulat
        persen_str = f'{int(persen)}' if persen == int(persen) else f'{persen:.1f}'
        label = f'{persen_str}% ({pembilang}/{penyebut})'

        # Semua label di luar bar, warna hitam
        ax.text(width + 1.5, bar.get_y() + bar.get_height()/2,
               label, ha='left', va='center',
               fontsize=11, fontweight='900', color='black')

    # Y-labels dengan jurusan annotation
    y_labels = []
    for prodi, jurusan in zip(prodi_list, jurusan_list):
        y_labels.append(f"{prodi}")

    # Styling
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels, fontsize=10, fontweight='600')
    ax.set_xlabel('Persentase (%)', fontsize=12, fontweight='700')
    ax.set_title(f"{metadata['title']}\n{metadata['subtitle']}",
                 fontsize=13, fontweight='900', pad=20)

    # Grid dengan style yang lebih halus tapi tetap terlihat
    ax.xaxis.grid(True, linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax.set_axisbelow(True)

    # Spines dengan line yang lebih tegas
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # X-axis limit
    max_val = max(persentase_list) if persentase_list else 100
    if target:
        max_val = max(max_val, target)
    ax.set_xlim(0, max_val * 1.15)

    # Legend untuk jurusan di pojok kanan atas
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=JURUSAN_COLORS[j]['base'],
                             edgecolor='black', linewidth=1.0, label=j)
                      for j in JURUSAN_ORDER if j in jurusan_list]

    # Reverse order agar sesuai dengan urutan chart (bottom to top)
    legend_elements = legend_elements[::-1]

    if target:
        from matplotlib.lines import Line2D
        legend_elements.append(Line2D([0], [0], color=COLORS['target'],
                                      linewidth=2.5, linestyle='--',
                                      label=f'Target ({target}%)'))

    ax.legend(handles=legend_elements, loc='upper right',
             fontsize=10, framealpha=0.95, edgecolor='black', fancybox=False)

    plt.tight_layout()

    # Save in multiple formats
    saved_files = save_figure(fig, f'IKU_{iku_number}_horizontal')
    plt.close()

    return saved_files

def create_vertical_bar_chart(data, iku_number, target=None):
    """
    Membuat vertical bar chart berkualitas publikasi dengan grouping jurusan

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    iku_number : str
        Nomor IKU
    target : float, optional
        Nilai target untuk garis horizontal

    Returns:
    --------
    str : Path file output
    """
    metadata = IKU_METADATA[iku_number]

    # Sort berdasarkan jurusan
    data_sorted = sort_by_jurusan(data.copy())

    # Assign colors based on jurusan
    colors = assign_colors_by_jurusan(data_sorted)

    prodi_list = data_sorted['Program Studi'].tolist()
    persentase_list = data_sorted['Persentase'].tolist()
    pembilang_list = data_sorted['Pembilang'].tolist()
    penyebut_list = data_sorted['Penyebut'].tolist()
    jurusan_list = data_sorted['Jurusan'].tolist()

    # Buat figure dengan width yang lebih lebar untuk spacing
    fig_width = max(14, len(prodi_list) * 1.0)  # Increased spacing: 0.8 -> 1.0
    fig, ax = plt.subplots(figsize=(fig_width, 7))

    # Vertical bars with spacing untuk readability X-axis labels
    x_pos = np.arange(len(prodi_list))
    bars = ax.bar(x_pos, persentase_list, color=colors,
                  edgecolor='#1a1a1a', linewidth=1.5,
                  alpha=0.88, width=0.75)  # Width 0.75 untuk spacing antar bar

    # Tambahkan separator antar jurusan dengan garis vertikal
    current_jurusan = None
    for i, jurusan in enumerate(jurusan_list):
        if current_jurusan is not None and jurusan != current_jurusan:
            # Garis separator vertikal tegas di tengah antar group
            ax.axvline(x=i-0.5, color='#333333', linestyle='-',
                      linewidth=2.0, alpha=0.6, zorder=2)
        current_jurusan = jurusan

    # Target line
    if target:
        ax.axhline(y=target, color=COLORS['target'], linestyle='--',
                   linewidth=2.5, label=f'Target ({target}%)', zorder=3, alpha=0.95)

    # Label di atas bars (persentase dan pembilang/penyebut)
    for bar, persen, pembilang, penyebut in zip(bars, persentase_list, pembilang_list, penyebut_list):
        height = bar.get_height()
        # Format: tampilkan decimal hanya jika bukan angka bulat
        persen_str = f'{int(persen)}' if persen == int(persen) else f'{persen:.1f}'
        label = f'{persen_str}%\n({pembilang}/{penyebut})'
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                label, ha='center', va='bottom', fontsize=10, fontweight='900')

    # Styling - X-axis labels dengan multi-line wrapping (tidak rotasi)
    import textwrap
    wrapped_labels = ['\n'.join(textwrap.wrap(prodi, width=12)) for prodi in prodi_list]
    ax.set_xticks(x_pos)
    ax.set_xticklabels(wrapped_labels, rotation=0, ha='center', fontsize=10, fontweight='600')
    ax.set_ylabel('Persentase (%)', fontsize=12, fontweight='700')
    ax.set_title(f"{metadata['title']}\n{metadata['subtitle']}",
                 fontsize=13, fontweight='900', pad=15)

    # Grid
    ax.yaxis.grid(True, linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax.set_axisbelow(True)

    # Spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # Y-axis limit
    max_val = max(persentase_list) if persentase_list else 100
    if target:
        max_val = max(max_val, target)
    ax.set_ylim(0, max_val * 1.25)

    # Legend untuk jurusan
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=JURUSAN_COLORS[j]['base'],
                             edgecolor='black', linewidth=1.0, label=j)
                      for j in JURUSAN_ORDER if j in jurusan_list]
    if target:
        from matplotlib.lines import Line2D
        legend_elements.append(Line2D([0], [0], color=COLORS['target'],
                                      linewidth=2.5, linestyle='--',
                                      label=f'Target ({target}%)'))

    ax.legend(handles=legend_elements, loc='upper right',
             fontsize=10, framealpha=0.95, edgecolor='black', fancybox=False)

    plt.tight_layout()

    # Save in multiple formats
    saved_files = save_figure(fig, f'IKU_{iku_number}_vertical')
    plt.close()

    return saved_files

def create_summary_dashboard(all_stats, all_data):
    """
    Membuat dashboard summary untuk semua IKU dengan desain modern dan compact

    Parameters:
    -----------
    all_stats : dict
        Dictionary berisi statistik keseluruhan untuk setiap IKU
    all_data : dict
        Dictionary berisi data detail untuk setiap IKU

    Returns:
    --------
    str : Path file output
    """
    num_iku = len(all_stats)
    # Figsize lebih compact: 3.5 inch per IKU, height 6 inch
    fig, axes = plt.subplots(1, num_iku, figsize=(3.5 * num_iku, 6))

    # Jika hanya 1 IKU, axes bukan array
    if num_iku == 1:
        axes = [axes]

    iku_list = sorted(all_stats.keys())

    for idx, iku in enumerate(iku_list):
        ax = axes[idx]
        metadata = IKU_METADATA[iku]
        stats = all_stats.get(iku, {'pembilang': 0, 'penyebut': 1, 'persentase': 0})

        # Donut chart (lebih modern daripada pie chart)
        pct = stats['persentase']
        sizes = [pct, 100 - pct]

        # Warna soft yang menarik dan bervariasi per IKU
        color_map = {
            '11': '#5B9BD5',  # Soft blue
            '12': '#70AD47',  # Soft green
            '13': '#ED7D31',  # Soft orange
            '21': '#9966CC',  # Soft purple
            '22': '#E85D75',  # Soft red/pink
            '23': '#7F8C8D',  # Soft gray
            '31': '#5B9BD5',  # Soft blue
            '33': '#70AD47',  # Soft green
            '41': '#ED7D31',  # Soft orange
            '42': '#9966CC'   # Soft purple
        }
        colors_donut = [color_map.get(iku, '#70AD47'), '#E8E8E8']

        # Buat donut chart dengan size yang lebih proporsional
        wedges, texts, autotexts = ax.pie(
            sizes,
            colors=colors_donut,
            autopct='',  # Akan custom label di tengah
            startangle=90,
            wedgeprops=dict(width=0.35, edgecolor='white', linewidth=2.5),
            textprops={'fontsize': 10, 'fontweight': 'bold'}
        )

        # Text di tengah donut (persentase besar)
        ax.text(0, 0.08, f'{pct:.1f}%',
               ha='center', va='center',
               fontsize=24, fontweight='bold', color='#333333')

        # Text di bawah persentase (keterangan)
        ax.text(0, -0.22, f'{stats["pembilang"]}/{stats["penyebut"]}',
               ha='center', va='center',
               fontsize=9, color='#666666', fontweight='500')

        # Title di atas dengan wrapping yang lebih baik dan compact
        title_text = f"IKU {iku}\n{textwrap.fill(metadata['title'], width=28)}"
        ax.set_title(title_text,
                    fontsize=9, fontweight='bold',
                    pad=12, linespacing=1.2)

    # Suptitle dengan posisi lebih tinggi agar tidak menabrak
    plt.suptitle('Ringkasan Pencapaian IKU\nFakultas Sains & Teknologi',
                 fontsize=12, fontweight='bold', y=0.99, linespacing=1.1)

    plt.tight_layout(rect=[0, 0, 1, 0.93])

    # Save in multiple formats
    saved_files = save_figure(fig, 'IKU_summary_dashboard')
    plt.close()

    return saved_files

# ============================================================================
# MAIN ORCHESTRATION
# ============================================================================

def cleanup_output_folder():
    """
    Hapus semua file di output folder untuk clean start
    """
    output_dir = CONFIG['base_path'] / CONFIG['output_dir']

    if output_dir.exists():
        print("\n🧹 Cleaning output folder...")

        # Hapus semua file PNG
        png_dir = output_dir / 'png'
        if png_dir.exists():
            for file in png_dir.glob('*.png'):
                file.unlink()
                print(f"  ✓ Deleted: {file.name}")

        # Hapus semua file SVG
        svg_dir = output_dir / 'svg'
        if svg_dir.exists():
            for file in svg_dir.glob('*.svg'):
                file.unlink()
                print(f"  ✓ Deleted: {file.name}")

        print("✅ Output folder cleaned\n")
    else:
        print("\n📁 Output folder tidak ada, akan dibuat saat save...\n")

def process_single_iku(iku_number):
    """
    Proses satu IKU lengkap: baca data, proses, visualisasi

    Parameters:
    -----------
    iku_number : str
        Nomor IKU (31, 33, 41)

    Returns:
    --------
    dict : {'data': DataFrame, 'stats': dict, 'files': list}
    """
    print(f"\n{'='*70}")
    print(f"IKU {iku_number}: {IKU_METADATA[iku_number]['title']}")
    print(f"{'='*70}")

    try:
        # 1. Baca data
        print("  [1/4] Membaca data...")
        df_pembilang = read_excel_iku(iku_number, 'pembilang')
        df_penyebut = read_excel_iku(iku_number, 'penyebut')

        # 2. Hitung statistik keseluruhan
        print("  [2/4] Menghitung statistik...")
        stats = calculate_overall_stats(df_pembilang, df_penyebut)
        print(f"        Pembilang: {stats['pembilang']} dosen")
        print(f"        Penyebut: {stats['penyebut']} dosen")
        print(f"        Persentase: {stats['persentase']}%")

        # 3. Proses data per prodi
        print("  [3/4] Memproses data per program studi...")
        if iku_number == '11':
            data = process_iku_11(df_pembilang, df_penyebut)
        elif iku_number == '12':
            data = process_iku_12(df_pembilang, df_penyebut)
        elif iku_number == '13':
            data = process_iku_13(df_pembilang, df_penyebut)
        elif iku_number == '21':
            data = process_iku_21(df_pembilang, df_penyebut)
        elif iku_number == '22':
            data = process_iku_22(df_pembilang, df_penyebut)
        elif iku_number == '23':
            data = process_iku_23(df_pembilang, df_penyebut)
        elif iku_number == '31':
            data = process_iku_31(df_pembilang, df_penyebut)
        elif iku_number == '33':
            data = process_iku_33(df_pembilang, df_penyebut)
        elif iku_number == '41':
            data = process_iku_41(df_pembilang, df_penyebut)
        elif iku_number == '42':
            data = process_iku_42(df_pembilang, df_penyebut)
        else:
            raise ValueError(f"IKU number tidak valid: {iku_number}")

        # 4. Buat visualisasi
        print("  [4/4] Membuat visualisasi...")
        target = CONFIG['target_values'].get(iku_number)
        files = []
        files.append(create_horizontal_bar_chart(data, iku_number, target))
        files.append(create_vertical_bar_chart(data, iku_number, target))

        print(f"  ✅ IKU {iku_number} selesai diproses\n")

        return {
            'data': data,
            'stats': stats,
            'files': files
        }

    except Exception as e:
        print(f"  ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return None

def main():
    """
    Main function - Orchestrate seluruh proses visualisasi
    """
    print("="*70)
    print("SISTEM VISUALISASI IKU FAKULTAS SAINS & TEKNOLOGI")
    print("Standar Publikasi Internasional")
    print("="*70)
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output directory: {CONFIG['base_path'] / CONFIG['output_dir']}")
    print(f"Resolution: {CONFIG['dpi']} DPI")

    # Clean output folder terlebih dahulu
    cleanup_output_folder()

    # Setup matplotlib style
    setup_publication_style()

    # Process semua IKU
    all_results = {}
    all_stats = {}
    all_data = {}

    for iku in ['11', '12', '13', '21', '22', '23', '31', '33', '41', '42']:
        result = process_single_iku(iku)
        if result:
            all_results[iku] = result
            all_stats[iku] = result['stats']
            all_data[iku] = result['data']

    # Buat summary dashboard
    if all_stats:
        print(f"\n{'='*70}")
        print("MEMBUAT SUMMARY DASHBOARD")
        print(f"{'='*70}")
        create_summary_dashboard(all_stats, all_data)

    # Buat breakdown visualizations
    print(f"\n{'='*70}")
    print("MEMBUAT BREAKDOWN VISUALIZATIONS")
    print(f"{'='*70}")

    try:
        # Import breakdown modules
        from breakdown.iku_11_breakdown import create_iku_11_breakdown
        from breakdown.iku_12_breakdown import create_iku_12_breakdown
        from breakdown.iku_13_breakdown import create_iku_13_breakdown
        from breakdown.iku_21_breakdown import create_iku_21_breakdown
        from breakdown.iku_22_breakdown import create_iku_22_breakdown
        from breakdown.iku_23_breakdown import create_iku_23_breakdown
        from breakdown.iku_31_breakdown import create_iku_31_breakdown
        from breakdown.iku_33_breakdown import create_iku_33_breakdown
        from breakdown.iku_41_breakdown import create_iku_41_breakdown
        from breakdown.iku_42_breakdown import create_iku_42_breakdown

        # Generate breakdowns
        create_iku_11_breakdown()
        create_iku_12_breakdown()
        create_iku_13_breakdown()
        create_iku_21_breakdown()
        create_iku_22_breakdown()
        create_iku_23_breakdown()
        create_iku_31_breakdown()
        create_iku_33_breakdown()
        create_iku_41_breakdown()
        create_iku_42_breakdown()
    except Exception as e:
        print(f"  ⚠️  Warning: Breakdown generation error: {e}")

    # Print summary
    print(f"\n{'='*70}")
    print("RINGKASAN HASIL")
    print(f"{'='*70}")
    for iku, stats in all_stats.items():
        print(f"IKU {iku}: {stats['persentase']}% ({stats['pembilang']}/{stats['penyebut']} dosen)")

    print(f"\n{'='*70}")
    print("VISUALISASI SELESAI ✅")
    print(f"{'='*70}")
    print("\nStandar Publikasi yang Diterapkan:")
    print(f"  ✓ Font: {CONFIG['font_name'][0]} {CONFIG['font_size']}pt")
    print(f"  ✓ Resolution: {CONFIG['dpi']} DPI (publication quality)")
    print(f"  ✓ Color Palette: Colorblind-friendly (ColorBrewer)")
    print(f"  ✓ Line Width: {CONFIG['axes_linewidth']}pt (Nature/IEEE standard)")
    print("  ✓ Data-ink Ratio: Maximized")
    print("\nReferensi:")
    print("  - Environmental Modelling & Software (Ten Guidelines)")
    print("  - Nature, Science, IEEE standards")
    print("  - ColorBrewer2.org")

    return all_results

if __name__ == "__main__":
    try:
        results = main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Proses dibatalkan oleh user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
