"""
============================================================================
UTILITY FUNCTIONS - SISTEM VISUALISASI IKU
============================================================================

Modul ini berisi fungsi utility untuk sistem visualisasi IKU.

Author: Tim IKU FST
Version: 2.0 (Modular)
Last Updated: 2026-01-07
============================================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import CONFIG, PRODI_TO_JURUSAN, JURUSAN_ORDER, JURUSAN_COLORS


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
# FILE I/O FUNCTIONS
# ============================================================================

def read_excel_iku(iku_number, file_type='pembilang'):
    """
    Membaca file Excel IKU

    Parameters:
    -----------
    iku_number : str
        Nomor IKU (11, 12, 13, 21, 22, 23, 31, 33, 41, 42)
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


# ============================================================================
# DATA PROCESSING HELPERS
# ============================================================================

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
