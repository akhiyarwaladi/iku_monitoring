"""
============================================================================
IKU 23 BREAKDOWN: Mahasiswa yang Memiliki HKI
============================================================================
Visualisasi breakdown untuk IKU 23:
1. Statistik Summary - Jenis HKI dan Detail
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


def create_iku_23_statistik(df_pembilang, df_penyebut):
    """Chart: Statistik Summary - Detail HKI dengan Annotasi"""

    # Data processing
    total_hki = len(df_pembilang)
    total_mahasiswa = len(df_penyebut)
    persentase = (total_hki / total_mahasiswa * 100) if total_mahasiswa > 0 else 0

    # Map prodi to jurusan
    df_pembilang['Jurusan_Short'] = df_pembilang['Program Studi'].apply(get_jurusan_short)

    # Create figure with size adjusted for small data
    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=(18, max(6, total_hki * 2.5)))

    # For small datasets, show detailed annotated chart
    if total_hki <= 10:
        # Sort by Jenis HKI then by Nama
        df_sorted = df_pembilang.sort_values(['Jenis HKI', 'Nama HKI'], ascending=[False, True])

        # Create horizontal bar with annotations
        ax = fig.add_subplot(111)

        y_pos = np.arange(len(df_sorted))

        # Get colors based on jurusan
        colors_bar = [JURUSAN_COLORS[row['Jurusan_Short']]['base']
                     for _, row in df_sorted.iterrows()]

        bars = ax.barh(y_pos, [1] * len(df_sorted),  # All bars same length for uniform display
                      color=colors_bar, edgecolor='#1a1a1a',
                      linewidth=1.5, alpha=0.88, height=0.75)

        # Prepare labels with detailed info
        labels = []
        for idx, row in df_sorted.iterrows():
            # Create multi-line label with key info
            nama_hki = row['Nama HKI']
            if len(nama_hki) > 50:
                nama_hki = nama_hki[:47] + '...'

            jenis = row['Jenis HKI']
            tingkat = row['Tingkat']
            nama_mhs = row['Nama']
            prodi = row['Program Studi'].replace('Program Studi ', '')

            label = f"{nama_hki}\n[{jenis} | {tingkat}] - {nama_mhs} ({prodi})"
            labels.append(label)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels, fontsize=10, fontweight='600')
        ax.set_xlabel('Detail HKI', fontsize=13, fontweight='700')
        ax.set_xlim(0, 1.3)  # Fixed range for uniform bars
        ax.set_xticks([])  # Hide x-axis ticks

        # Remove x-axis grid for cleaner look
        ax.xaxis.grid(False)
        ax.set_axisbelow(True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_linewidth(1.8)
        ax.spines['left'].set_color('#7f8c8d')
        ax.invert_yaxis()

        # Add jurusan legend
        all_jurusan = set(df_sorted['Jurusan_Short'].unique())
        legend_jurusan = [j for j in JURUSAN_ORDER if j in all_jurusan]

        legend_elements = [
            mpatches.Patch(facecolor=JURUSAN_COLORS[j]['base'],
                          edgecolor='#1a1a1a', linewidth=1.5, label=j)
            for j in legend_jurusan
        ]

        ax.legend(handles=legend_elements,
                 loc='upper right',
                 bbox_to_anchor=(0.98, 0.98),
                 fontsize=10,
                 frameon=True,
                 framealpha=0.95,
                 edgecolor='0.2',
                 title='Jurusan',
                 title_fontsize=11)

        # Add info box showing summary
        info_text = f"Total: {total_hki} HKI"
        if len(df_sorted['Jenis HKI'].unique()) > 0:
            jenis_list = df_sorted['Jenis HKI'].value_counts()
            info_text += "\n\nJenis HKI:"
            for jenis, count in jenis_list.items():
                info_text += f"\n  • {jenis}: {count}"

        # Add text box
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.15, edgecolor='#7f8c8d', linewidth=1.5)
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props, fontweight='600')

    else:
        # For larger datasets, use simpler grouped visualization
        ax = fig.add_subplot(111)

        # Count per jenis HKI
        jenis_counts = df_pembilang['Jenis HKI'].value_counts().sort_values(ascending=True)

        # Get dominant jurusan for each jenis
        jenis_jurusan = []
        for jenis in jenis_counts.index:
            jenis_rows = df_pembilang[df_pembilang['Jenis HKI'] == jenis]
            dominant_jurusan = jenis_rows['Jurusan_Short'].value_counts().index[0]
            jenis_jurusan.append(dominant_jurusan)

        colors_bar = [JURUSAN_COLORS[j]['base'] for j in jenis_jurusan]

        y_pos = np.arange(len(jenis_counts))
        bars = ax.barh(y_pos, jenis_counts.values,
                      color=colors_bar, edgecolor='#1a1a1a',
                      linewidth=1.5, alpha=0.88, height=0.75)

        # Labels
        for bar, count in zip(bars, jenis_counts.values):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                   f'{int(count)}', ha='left', va='center',
                   fontsize=11, fontweight='900')

        ax.set_yticks(y_pos)
        ax.set_yticklabels(jenis_counts.index, fontsize=11, fontweight='600')
        ax.set_xlabel('Jumlah HKI', fontsize=13, fontweight='700')
        ax.xaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0, color='#bdc3c7')
        ax.set_axisbelow(True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.8)
        ax.spines['bottom'].set_linewidth(1.8)
        ax.spines['left'].set_color('#7f8c8d')
        ax.spines['bottom'].set_color('#7f8c8d')
        ax.invert_yaxis()

        # Add jurusan legend
        all_jurusan = set(jenis_jurusan)
        legend_jurusan = [j for j in JURUSAN_ORDER if j in all_jurusan]

        legend_elements = [
            mpatches.Patch(facecolor=JURUSAN_COLORS[j]['base'],
                          edgecolor='#1a1a1a', linewidth=1.5, label=j)
            for j in legend_jurusan
        ]

        ax.legend(handles=legend_elements,
                 loc='upper right',
                 fontsize=10,
                 frameon=True,
                 framealpha=0.95,
                 edgecolor='0.2',
                 title='Jurusan',
                 title_fontsize=11)

    # Main title
    main_title = (f'IKU 23: Statistik Summary - Mahasiswa yang Memiliki HKI\n'
                  f'Total: {total_hki} HKI '
                  f'({persentase:.2f}% dari {total_mahasiswa} mahasiswa FST)')
    fig.suptitle(main_title, fontsize=15, fontweight='900', y=0.97)

    plt.tight_layout(rect=[0, 0, 1, 0.93])

    saved_files = save_figure(fig, 'IKU_23_breakdown_statistik')
    plt.close()

    return saved_files


def create_iku_23_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 23"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 23...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('23', 'pembilang')
    df_penyebut = read_excel_iku('23', 'penyebut')

    # Generate chart
    all_files = []

    print("    → Statistik Summary (Detail HKI)...")
    all_files.extend(create_iku_23_statistik(df_pembilang, df_penyebut))

    print(f"  ✅ Breakdown IKU 23 selesai (1 chart)")
    return all_files


if __name__ == "__main__":
    create_iku_23_breakdown()
