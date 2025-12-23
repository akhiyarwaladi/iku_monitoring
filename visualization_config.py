"""
============================================================================
SHARED CONFIGURATION & UTILITIES
Untuk Sistem Visualisasi IKU Fakultas Sains & Teknologi
============================================================================
File ini berisi konfigurasi dan fungsi utility yang digunakan bersama
oleh semua script visualisasi dan breakdown.
============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# KONFIGURASI GLOBAL
# ============================================================================

BASE_PATH = Path(__file__).parent
OUTPUT_DIR = BASE_PATH / 'output'

CONFIG = {
    # Publication settings
    'dpi': 300,
    'font_size': 9,
    'font_family': 'sans-serif',
    'font_name': ['Arial', 'Helvetica', 'DejaVu Sans'],

    # Export formats
    'export_png': True,
    'export_svg': True,

    # Line widths
    'axes_linewidth': 0.75,
    'grid_linewidth': 0.5,
    'bar_linewidth': 1.2,
}

# ============================================================================
# COLOR PALETTES
# ============================================================================

# Warna soft tapi tetap tegas per Jurusan
JURUSAN_COLORS = {
    'MIPA': {
        'base': '#5B9BD5',
        'light': '#9DC3E6',
        'dark': '#2E75B6'
    },
    'Teknik Geologi': {
        'base': '#ED7D31',
        'light': '#F4B183',
        'dark': '#C65911'
    },
    'Teknik Kimia': {
        'base': '#70AD47',
        'light': '#A8D08D',
        'dark': '#548235'
    },
    'Teknik Sipil': {
        'base': '#9966CC',
        'light': '#C5A8E0',
        'dark': '#7030A0'
    },
    'Teknik Elektro': {
        'base': '#E85D75',
        'light': '#F4A6B7',
        'dark': '#C13552'
    },
    'D3': {
        'base': '#7F8C8D',
        'light': '#BDC3C7',
        'dark': '#5D6D7E'
    },
    # Nama lengkap jurusan (untuk compatibility dengan raw data)
    'Jurusan Matematika dan Ilmu Pengetahuan Alam': {
        'base': '#5B9BD5',
        'light': '#9DC3E6',
        'dark': '#2E75B6'
    },
    'Jurusan Teknik Kebumian': {
        'base': '#ED7D31',
        'light': '#F4B183',
        'dark': '#C65911'
    },
    'Jurusan Teknik Sipil, Kimia dan Lingkungan': {
        'base': '#70AD47',
        'light': '#A8D08D',
        'dark': '#548235'
    },
    'Jurusan Teknik Elektro dan Informatika': {
        'base': '#E85D75',
        'light': '#F4A6B7',
        'dark': '#C13552'
    }
}

# Mapping Program Studi ke Jurusan
PRODI_TO_JURUSAN = {
    'Matematika': 'MIPA',
    'Biologi': 'MIPA',
    'Fisika': 'MIPA',
    'Kimia': 'MIPA',
    'Teknik Geofisika': 'Teknik Geologi',
    'Teknik Geologi': 'Teknik Geologi',
    'Teknik Kimia': 'Teknik Kimia',
    'Teknik Lingkungan': 'Teknik Kimia',
    'Teknik Sipil': 'Teknik Sipil',
    'Teknik Pertambangan': 'Teknik Sipil',
    'Teknik Elektro': 'Teknik Elektro',
    'Sistem Informasi': 'Teknik Elektro',
    'Informatika': 'Teknik Elektro',
    'Analis Kimia (D3)': 'D3',
    'Kimia Industri (D3)': 'D3',
}

# Urutan Jurusan
JURUSAN_ORDER = ['MIPA', 'Teknik Geologi', 'Teknik Kimia', 'Teknik Sipil', 'Teknik Elektro', 'D3']

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def setup_publication_style():
    """Setup matplotlib style untuk publikasi"""
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

def save_figure(fig, filename_base):
    """
    Save figure dalam multiple formats (PNG dan SVG)

    Parameters:
    -----------
    fig : matplotlib.figure.Figure
    filename_base : str (tanpa extension)

    Returns:
    --------
    list : List of saved file paths
    """
    saved_files = []

    # Save PNG
    if CONFIG['export_png']:
        png_dir = OUTPUT_DIR / 'png'
        png_dir.mkdir(parents=True, exist_ok=True)
        png_file = png_dir / f'{filename_base}.png'
        fig.savefig(png_file, dpi=CONFIG['dpi'], bbox_inches='tight', format='png')
        saved_files.append(str(png_file))
        print(f"    ✓ PNG: {png_file.relative_to(OUTPUT_DIR)}")

    # Save SVG
    if CONFIG['export_svg']:
        svg_dir = OUTPUT_DIR / 'svg'
        svg_dir.mkdir(parents=True, exist_ok=True)
        svg_file = svg_dir / f'{filename_base}.svg'
        fig.savefig(svg_file, bbox_inches='tight', format='svg')
        saved_files.append(str(svg_file))
        print(f"    ✓ SVG: {svg_file.relative_to(OUTPUT_DIR)}")

    return saved_files

def get_prodi_color(prodi_name, index_in_jurusan=0, total_in_jurusan=1):
    """Generate warna untuk prodi berdasarkan jurusan"""
    jurusan = PRODI_TO_JURUSAN.get(prodi_name, 'MIPA')
    colors = JURUSAN_COLORS[jurusan]

    if total_in_jurusan == 1:
        return colors['base']

    if index_in_jurusan == 0:
        return colors['dark']
    elif index_in_jurusan == total_in_jurusan - 1:
        return colors['light']
    else:
        return colors['base']

def normalize_prodi_name(prodi_name):
    """
    Normalisasi nama Program Studi untuk konsistensi

    Menghapus prefix "Program Studi " dan mempertahankan format standar
    dengan suffix (D3) jika ada.

    Examples:
    ---------
    "Program Studi Kimia" -> "Kimia"
    "Kimia" -> "Kimia"
    "Program Studi Analis Kimia (D3)" -> "Analis Kimia (D3)"
    "Analis Kimia" -> "Analis Kimia (D3)"
    """
    if pd.isna(prodi_name):
        return prodi_name

    # Remove "Program Studi " prefix
    normalized = str(prodi_name).replace('Program Studi ', '')

    # Ensure D3 programs have (D3) suffix
    d3_programs = ['Analis Kimia', 'Kimia Industri']
    for d3_prog in d3_programs:
        if normalized == d3_prog or normalized.startswith(d3_prog + ' '):
            if '(D3)' not in normalized:
                normalized = d3_prog + ' (D3)'
            break

    return normalized

def read_excel_iku(iku_number, file_type='pembilang'):
    """
    Membaca file Excel IKU dengan normalisasi Program Studi

    Parameters:
    -----------
    iku_number : str (31, 33, 41, 42)
    file_type : str ('pembilang' atau 'penyebut')

    Returns:
    --------
    pd.DataFrame
    """
    file_path = BASE_PATH / f'monitoring-iku-{iku_number}-{file_type}.xlsx'

    if not file_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")

    df = pd.read_excel(file_path, header=1)

    # Normalisasi kolom Program Studi jika ada
    if 'Program Studi' in df.columns:
        df['Program Studi'] = df['Program Studi'].apply(normalize_prodi_name)

    return df
