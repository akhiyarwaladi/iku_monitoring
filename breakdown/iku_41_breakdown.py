"""
============================================================================
IKU 41 BREAKDOWN: Sertifikat DUDI
============================================================================
Visualisasi breakdown untuk IKU 41:
1. Statistik Summary - Top lembaga dan top bidang sertifikasi
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
    JURUSAN_COLORS, PRODI_TO_JURUSAN, BREAKDOWN_STYLE
)


def get_jurusan_short(row):
    """Map row to short jurusan name"""
    if pd.notna(row.get('Jurusan', None)):
        j = row['Jurusan']
        if 'Matematika' in j or 'MIPA' in j or 'Ilmu Pengetahuan Alam' in j:
            return 'MIPA'
        elif 'Kebumian' in j or 'Geologi' in j:
            return 'Teknik Geologi'
        elif 'Kimia dan Lingkungan' in j or 'Sipil, Kimia' in j:
            return 'Teknik Kimia'
        elif 'Elektro dan Informatika' in j:
            return 'Teknik Elektro'
        elif 'Sipil' in j:
            return 'Teknik Sipil'

    if pd.notna(row.get('Program Studi', None)):
        prodi = row['Program Studi']
        return PRODI_TO_JURUSAN.get(prodi, 'MIPA')

    return 'MIPA'


def get_jurusan_abbrev(jurusan):
    """Get abbreviated jurusan name for compact display"""
    abbrev_map = {
        'MIPA': 'MIPA',
        'Teknik Geologi': 'T.Geo',
        'Teknik Kimia': 'T.Kim',
        'Teknik Sipil': 'T.Sip',
        'Teknik Elektro': 'T.Elek',
        'D3': 'D3'
    }
    return abbrev_map.get(jurusan, jurusan)


def create_dual_bar_chart_with_jurusan(left_data_with_jurusan, right_data_with_jurusan,
                                        left_title='', right_title='',
                                        main_title='', filename_base=''):
    """
    Create dual bar chart with jurusan color coding and legend

    Parameters:
    -----------
    left_data_with_jurusan : pd.DataFrame
        DataFrame with columns: name, count, jurusan, jurusan_detail
    right_data_with_jurusan : pd.DataFrame
        DataFrame with columns: name, count, jurusan, jurusan_detail
    """
    style = BREAKDOWN_STYLE

    # Determine figure height
    max_items = max(len(left_data_with_jurusan), len(right_data_with_jurusan))
    fig_height = max(style['min_fig_height'], max_items * 0.7)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, fig_height))

    # LEFT CHART
    y_pos1 = np.arange(len(left_data_with_jurusan))
    left_colors = [JURUSAN_COLORS[row['jurusan']]['base'] for _, row in left_data_with_jurusan.iterrows()]

    bars1 = ax1.barh(y_pos1, left_data_with_jurusan['count'].values,
                     color=left_colors, edgecolor='#1a1a1a',
                     linewidth=1.5, alpha=0.88, height=0.75)

    # Labels pada bars
    for bar, (_, row) in zip(bars1, left_data_with_jurusan.iterrows()):
        count = row['count']
        # Count number
        ax1.text(count + 0.15, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=10, fontweight='900')

        # Jurusan detail if mixed (abbreviated)
        if row['jurusan_detail']:
            ax1.text(count + 0.65, bar.get_y() + bar.get_height()/2,
                    f"{row['jurusan_detail']}",
                    ha='left', va='center', fontsize=8,
                    color='#444444', fontweight='600')

    # Styling ax1
    ax1.set_yticks(y_pos1)
    left_labels = ['\n'.join(textwrap.wrap(name, width=35))
                   for name in left_data_with_jurusan['name']]
    ax1.set_yticklabels(left_labels, fontsize=8, fontweight='600')
    ax1.set_xlabel('Jumlah Sertifikat', fontsize=12, fontweight='700')
    ax1.set_title(left_title, fontsize=13, fontweight='900', pad=15)
    ax1.xaxis.grid(True, linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax1.set_axisbelow(True)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_linewidth(1.5)
    ax1.spines['bottom'].set_linewidth(1.5)
    ax1.invert_yaxis()

    # Expand X-axis to give room for annotations
    max_count_left = left_data_with_jurusan['count'].max()
    ax1.set_xlim(0, max_count_left * 1.5)

    # RIGHT CHART
    y_pos2 = np.arange(len(right_data_with_jurusan))
    right_colors = [JURUSAN_COLORS[row['jurusan']]['base'] for _, row in right_data_with_jurusan.iterrows()]

    bars2 = ax2.barh(y_pos2, right_data_with_jurusan['count'].values,
                     color=right_colors, edgecolor='#1a1a1a',
                     linewidth=1.5, alpha=0.88, height=0.75)

    # Labels pada bars
    for bar, (_, row) in zip(bars2, right_data_with_jurusan.iterrows()):
        count = row['count']
        # Count number
        ax2.text(count + 0.15, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=10, fontweight='900')

        # Jurusan detail if mixed (abbreviated)
        if row['jurusan_detail']:
            ax2.text(count + 0.65, bar.get_y() + bar.get_height()/2,
                    f"{row['jurusan_detail']}",
                    ha='left', va='center', fontsize=8,
                    color='#444444', fontweight='600')

    # Styling ax2
    ax2.set_yticks(y_pos2)
    right_labels = ['\n'.join(textwrap.wrap(name, width=35))
                    for name in right_data_with_jurusan['name']]
    ax2.set_yticklabels(right_labels, fontsize=8, fontweight='600')
    ax2.set_xlabel('Jumlah Sertifikat', fontsize=12, fontweight='700')
    ax2.set_title(right_title, fontsize=13, fontweight='900', pad=15)
    ax2.xaxis.grid(True, linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax2.set_axisbelow(True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_linewidth(1.5)
    ax2.spines['bottom'].set_linewidth(1.5)
    ax2.invert_yaxis()

    # Expand X-axis to give room for annotations
    max_count_right = right_data_with_jurusan['count'].max()
    ax2.set_xlim(0, max_count_right * 1.5)

    # Add legend (jurusan used in this chart)
    all_jurusan = set(left_data_with_jurusan['jurusan'].unique()) | set(right_data_with_jurusan['jurusan'].unique())
    legend_order = ['MIPA', 'Teknik Geologi', 'Teknik Kimia', 'Teknik Sipil', 'Teknik Elektro', 'D3']
    legend_jurusan = [j for j in legend_order if j in all_jurusan]

    legend_elements = [
        mpatches.Patch(facecolor=JURUSAN_COLORS[j]['base'],
                      edgecolor='#1a1a1a', linewidth=1.5,
                      label=j)
        for j in legend_jurusan
    ]

    fig.legend(handles=legend_elements,
              loc='upper right',
              bbox_to_anchor=(0.98, 0.98),
              ncol=1,  # Vertical layout
              frameon=True,
              framealpha=0.95,
              edgecolor='0.2',
              fontsize=10,
              title='Jurusan',
              title_fontsize=11)

    # Main title
    if main_title:
        fig.suptitle(main_title, fontsize=13, fontweight='900', y=0.94)

    plt.tight_layout(rect=[0, 0, 1, 0.92])

    # Save
    saved_files = save_figure(fig, filename_base)
    plt.close()

    return saved_files


def create_iku_41_statistik(df_pembilang, df_penyebut):
    """Chart: Statistik Summary - Top Lembaga dan Top Bidang with Jurusan Color Coding"""

    # Data processing
    total_sertifikat = len(df_pembilang)
    total_dosen_bersertifikat = df_pembilang['NIP'].nunique()
    total_dosen_fst = len(df_penyebut)
    persentase_dosen = (total_dosen_bersertifikat / total_dosen_fst * 100) if total_dosen_fst > 0 else 0

    # Map each row to jurusan
    df_pembilang['Jurusan_Short'] = df_pembilang.apply(get_jurusan_short, axis=1)

    # Process TOP 10 LEMBAGA with jurusan info
    lembaga_counts = df_pembilang['Lembaga Sertifikasi'].value_counts().head(10)
    lembaga_data = []

    for lembaga in lembaga_counts.index:
        count = lembaga_counts[lembaga]
        # Get jurusan distribution for this lembaga
        lembaga_rows = df_pembilang[df_pembilang['Lembaga Sertifikasi'] == lembaga]
        jurusan_dist = lembaga_rows['Jurusan_Short'].value_counts()

        # Determine dominant jurusan
        dominant_jurusan = jurusan_dist.index[0]

        # Create detail string if mixed jurusan (use abbreviated names)
        if len(jurusan_dist) > 1:
            detail = ', '.join([f"{get_jurusan_abbrev(j)}:{c}" for j, c in jurusan_dist.items()])
        else:
            detail = ''

        lembaga_data.append({
            'name': lembaga,
            'count': count,
            'jurusan': dominant_jurusan,
            'jurusan_detail': detail
        })

    lembaga_df = pd.DataFrame(lembaga_data)

    # Process TOP 10 BIDANG with jurusan info
    bidang_counts = df_pembilang['Bidang Sertifikasi'].value_counts().head(10)
    bidang_data = []

    for bidang in bidang_counts.index:
        count = bidang_counts[bidang]
        # Get jurusan distribution for this bidang
        bidang_rows = df_pembilang[df_pembilang['Bidang Sertifikasi'] == bidang]
        jurusan_dist = bidang_rows['Jurusan_Short'].value_counts()

        # Determine dominant jurusan
        dominant_jurusan = jurusan_dist.index[0]

        # Create detail string if mixed jurusan (use abbreviated names)
        if len(jurusan_dist) > 1:
            detail = ', '.join([f"{get_jurusan_abbrev(j)}:{c}" for j, c in jurusan_dist.items()])
        else:
            detail = ''

        bidang_data.append({
            'name': bidang,
            'count': count,
            'jurusan': dominant_jurusan,
            'jurusan_detail': detail
        })

    bidang_df = pd.DataFrame(bidang_data)

    # Create main title
    main_title = (f'IKU 41: Statistik Summary - Dosen dengan Sertifikat DUDI\n'
                  f'Total: {total_sertifikat} sertifikat | {total_dosen_bersertifikat} dosen '
                  f'({persentase_dosen:.1f}% dari {total_dosen_fst} dosen FST)')

    return create_dual_bar_chart_with_jurusan(
        left_data_with_jurusan=lembaga_df,
        right_data_with_jurusan=bidang_df,
        left_title='Top 10 Lembaga Penerbit',
        right_title='Top 10 Bidang Sertifikasi',
        main_title=main_title,
        filename_base='IKU_41_breakdown_statistik'
    )


def create_iku_41_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 41"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 41...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('41', 'pembilang')
    df_penyebut = read_excel_iku('41', 'penyebut')

    # Generate chart
    all_files = []

    print("    → Statistik Summary (Top Lembaga & Bidang)...")
    all_files.extend(create_iku_41_statistik(df_pembilang, df_penyebut))

    print(f"  ✅ Breakdown IKU 41 selesai (1 chart)")
    return all_files


if __name__ == "__main__":
    create_iku_41_breakdown()
