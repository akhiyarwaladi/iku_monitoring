"""
============================================================================
IKU 33 BREAKDOWN: Bimbingan Mahasiswa Luar Prodi
============================================================================
Visualisasi breakdown untuk IKU 33:
1. Statistik Summary - Kategori program dan paket program spesifik
============================================================================
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import textwrap
from visualization_config import (
    read_excel_iku, setup_publication_style, save_figure,
    JURUSAN_COLORS, PRODI_TO_JURUSAN, BREAKDOWN_STYLE, JURUSAN_ORDER
)
from .breakdown_utils import create_dual_bar_chart


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


def create_iku_33_statistik_with_jurusan(df_pembilang, df_penyebut):
    """Chart: Statistik Summary with Jurusan Color Coding"""

    # Data processing
    total_mahasiswa = len(df_pembilang)
    total_dosen_aktif = df_pembilang['NIP'].nunique()
    total_dosen_fst = len(df_penyebut)
    persentase_dosen = (total_dosen_aktif / total_dosen_fst * 100) if total_dosen_fst > 0 else 0

    # Merge pembilang dengan penyebut untuk dapat Jurusan dan Program Studi
    df_pembilang_enriched = df_pembilang.merge(
        df_penyebut[['NIP', 'Program Studi', 'Jurusan']],
        on='NIP',
        how='left'
    )

    # Map each row to jurusan
    df_pembilang_enriched['Jurusan_Short'] = df_pembilang_enriched.apply(get_jurusan_short, axis=1)

    # Process nama program with jurusan info
    program_counts = df_pembilang_enriched['Nama Program'].value_counts()
    program_data = []

    for program in program_counts.index:
        count = program_counts[program]
        program_rows = df_pembilang_enriched[df_pembilang_enriched['Nama Program'] == program]
        jurusan_dist = program_rows['Jurusan_Short'].value_counts()
        dominant_jurusan = jurusan_dist.index[0]
        program_data.append({
            'name': program,
            'count': count,
            'jurusan': dominant_jurusan
        })

    program_df = pd.DataFrame(program_data)

    # Process paket program with jurusan info
    paket_counts = df_pembilang_enriched['Paket Program'].value_counts().head(10)
    paket_data = []

    for paket in paket_counts.index:
        count = paket_counts[paket]
        paket_rows = df_pembilang_enriched[df_pembilang_enriched['Paket Program'] == paket]
        jurusan_dist = paket_rows['Jurusan_Short'].value_counts()
        dominant_jurusan = jurusan_dist.index[0]
        paket_data.append({
            'name': paket,
            'count': count,
            'jurusan': dominant_jurusan
        })

    paket_df = pd.DataFrame(paket_data)

    # Create dual chart with jurusan colors
    style = BREAKDOWN_STYLE
    max_items = len(paket_df)
    fig_height = max(style['min_fig_height'], max_items * 0.7)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, fig_height))

    # LEFT CHART - Program breakdown per jurusan (Pie Chart)
    # Create detailed breakdown: each program-jurusan combination is a slice
    program_jurusan_data = []

    for program in df_pembilang_enriched['Nama Program'].unique():
        program_rows = df_pembilang_enriched[df_pembilang_enriched['Nama Program'] == program]
        jurusan_dist = program_rows['Jurusan_Short'].value_counts()

        for jurusan, count in jurusan_dist.items():
            program_jurusan_data.append({
                'label': f'{program}\n{jurusan}',
                'program': program,
                'jurusan': jurusan,
                'count': count
            })

    # Sort by program order then by count
    program_order = ['Magang Dudi', 'Studi Independen', 'Kewirausahaan', 'Riset', 'KKNT']
    program_jurusan_df = pd.DataFrame(program_jurusan_data)
    program_jurusan_df['program_order'] = program_jurusan_df['program'].map(
        {p: i for i, p in enumerate(program_order)}
    )
    program_jurusan_df = program_jurusan_df.sort_values(['program_order', 'count'], ascending=[True, False])

    # Prepare data for pie chart
    pie_labels = program_jurusan_df['label'].values
    pie_counts = program_jurusan_df['count'].values
    pie_colors = [JURUSAN_COLORS[row['jurusan']]['base'] for _, row in program_jurusan_df.iterrows()]

    wedges, texts, autotexts = ax1.pie(
        pie_counts,
        labels=pie_labels,
        colors=pie_colors,
        autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100.*sum(pie_counts))})',
        startangle=90,
        wedgeprops={'edgecolor': '#1a1a1a', 'linewidth': 1.5, 'alpha': 0.88},
        textprops={'fontsize': 8, 'fontweight': '600'}
    )

    # Style autopct text (percentages and counts)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(8)
        autotext.set_fontweight('900')

    # Title
    total_mahasiswa = sum(pie_counts)
    ax1.set_title(f'Kategori Program Bimbingan per Jurusan\nTotal: {total_mahasiswa} mahasiswa',
                 fontsize=13, fontweight='900', pad=15)

    # RIGHT CHART - Paket
    y_pos2 = np.arange(len(paket_df))
    right_colors = [JURUSAN_COLORS[row['jurusan']]['base'] for _, row in paket_df.iterrows()]

    bars2 = ax2.barh(y_pos2, paket_df['count'].values,
                     color=right_colors, edgecolor='#1a1a1a',
                     linewidth=1.5, alpha=0.88, height=0.75)

    for bar, count in zip(bars2, paket_df['count'].values):
        ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f'{int(count)}', ha='left', va='center', fontsize=10, fontweight='900')

    ax2.set_yticks(y_pos2)
    right_labels = ['\n'.join(textwrap.wrap(name, width=45))
                    for name in paket_df['name']]
    ax2.set_yticklabels(right_labels, fontsize=10, fontweight='600')
    ax2.set_xlabel('Jumlah Mahasiswa', fontsize=12, fontweight='700')
    ax2.set_title('Top 10 Paket\nProgram Spesifik', fontsize=13, fontweight='900', pad=15)
    ax2.xaxis.grid(True, linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax2.set_axisbelow(True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_linewidth(1.5)
    ax2.spines['bottom'].set_linewidth(1.5)
    ax2.invert_yaxis()

    # Add JURUSAN legend
    all_jurusan = set(program_df['jurusan'].unique()) | set(paket_df['jurusan'].unique())
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

    # Main title
    main_title = (f'IKU 33: Statistik Summary - Bimbingan Mahasiswa Luar Prodi\n'
                  f'Total: {total_mahasiswa} mahasiswa | {total_dosen_aktif} dosen '
                  f'({persentase_dosen:.1f}% dari {total_dosen_fst} dosen FST)')
    fig.suptitle(main_title, fontsize=13, fontweight='900', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    saved_files = save_figure(fig, 'IKU_33_breakdown_statistik')
    plt.close()

    return saved_files


# Keep old function name for backward compatibility
def create_iku_33_statistik(df_pembilang, df_penyebut):
    """Chart: Statistik Summary - Kategori Program dan Paket Program"""
    return create_iku_33_statistik_with_jurusan(df_pembilang, df_penyebut)


def create_iku_33_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 33"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 33...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('33', 'pembilang')
    df_penyebut = read_excel_iku('33', 'penyebut')

    # Generate chart
    all_files = []

    print("    → Statistik Summary (Program & Paket)...")
    all_files.extend(create_iku_33_statistik(df_pembilang, df_penyebut))

    print(f"  ✅ Breakdown IKU 33 selesai (1 chart)")
    return all_files


if __name__ == "__main__":
    create_iku_33_breakdown()
