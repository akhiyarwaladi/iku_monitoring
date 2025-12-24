"""
============================================================================
IKU 21 BREAKDOWN: Mahasiswa yang Mengikuti Kegiatan MBKM
============================================================================
Visualisasi breakdown untuk IKU 21:
1. Statistik Summary - Distribusi Total SKS dan Top Nama Kegiatan
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
    # Remove 'Program Studi ' prefix if exists
    prodi_clean = prodi.replace('Program Studi ', '')
    return PRODI_TO_JURUSAN.get(prodi_clean, 'MIPA')


def create_iku_21_statistik(df_pembilang, df_penyebut):
    """Chart: Statistik Summary - Total SKS dan Top Kegiatan"""

    # Data processing
    total_kegiatan = len(df_pembilang)
    total_mahasiswa = len(df_penyebut)
    persentase = (total_kegiatan / total_mahasiswa * 100) if total_mahasiswa > 0 else 0

    # Map prodi to jurusan
    df_pembilang['Jurusan_Short'] = df_pembilang['Program Studi'].apply(get_jurusan_short)

    # Create figure with better proportions
    style = BREAKDOWN_STYLE
    fig_height = 8

    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=(20, fig_height))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1.2, 1.5], wspace=0.25)

    ax1 = fig.add_subplot(gs[0])  # Left: Bar chart - Total SKS Distribution
    ax2 = fig.add_subplot(gs[1])  # Right: Bar chart - Top 10 Nama Kegiatan

    # LEFT CHART - Total SKS Distribution (Binned Bar Chart)
    # Create SKS categories
    def categorize_sks(sks):
        if sks <= 8:
            return '2-8 SKS\n(Rendah)'
        elif sks <= 14:
            return '9-14 SKS\n(Sedang)'
        else:
            return '15-22 SKS\n(Tinggi)'

    df_pembilang['SKS_Category'] = df_pembilang['Total SKS'].apply(categorize_sks)
    sks_counts = df_pembilang['SKS_Category'].value_counts()

    # Order categories
    sks_order = ['2-8 SKS\n(Rendah)', '9-14 SKS\n(Sedang)', '15-22 SKS\n(Tinggi)']
    sks_data = []
    sks_labels = []

    for cat in sks_order:
        if cat in sks_counts.index:
            sks_data.append(sks_counts[cat])
            sks_labels.append(cat)

    # Define colors (low to high intensity)
    sks_colors = ['#ED7D31', '#70AD47', '#5B9BD5']  # Orange (low), Green (medium), Blue (high)

    x_pos = np.arange(len(sks_data))
    bars = ax1.bar(x_pos, sks_data,
                   color=sks_colors[:len(sks_data)], edgecolor='#1a1a1a',
                   linewidth=1.5, alpha=0.9, width=0.6)

    # Labels on top of bars
    max_count_left = max(sks_data)
    for bar, count in zip(bars, sks_data):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height + max_count_left * 0.02,
                f'{int(count)}', ha='center', va='bottom',
                fontsize=11, fontweight='900', color='#2c3e50')

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(sks_labels, fontsize=11, fontweight='600', rotation=0)
    ax1.set_ylabel('Jumlah Mahasiswa', fontsize=13, fontweight='700')
    ax1.set_title(f'Distribusi Total SKS MBKM\nTotal: {total_kegiatan} mahasiswa',
                  fontsize=14, fontweight='900', pad=20)
    ax1.yaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0, color='#bdc3c7')
    ax1.set_axisbelow(True)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_linewidth(1.8)
    ax1.spines['bottom'].set_linewidth(1.8)
    ax1.spines['left'].set_color('#7f8c8d')
    ax1.spines['bottom'].set_color('#7f8c8d')
    ax1.set_ylim(0, max_count_left * 1.15)

    # RIGHT CHART - Top 10 Nama Kegiatan
    kegiatan_counts = df_pembilang['Nama Kegiatan'].value_counts().head(10)

    # Get jurusan for each kegiatan
    kegiatan_jurusan = []
    for kegiatan in kegiatan_counts.index:
        kegiatan_rows = df_pembilang[df_pembilang['Nama Kegiatan'] == kegiatan]
        dominant_jurusan = kegiatan_rows['Jurusan_Short'].value_counts().index[0]
        kegiatan_jurusan.append(dominant_jurusan)

    # Sort ascending for horizontal bar
    kegiatan_df = pd.DataFrame({
        'kegiatan': kegiatan_counts.index[::-1],
        'count': kegiatan_counts.values[::-1],
        'jurusan': kegiatan_jurusan[::-1]
    })

    # Assign colors based on jurusan
    colors_bar_right = [JURUSAN_COLORS[j]['base'] for j in kegiatan_df['jurusan']]

    y_pos = np.arange(len(kegiatan_df))
    bars2 = ax2.barh(y_pos, kegiatan_df['count'].values,
                     color=colors_bar_right, edgecolor='#1a1a1a',
                     linewidth=1.5, alpha=0.88, height=0.75)

    # Labels
    for bar, count in zip(bars2, kegiatan_df['count'].values):
        ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f'{int(count)}', ha='left', va='center',
                fontsize=10, fontweight='900')

    ax2.set_yticks(y_pos)
    # Wrap labels
    wrapped_labels = ['\n'.join(textwrap.wrap(name, width=45))
                     for name in kegiatan_df['kegiatan']]
    ax2.set_yticklabels(wrapped_labels, fontsize=10, fontweight='600')
    ax2.set_xlabel('Jumlah Mahasiswa', fontsize=13, fontweight='700')
    ax2.set_title('Top 10 Nama Kegiatan MBKM\nTerbanyak Diikuti',
                  fontsize=14, fontweight='900', pad=20)
    ax2.xaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0, color='#bdc3c7')
    ax2.set_axisbelow(True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_linewidth(1.8)
    ax2.spines['bottom'].set_linewidth(1.8)
    ax2.spines['left'].set_color('#7f8c8d')
    ax2.spines['bottom'].set_color('#7f8c8d')
    ax2.invert_yaxis()

    # Add jurusan legend
    all_jurusan = set(kegiatan_df['jurusan'].unique())
    legend_jurusan = [j for j in JURUSAN_ORDER if j in all_jurusan]

    legend_elements = [
        mpatches.Patch(facecolor=JURUSAN_COLORS[j]['base'],
                      edgecolor='#1a1a1a', linewidth=1.5, label=j)
        for j in legend_jurusan
    ]

    fig.legend(handles=legend_elements,
              loc='upper right',
              bbox_to_anchor=(0.98, 0.96),
              ncol=1,
              frameon=True,
              framealpha=0.95,
              edgecolor='0.2',
              fontsize=10,
              title='Jurusan',
              title_fontsize=11)

    # Main title with better positioning
    main_title = (f'IKU 21: Statistik Summary - Mahasiswa yang Mengikuti Kegiatan MBKM\n'
                  f'Total: {total_kegiatan} kegiatan MBKM '
                  f'({persentase:.1f}% dari {total_mahasiswa} mahasiswa FST)')
    fig.suptitle(main_title, fontsize=15, fontweight='900', y=0.97)

    plt.tight_layout(rect=[0, 0, 1, 0.93])

    saved_files = save_figure(fig, 'IKU_21_breakdown_statistik')
    plt.close()

    return saved_files


def create_iku_21_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 21"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 21...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('21', 'pembilang')
    df_penyebut = read_excel_iku('21', 'penyebut')

    # Generate chart
    all_files = []

    print("    → Statistik Summary (Total SKS & Nama Kegiatan)...")
    all_files.extend(create_iku_21_statistik(df_pembilang, df_penyebut))

    print(f"  ✅ Breakdown IKU 21 selesai (1 chart)")
    return all_files


if __name__ == "__main__":
    create_iku_21_breakdown()
