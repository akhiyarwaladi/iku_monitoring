"""
============================================================================
IKU 31 BREAKDOWN: Tridharma di PT Lain
============================================================================
Visualisasi breakdown untuk IKU 31:
1. Dosen Annotated - Bar chart dengan nama dosen per prodi
2. Statistik Summary - Top kegiatan dan jenis kegiatan
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
from .breakdown_utils import create_annotated_bar_chart, create_dual_bar_chart


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


def create_iku_31_dosen_annotated(df_pembilang, df_penyebut):
    """Chart: Bar Chart dengan Nama Dosen Aktif per Prodi"""

    # Get unique dosen aktif (unique NIP)
    dosen_aktif = df_pembilang[['NIP', 'Nama']].drop_duplicates(subset='NIP')

    # Join dengan penyebut untuk dapat Program Studi dan Jurusan
    df_dosen = dosen_aktif.merge(
        df_penyebut[['NIP', 'Program Studi', 'Jurusan']],
        on='NIP',
        how='left'
    )

    return create_annotated_bar_chart(
        df_data=df_dosen,
        groupby_col='Program Studi',
        name_col='Nama',
        jurusan_col='Jurusan',
        chart_title='IKU 31: Dosen Aktif Tridharma di PT Lain per Program Studi\ndengan Daftar Nama',
        xlabel='Jumlah Dosen Aktif',
        filename_base='IKU_31_breakdown_dosen_annotated',
        max_names_full=6
    )


def create_iku_31_statistik_with_jurusan(df_pembilang, df_penyebut):
    """Chart: Statistik Summary with Jurusan Color Coding"""

    # Data processing
    total_kegiatan = len(df_pembilang)
    total_dosen_aktif = df_pembilang['NIP'].nunique()
    total_dosen_fst = len(df_penyebut)
    persentase_dosen_aktif = (total_dosen_aktif / total_dosen_fst * 100) if total_dosen_fst > 0 else 0
    rata_rata_per_aktif = total_kegiatan / total_dosen_aktif if total_dosen_aktif > 0 else 0

    # Merge pembilang dengan penyebut untuk dapat Jurusan dan Program Studi
    df_pembilang_enriched = df_pembilang.merge(
        df_penyebut[['NIP', 'Program Studi', 'Jurusan']],
        on='NIP',
        how='left'
    )

    # Map each row to jurusan
    df_pembilang_enriched['Jurusan_Short'] = df_pembilang_enriched.apply(get_jurusan_short, axis=1)

    # Process kegiatan with jurusan info (similar to IKU 41)
    kegiatan_counts = df_pembilang_enriched['Kegiatan'].value_counts().head(10)
    kegiatan_data = []

    for kegiatan in kegiatan_counts.index:
        count = kegiatan_counts[kegiatan]
        kegiatan_rows = df_pembilang_enriched[df_pembilang_enriched['Kegiatan'] == kegiatan]
        jurusan_dist = kegiatan_rows['Jurusan_Short'].value_counts()
        dominant_jurusan = jurusan_dist.index[0]
        kegiatan_data.append({
            'name': kegiatan,
            'count': count,
            'jurusan': dominant_jurusan
        })

    kegiatan_df = pd.DataFrame(kegiatan_data)

    # Process jenis with jurusan distribution (for stacked bar)
    jenis_list = df_pembilang_enriched['Jenis'].unique()
    jenis_jurusan_matrix = []

    for jenis in jenis_list:
        jenis_rows = df_pembilang_enriched[df_pembilang_enriched['Jenis'] == jenis]
        jurusan_counts = jenis_rows['Jurusan_Short'].value_counts()

        row_data = {'Jenis': jenis}
        for jurusan in JURUSAN_ORDER:
            row_data[jurusan] = jurusan_counts.get(jurusan, 0)

        jenis_jurusan_matrix.append(row_data)

    jenis_df = pd.DataFrame(jenis_jurusan_matrix).set_index('Jenis')

    # Create figure with custom layout
    style = BREAKDOWN_STYLE
    max_items = len(kegiatan_df)
    fig_height = max(style['min_fig_height'], max_items * 0.7)

    # Create figure with GridSpec for custom layout
    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=(18, fig_height))
    gs = GridSpec(2, 2, figure=fig, width_ratios=[1.2, 1], height_ratios=[1, 1],
                  hspace=0.3, wspace=0.3)

    ax1 = fig.add_subplot(gs[:, 0])  # Left: spans both rows
    ax2_top = fig.add_subplot(gs[0, 1])  # Top right: Penelitian pie
    ax2_bottom = fig.add_subplot(gs[1, 1])  # Bottom right: Pengabdian pie

    # LEFT CHART - Kegiatan
    y_pos1 = np.arange(len(kegiatan_df))
    left_colors = [JURUSAN_COLORS[row['jurusan']]['base'] for _, row in kegiatan_df.iterrows()]

    bars1 = ax1.barh(y_pos1, kegiatan_df['count'].values,
                     color=left_colors, edgecolor='#1a1a1a',
                     linewidth=1.5, alpha=0.88, height=0.75)

    for bar, count in zip(bars1, kegiatan_df['count'].values):
        ax1.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height()/2,
                f'{int(count)}', ha='left', va='center', fontsize=10, fontweight='900')

    ax1.set_yticks(y_pos1)
    left_labels = ['\n'.join(textwrap.wrap(name, width=35))
                   for name in kegiatan_df['name']]
    ax1.set_yticklabels(left_labels, fontsize=8, fontweight='600')
    ax1.set_xlabel('Jumlah Kegiatan', fontsize=12, fontweight='700')
    ax1.set_title('Top 10 Kegiatan Tridharma Spesifik', fontsize=13, fontweight='900', pad=15)
    ax1.xaxis.grid(True, linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax1.set_axisbelow(True)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_linewidth(1.5)
    ax1.spines['bottom'].set_linewidth(1.5)
    ax1.invert_yaxis()

    # RIGHT CHARTS - Pie charts for Penelitian and Pengabdian
    def create_pie_chart(ax, jenis_name, jenis_data):
        """Create pie chart for a specific jenis"""
        # Get jurusan counts
        jurusan_counts = []
        jurusan_labels = []
        jurusan_colors = []

        for jurusan in JURUSAN_ORDER:
            if jurusan in jenis_data.index and jenis_data[jurusan] > 0:
                jurusan_counts.append(jenis_data[jurusan])
                jurusan_labels.append(jurusan)
                jurusan_colors.append(JURUSAN_COLORS[jurusan]['base'])

        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            jurusan_counts,
            labels=jurusan_labels,
            colors=jurusan_colors,
            autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100.*sum(jurusan_counts))})',
            startangle=90,
            wedgeprops={'edgecolor': '#1a1a1a', 'linewidth': 1.5, 'alpha': 0.88},
            textprops={'fontsize': 9, 'fontweight': '600'}
        )

        # Style autopct text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_fontweight('900')

        # Title with total count
        total = sum(jurusan_counts)
        ax.set_title(f'{jenis_name}\nTotal: {total} kegiatan',
                    fontsize=12, fontweight='900', pad=10)

    # Top pie: Penelitian
    if 'Penelitian' in jenis_df.index:
        create_pie_chart(ax2_top, 'Penelitian', jenis_df.loc['Penelitian'])
    else:
        ax2_top.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14)
        ax2_top.axis('off')

    # Bottom pie: Pengabdian
    if 'Pengabdian' in jenis_df.index:
        create_pie_chart(ax2_bottom, 'Pengabdian', jenis_df.loc['Pengabdian'])
    else:
        ax2_bottom.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14)
        ax2_bottom.axis('off')

    # Add JURUSAN legend (combine from kegiatan and jenis)
    all_jurusan = set(kegiatan_df['jurusan'].unique())
    # Add jurusan from jenis_df columns that have non-zero values
    for jurusan in JURUSAN_ORDER:
        if jurusan in jenis_df.columns and jenis_df[jurusan].sum() > 0:
            all_jurusan.add(jurusan)

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
    main_title = (f'IKU 31: Statistik Summary - Dosen Aktif Tridharma di PT Lain\n'
                  f'Total: {total_kegiatan} kegiatan | {total_dosen_aktif} dosen aktif '
                  f'({persentase_dosen_aktif:.1f}% dari {total_dosen_fst} dosen FST) | '
                  f'Rata-rata: {rata_rata_per_aktif:.1f} kegiatan/dosen')
    fig.suptitle(main_title, fontsize=13, fontweight='900', y=0.97)

    # Adjust layout with GridSpec
    gs.tight_layout(fig, rect=[0, 0, 1, 0.94])

    saved_files = save_figure(fig, 'IKU_31_breakdown_statistik')
    plt.close()

    return saved_files


# Keep old function name for backward compatibility
def create_iku_31_statistik(df_pembilang, df_penyebut):
    """Chart: Statistik Summary - Top Kegiatan dan Jenis"""
    return create_iku_31_statistik_with_jurusan(df_pembilang, df_penyebut)


def create_iku_31_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 31"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 31...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('31', 'pembilang')
    df_penyebut = read_excel_iku('31', 'penyebut')

    # Generate semua charts
    all_files = []

    print("    → Dosen Annotated (Bar dengan Nama Dosen)...")
    all_files.extend(create_iku_31_dosen_annotated(df_pembilang, df_penyebut))

    print("    → Statistik Summary (Top Kegiatan & Jenis)...")
    all_files.extend(create_iku_31_statistik(df_pembilang, df_penyebut))

    print(f"  ✅ Breakdown IKU 31 selesai (2 charts)")
    return all_files


if __name__ == "__main__":
    create_iku_31_breakdown()
