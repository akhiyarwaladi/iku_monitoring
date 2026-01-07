"""
============================================================================
IKU 22 BREAKDOWN: Mahasiswa yang Meraih Prestasi
============================================================================
Visualisasi breakdown untuk IKU 22:
1. Statistik Summary - Distribusi Tingkat Prestasi dan Top Kegiatan
============================================================================
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import textwrap
from visualization_config import (
    read_excel_iku, setup_publication_style, save_figure,
    JURUSAN_COLORS, PRODI_TO_JURUSAN, BREAKDOWN_STYLE, JURUSAN_ORDER
)


def get_jurusan_short(prodi):
    """Map prodi to short jurusan name"""
    # Handle NaN values
    if pd.isna(prodi):
        return 'MIPA'
    # Remove 'Program Studi ' prefix if exists
    prodi_clean = str(prodi).replace('Program Studi ', '')
    return PRODI_TO_JURUSAN.get(prodi_clean, 'MIPA')


def create_iku_22_statistik(df_pembilang, df_penyebut):
    """Chart: Statistik Summary - Tingkat Prestasi dan Pencapaian"""

    # Data processing
    total_prestasi = len(df_pembilang)
    total_mahasiswa = len(df_penyebut)
    persentase = (total_prestasi / total_mahasiswa * 100) if total_mahasiswa > 0 else 0

    # Join pembilang dengan penyebut untuk dapat Program Studi
    df_pembilang_enriched = df_pembilang.merge(
        df_penyebut[['NIM', 'Program Studi']],
        on='NIM',
        how='left'
    )

    # Map prodi to jurusan
    df_pembilang_enriched['Jurusan_Short'] = df_pembilang_enriched['Program Studi'].apply(get_jurusan_short)

    # Create figure with better proportions
    style = BREAKDOWN_STYLE
    fig_height = 8

    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=(20, fig_height))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1.2, 1.5], wspace=0.25)

    ax1 = fig.add_subplot(gs[0])  # Left: Pie chart - Tingkat Prestasi
    ax2 = fig.add_subplot(gs[1])  # Right: Bar chart - Pencapaian

    # LEFT CHART - Tingkat Prestasi Distribution (Pie Chart)
    # Clean tingkat data - remove 'Tingkat ' prefix
    df_pembilang_enriched['Tingkat_Clean'] = df_pembilang_enriched['Tingkat'].str.replace('Tingkat ', '')
    tingkat_counts = df_pembilang_enriched['Tingkat_Clean'].value_counts()

    # Define colors for tingkat (Internasional > Nasional > Provinsi > Universitas)
    tingkat_colors = {
        'Internasional': '#FFC000',  # Gold (highest)
        'Nasional': '#70AD47',       # Green (national)
        'Provinsi': '#5B9BD5',       # Blue (provincial)
        'Universitas': '#ED7D31'     # Orange (university)
    }

    # Order by importance
    tingkat_order = ['Internasional', 'Nasional', 'Provinsi', 'Universitas']
    tingkat_data = []
    tingkat_labels = []
    colors_pie = []

    for tingkat in tingkat_order:
        if tingkat in tingkat_counts.index:
            tingkat_data.append(tingkat_counts[tingkat])
            tingkat_labels.append(tingkat)
            colors_pie.append(tingkat_colors.get(tingkat, '#999999'))

    # Create pie chart with better styling
    explode = [0.05] * len(tingkat_data)  # Slight explode for all slices

    wedges, texts, autotexts = ax1.pie(
        tingkat_data,
        labels=tingkat_labels,
        colors=colors_pie,
        autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100.*sum(tingkat_data))})',
        startangle=90,
        explode=explode,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2.5, 'alpha': 0.9},
        textprops={'fontsize': 11, 'fontweight': '700'}
    )

    # Style autopct text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_fontweight('900')

    # Style labels
    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('700')

    ax1.set_title(f'Distribusi Tingkat Prestasi\nTotal: {total_prestasi} prestasi',
                  fontsize=14, fontweight='900', pad=20)

    # RIGHT CHART - Distribusi Pencapaian
    pencapaian_counts = df_pembilang_enriched['Pencapaian'].value_counts()

    # Define order and colors for pencapaian
    pencapaian_order = ['Juara 1', 'Juara 2', 'Juara 3', 'Harapan 1', 'Harapan 2', 'Peserta']
    pencapaian_colors_map = {
        'Juara 1': '#FFC000',    # Gold
        'Juara 2': '#C0C0C0',    # Silver
        'Juara 3': '#CD7F32',    # Bronze
        'Harapan 1': '#70AD47',  # Green
        'Harapan 2': '#5B9BD5',  # Blue
        'Peserta': '#ED7D31'     # Orange
    }

    pencapaian_data = []
    pencapaian_labels = []
    colors_bar = []

    for pencapaian in pencapaian_order:
        if pencapaian in pencapaian_counts.index:
            pencapaian_data.append(pencapaian_counts[pencapaian])
            pencapaian_labels.append(pencapaian)
            colors_bar.append(pencapaian_colors_map.get(pencapaian, '#999999'))

    x_pos = np.arange(len(pencapaian_data))

    bars = ax2.bar(x_pos, pencapaian_data,
                   color=colors_bar, edgecolor='#1a1a1a',
                   linewidth=1.5, alpha=0.9, width=0.65)

    # Labels on top of bars
    max_count_right = max(pencapaian_data)
    for bar, count in zip(bars, pencapaian_data):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height + max_count_right * 0.02,
                f'{int(count)}', ha='center', va='bottom',
                fontsize=11, fontweight='900', color='#2c3e50')

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(pencapaian_labels, fontsize=11, fontweight='600', rotation=0)
    ax2.set_ylabel('Jumlah Prestasi', fontsize=13, fontweight='700')
    ax2.set_title('Distribusi Pencapaian\nMahasiswa Berprestasi',
                  fontsize=14, fontweight='900', pad=20)
    ax2.yaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0, color='#bdc3c7')
    ax2.set_axisbelow(True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_linewidth(1.8)
    ax2.spines['bottom'].set_linewidth(1.8)
    ax2.spines['left'].set_color('#7f8c8d')
    ax2.spines['bottom'].set_color('#7f8c8d')

    # Set ylim with proper padding
    ax2.set_ylim(0, max_count_right * 1.15)

    # Main title with better positioning
    main_title = (f'IKU 22: Statistik Summary - Mahasiswa yang Meraih Prestasi\n'
                  f'Total: {total_prestasi} prestasi '
                  f'({persentase:.1f}% dari {total_mahasiswa} mahasiswa FST)')
    fig.suptitle(main_title, fontsize=15, fontweight='900', y=0.96)

    plt.tight_layout(rect=[0, 0.02, 1, 0.90])

    saved_files = save_figure(fig, 'IKU_22_breakdown_statistik')
    plt.close()

    return saved_files


def create_iku_22_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 22"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 22...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('22', 'pembilang')
    df_penyebut = read_excel_iku('22', 'penyebut')

    # Generate chart
    all_files = []

    print("    → Statistik Summary (Tingkat & Pencapaian Prestasi)...")
    all_files.extend(create_iku_22_statistik(df_pembilang, df_penyebut))

    print(f"  ✅ Breakdown IKU 22 selesai (1 chart)")
    return all_files


if __name__ == "__main__":
    create_iku_22_breakdown()
