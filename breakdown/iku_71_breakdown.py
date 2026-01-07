"""
============================================================================
IKU 71 BREAKDOWN: Mata Kuliah PJBL/Case Method
============================================================================
Visualisasi breakdown untuk IKU 71:
1. Mata Kuliah Annotated - Bar chart dengan nama mata kuliah per prodi
2. Statistik Summary - Metode Pembelajaran breakdown
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


def get_jurusan_from_prodi(prodi_name):
    """Get jurusan from prodi name"""
    # Clean up prodi name
    if pd.isna(prodi_name):
        return 'MIPA'
    prodi_clean = str(prodi_name).replace('Program Studi ', '')
    return PRODI_TO_JURUSAN.get(prodi_clean, 'MIPA')


def create_iku_71_matakuliah_annotated(df_pembilang, df_penyebut):
    """Chart: Bar Chart dengan Nama Mata Kuliah per Prodi"""

    style = BREAKDOWN_STYLE

    # Group by Program Studi and collect course names
    grouped = df_pembilang.groupby('Program Studi').agg({
        'Nama Matakuliah': list,
        'Kode Matakuliah': 'count'
    }).reset_index()
    grouped.columns = ['Program Studi', 'Mata Kuliah', 'Count']

    # Add jurusan
    grouped['Jurusan'] = grouped['Program Studi'].apply(get_jurusan_from_prodi)

    # Sort by jurusan order then count
    jurusan_order_map = {j: i for i, j in enumerate(JURUSAN_ORDER)}
    grouped['jurusan_order'] = grouped['Jurusan'].map(lambda x: jurusan_order_map.get(x, 999))
    grouped = grouped.sort_values(['jurusan_order', 'Count'], ascending=[True, True])

    # Create figure
    fig_height = max(style['min_fig_height'], len(grouped) * style['fig_height_per_item'])
    fig, ax = plt.subplots(figsize=(18, fig_height))

    y_pos = np.arange(len(grouped))

    # Colors by jurusan
    colors = [JURUSAN_COLORS[row['Jurusan']]['base'] for _, row in grouped.iterrows()]

    # Create bars
    bars = ax.barh(y_pos, grouped['Count'].values,
                   color=colors, edgecolor='#1a1a1a',
                   linewidth=1.5, alpha=0.88, height=0.75)

    # Add separator lines between jurusan
    jurusan_list = grouped['Jurusan'].tolist()
    current_jurusan = None
    for i, jurusan in enumerate(jurusan_list):
        if current_jurusan is not None and jurusan != current_jurusan:
            ax.axhline(y=i-0.5, color='#333333', linestyle='-',
                      linewidth=1.5, alpha=0.6, zorder=2)
        current_jurusan = jurusan

    # Add annotations
    max_names_show = 5
    for idx, (bar, row) in enumerate(zip(bars, grouped.itertuples())):
        count = row.Count
        mk_list = row._2  # Mata Kuliah list

        # Format mata kuliah names
        if count <= max_names_show:
            mk_text = ', '.join(mk_list[:max_names_show])
        else:
            mk_text = ', '.join(mk_list[:max_names_show]) + f'.. +{count-max_names_show} lainnya'

        # Wrap text
        wrapped_text = '\n'.join(textwrap.wrap(mk_text, width=style['text_wrap_width']))

        # Text annotation
        ax.text(bar.get_width() + style['annotation_offset_x'],
                bar.get_y() + bar.get_height()/2,
                wrapped_text,
                ha='left', va='center',
                fontsize=style['faculty_name_size'],
                color=style['annotation_color'])

        # Count label
        count_color = style['count_color_dark'] if count > style['count_threshold'] else style['count_color_light']
        ax.text(bar.get_width() + style['count_offset_x'],
                bar.get_y() + bar.get_height()/2,
                f'{count}',
                ha='right', va='center',
                fontsize=style['count_label_size'],
                fontweight='900',
                color=count_color)

    # Styling
    ax.set_yticks(y_pos)
    labels = [label.replace('Program Studi ', '') for label in grouped['Program Studi']]
    ax.set_yticklabels(labels, fontsize=10, fontweight='600')
    ax.set_xlabel('Jumlah Mata Kuliah', fontsize=12, fontweight='700')
    ax.set_title('IKU 71: Mata Kuliah PJBL/Case Method per Program Studi\ndengan Daftar Nama Mata Kuliah',
                fontsize=13, fontweight='900', pad=20)
    ax.grid(axis='x', linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # Expand x-axis
    max_count = max(grouped['Count'])
    ax.set_xlim(0, max_count * style['x_axis_multiplier'])

    plt.tight_layout()

    saved_files = save_figure(fig, 'IKU_71_breakdown_matakuliah_annotated')
    plt.close()

    return saved_files


def create_iku_71_statistik(df_pembilang, df_penyebut):
    """Chart: Statistik Summary - Metode Pembelajaran breakdown"""

    style = BREAKDOWN_STYLE

    # Statistics
    total_mk_pjbl = len(df_pembilang)
    total_mk_all = len(df_penyebut)
    persentase = (total_mk_pjbl / total_mk_all * 100) if total_mk_all > 0 else 0

    # Count by Metode Pembelajaran
    metode_counts = df_pembilang['Metode Pembelajaran'].value_counts().head(10)

    # Add jurusan to pembilang
    df_pembilang_enriched = df_pembilang.copy()
    df_pembilang_enriched['Jurusan'] = df_pembilang_enriched['Program Studi'].apply(get_jurusan_from_prodi)

    # Count by Kesimpulan
    kesimpulan_counts = df_pembilang['Kesimpulan'].value_counts()

    # Create figure
    fig_height = max(style['min_fig_height'], len(metode_counts) * 0.7)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, fig_height))

    # LEFT CHART - Top Metode Pembelajaran
    y_pos1 = np.arange(len(metode_counts))

    # Color by most common jurusan for each metode
    metode_colors = []
    for metode in metode_counts.index:
        metode_rows = df_pembilang_enriched[df_pembilang_enriched['Metode Pembelajaran'] == metode]
        jurusan_dist = metode_rows['Jurusan'].value_counts()
        if len(jurusan_dist) > 0:
            dominant_jurusan = jurusan_dist.index[0]
            metode_colors.append(JURUSAN_COLORS[dominant_jurusan]['base'])
        else:
            metode_colors.append(JURUSAN_COLORS['MIPA']['base'])

    bars1 = ax1.barh(y_pos1, metode_counts.values,
                     color=metode_colors, edgecolor='#1a1a1a',
                     linewidth=1.5, alpha=0.88, height=0.75)

    for bar, count in zip(bars1, metode_counts.values):
        ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f'{int(count)}', ha='left', va='center', fontsize=10, fontweight='900')

    ax1.set_yticks(y_pos1)
    left_labels = ['\n'.join(textwrap.wrap(str(name)[:60], width=40)) for name in metode_counts.index]
    ax1.set_yticklabels(left_labels, fontsize=9, fontweight='600')
    ax1.set_xlabel('Jumlah Mata Kuliah', fontsize=12, fontweight='700')
    ax1.set_title('Top 10 Metode Pembelajaran', fontsize=13, fontweight='900', pad=15)
    ax1.xaxis.grid(True, linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax1.set_axisbelow(True)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_linewidth(1.5)
    ax1.spines['bottom'].set_linewidth(1.5)
    ax1.invert_yaxis()

    # RIGHT CHART - Pie chart by Jurusan
    jurusan_counts = df_pembilang_enriched['Jurusan'].value_counts()

    jurusan_colors = [JURUSAN_COLORS[j]['base'] for j in jurusan_counts.index if j in JURUSAN_COLORS]

    if len(jurusan_counts) > 0:
        wedges, texts, autotexts = ax2.pie(
            jurusan_counts.values,
            labels=jurusan_counts.index,
            colors=jurusan_colors,
            autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100.*sum(jurusan_counts.values))})',
            startangle=90,
            wedgeprops={'edgecolor': '#1a1a1a', 'linewidth': 1.5, 'alpha': 0.88},
            textprops={'fontsize': 10, 'fontweight': '600'}
        )

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('900')

        ax2.set_title('Distribusi per Jurusan', fontsize=13, fontweight='900', pad=15)
    else:
        ax2.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14)
        ax2.axis('off')

    # Main title
    main_title = (f'IKU 71: Statistik Mata Kuliah PJBL/Case Method\n'
                  f'Total: {total_mk_pjbl} mata kuliah PJBL dari {total_mk_all} total ({persentase:.1f}%)')
    fig.suptitle(main_title, fontsize=13, fontweight='900', y=0.96)

    plt.tight_layout(rect=[0, 0.02, 1, 0.90])

    saved_files = save_figure(fig, 'IKU_71_breakdown_statistik')
    plt.close()

    return saved_files


def create_iku_71_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 71"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 71...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('71', 'pembilang')
    df_penyebut = read_excel_iku('71', 'penyebut')

    # Generate semua charts
    all_files = []

    print("    -> Mata Kuliah Annotated (Bar dengan Nama MK)...")
    all_files.extend(create_iku_71_matakuliah_annotated(df_pembilang, df_penyebut))

    print("    -> Statistik Summary (Metode Pembelajaran)...")
    all_files.extend(create_iku_71_statistik(df_pembilang, df_penyebut))

    print(f"  -> Breakdown IKU 71 selesai (2 charts)")
    return all_files


if __name__ == "__main__":
    create_iku_71_breakdown()
