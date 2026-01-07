"""
============================================================================
IKU 11 BREAKDOWN: Lulusan yang Memiliki Pekerjaan
============================================================================
Visualisasi breakdown untuk IKU 11:
1. Statistik Summary - Distribusi Masa Tunggu dan Top Prodi
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


def create_iku_11_statistik(df_pembilang, df_penyebut):
    """Chart: Statistik Summary - Masa Tunggu dan Top Prodi"""

    # Data processing
    total_lulusan_bekerja = len(df_pembilang)
    total_lulusan = len(df_penyebut)
    persentase = (total_lulusan_bekerja / total_lulusan * 100) if total_lulusan > 0 else 0

    # Map prodi to jurusan
    df_pembilang['Jurusan_Short'] = df_pembilang['Prodi'].apply(get_jurusan_short)

    # Process Masa Tunggu distribution
    masa_tunggu_counts = df_pembilang['Masa Tunggu'].value_counts()

    # Create figure with better proportions
    style = BREAKDOWN_STYLE
    fig_height = 8

    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=(20, fig_height))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1.2, 1.5], wspace=0.25)

    ax1 = fig.add_subplot(gs[0])  # Left: Pie chart - Masa Tunggu
    ax2 = fig.add_subplot(gs[1])  # Right: Bar chart - Top 10 Prodi

    # LEFT CHART - Masa Tunggu Distribution (Pie Chart)
    # Define colors for masa tunggu categories
    masa_tunggu_colors = {
        '< 6 Bulan': '#70AD47',  # Green (good)
        '> 6 Bulan': '#ED7D31',  # Orange (moderate)
        '0': '#E85D75'           # Red (not ideal)
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

    ax1.set_title(f'Distribusi Masa Tunggu Kerja\nTotal: {total_lulusan_bekerja} lulusan',
                  fontsize=14, fontweight='900', pad=20)

    # RIGHT CHART - Distribusi per Semester Lulus (Tren Waktu)
    semester_counts = df_pembilang['Semester Lulus'].value_counts().sort_index()

    # Map semester to labels (e.g., 20231 -> "2023/1", 20232 -> "2023/2")
    semester_labels = []
    for sem in semester_counts.index:
        try:
            tahun = str(sem)[:4]
            periode = str(sem)[4]
            semester_labels.append(f"{tahun}/{periode}")
        except:
            semester_labels.append(str(sem))

    x_pos = np.arange(len(semester_counts))

    # Use gradient color based on count
    colors_bar = plt.cm.Blues(np.linspace(0.5, 0.9, len(semester_counts)))

    bars = ax2.bar(x_pos, semester_counts.values,
                   color=colors_bar, edgecolor='#1a1a1a',
                   linewidth=1.5, alpha=0.9, width=0.7)

    # Labels on top of bars
    max_count_right = semester_counts.max()
    for bar, count in zip(bars, semester_counts.values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height + max_count_right * 0.02,
                f'{int(count)}', ha='center', va='bottom',
                fontsize=11, fontweight='900', color='#2c3e50')

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(semester_labels, fontsize=11, fontweight='600', rotation=0)
    ax2.set_ylabel('Jumlah Lulusan Bekerja', fontsize=13, fontweight='700')
    ax2.set_title('Distribusi Lulusan Bekerja\nper Semester Kelulusan',
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
    main_title = (f'IKU 11: Statistik Summary - Lulusan yang Memiliki Pekerjaan\n'
                  f'Total: {total_lulusan_bekerja} lulusan bekerja '
                  f'({persentase:.1f}% dari {total_lulusan} lulusan FST)')
    fig.suptitle(main_title, fontsize=15, fontweight='900', y=0.96)

    plt.tight_layout(rect=[0, 0.02, 1, 0.90])

    saved_files = save_figure(fig, 'IKU_11_breakdown_statistik')
    plt.close()

    return saved_files


def create_iku_11_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 11"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 11...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('11', 'pembilang')
    df_penyebut = read_excel_iku('11', 'penyebut')

    # Generate chart
    all_files = []

    print("    → Statistik Summary (Masa Tunggu & Top Prodi)...")
    all_files.extend(create_iku_11_statistik(df_pembilang, df_penyebut))

    print(f"  ✅ Breakdown IKU 11 selesai (1 chart)")
    return all_files


if __name__ == "__main__":
    create_iku_11_breakdown()
