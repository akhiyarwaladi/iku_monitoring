"""
============================================================================
IKU 13 BREAKDOWN: Lulusan yang Berwiraswasta
============================================================================
Visualisasi breakdown untuk IKU 13:
1. Statistik Summary - Distribusi Masa Tunggu dan Jenjang Pendidikan
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
    return PRODI_TO_JURUSAN.get(prodi, 'MIPA')


def create_iku_13_statistik(df_pembilang, df_penyebut):
    """Chart: Statistik Summary - Masa Tunggu dan Jenjang Pendidikan"""

    # Data processing
    total_lulusan_wirausaha = len(df_pembilang)
    total_lulusan = len(df_penyebut)
    persentase = (total_lulusan_wirausaha / total_lulusan * 100) if total_lulusan > 0 else 0

    # Map prodi to jurusan
    df_pembilang['Jurusan_Short'] = df_pembilang['Prodi'].apply(get_jurusan_short)

    # Process Masa Tunggu distribution
    # Filter out NaN values
    masa_tunggu_counts = df_pembilang['Masa Tunggu'].dropna().value_counts()

    # Create figure with better proportions
    style = BREAKDOWN_STYLE
    fig_height = 8

    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=(20, fig_height))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1.2, 1.5], wspace=0.25)

    ax1 = fig.add_subplot(gs[0])  # Left: Pie chart - Masa Tunggu
    ax2 = fig.add_subplot(gs[1])  # Right: Bar chart - Jenjang Pendidikan

    # LEFT CHART - Masa Tunggu Distribution (Pie Chart)
    # Define colors for masa tunggu categories
    masa_tunggu_colors = {
        '< 6 Bulan': '#70AD47',  # Green (good - quick to start)
        '> 6 Bulan': '#ED7D31',  # Orange (longer wait)
        '0': '#E85D75'           # Red (if any)
    }

    # Prepare data
    masa_tunggu_order = ['< 6 Bulan', '> 6 Bulan', '0']
    masa_tunggu_data = []
    colors_pie = []

    for mt in masa_tunggu_order:
        if mt in masa_tunggu_counts.index:
            masa_tunggu_data.append(masa_tunggu_counts[mt])
            colors_pie.append(masa_tunggu_colors[mt])

    # Create pie chart with better styling
    explode = [0.05] * len(masa_tunggu_data)  # Slight explode for all slices

    wedges, texts, autotexts = ax1.pie(
        masa_tunggu_data,
        labels=masa_tunggu_order[:len(masa_tunggu_data)],
        colors=colors_pie,
        autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100.*sum(masa_tunggu_data))})',
        startangle=140,
        explode=explode,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2.5, 'alpha': 0.9},
        textprops={'fontsize': 11, 'fontweight': '700'}
    )

    # Style autopct text (percentages)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_fontweight('900')

    # Style labels
    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('700')

    total_with_masa_tunggu = int(sum(masa_tunggu_data))
    ax1.set_title(f'Masa Tunggu Memulai Wirausaha\nTotal: {total_with_masa_tunggu} lulusan',
                  fontsize=14, fontweight='900', pad=20)

    # RIGHT CHART - Distribusi per Jenjang Pendidikan
    jenjang_counts = df_pembilang['Jenjang Pendidikan'].value_counts()

    # Define colors for jenjang
    jenjang_colors = {
        'S1': '#5B9BD5',  # Blue
        'S2': '#70AD47',  # Green
        'S3': '#FFC000',  # Gold
        'D3': '#ED7D31',  # Orange
        'D4': '#A5A5A5'   # Gray
    }

    # Sort by importance (S3 > S2 > S1 > D4 > D3)
    jenjang_order = ['S3', 'S2', 'S1', 'D4', 'D3']
    jenjang_data = []
    jenjang_labels = []
    colors_bar = []

    for jenjang in jenjang_order:
        if jenjang in jenjang_counts.index:
            jenjang_data.append(jenjang_counts[jenjang])
            jenjang_labels.append(jenjang)
            colors_bar.append(jenjang_colors.get(jenjang, '#999999'))

    x_pos = np.arange(len(jenjang_data))

    bars = ax2.bar(x_pos, jenjang_data,
                   color=colors_bar, edgecolor='#1a1a1a',
                   linewidth=1.5, alpha=0.9, width=0.6)

    # Labels on top of bars
    max_count_right = max(jenjang_data)
    for bar, count in zip(bars, jenjang_data):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height + max_count_right * 0.02,
                f'{int(count)}', ha='center', va='bottom',
                fontsize=11, fontweight='900', color='#2c3e50')

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(jenjang_labels, fontsize=12, fontweight='600', rotation=0)
    ax2.set_ylabel('Jumlah Lulusan Berwiraswasta', fontsize=13, fontweight='700')
    ax2.set_title('Distribusi Lulusan Berwiraswasta\nper Jenjang Pendidikan',
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
    main_title = (f'IKU 13: Statistik Summary - Lulusan yang Berwiraswasta\n'
                  f'Total: {total_lulusan_wirausaha} lulusan berwiraswasta '
                  f'({persentase:.1f}% dari {total_lulusan} lulusan FST)')
    fig.suptitle(main_title, fontsize=15, fontweight='900', y=0.97)

    plt.tight_layout(rect=[0, 0, 1, 0.93])

    saved_files = save_figure(fig, 'IKU_13_breakdown_statistik')
    plt.close()

    return saved_files


def create_iku_13_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 13"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 13...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('13', 'pembilang')
    df_penyebut = read_excel_iku('13', 'penyebut')

    # Generate chart
    all_files = []

    print("    → Statistik Summary (Masa Tunggu & Jenjang Pendidikan)...")
    all_files.extend(create_iku_13_statistik(df_pembilang, df_penyebut))

    print(f"  ✅ Breakdown IKU 13 selesai (1 chart)")
    return all_files


if __name__ == "__main__":
    create_iku_13_breakdown()
