"""
============================================================================
IKU 81 BREAKDOWN: Prodi Akreditasi Internasional
============================================================================
Visualisasi breakdown untuk IKU 81:
1. Overview - Prodi dengan/tanpa akreditasi internasional
2. Detail Akreditasi - Info lembaga dan tanggal
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
    if pd.isna(prodi_name):
        return 'MIPA'
    prodi_clean = str(prodi_name).replace('Program Studi ', '')
    return PRODI_TO_JURUSAN.get(prodi_clean, 'MIPA')


def create_iku_81_overview(df_pembilang, df_penyebut):
    """Chart: Overview - Prodi dengan/tanpa akreditasi internasional"""

    style = BREAKDOWN_STYLE

    # Get set of prodi with international accreditation
    prodi_akreditasi = set(df_pembilang['Program Studi'].dropna().unique())

    # Create data for all prodi
    prodi_data = []
    for _, row in df_penyebut.iterrows():
        prodi = row['Program Studi']
        has_akreditasi = prodi in prodi_akreditasi
        jurusan = get_jurusan_from_prodi(prodi)
        prodi_data.append({
            'Program Studi': prodi,
            'Jurusan': jurusan,
            'Has_Akreditasi': has_akreditasi,
            'Status': 'Akreditasi Internasional' if has_akreditasi else 'Belum'
        })

    df_prodi = pd.DataFrame(prodi_data)

    # Sort by jurusan order and then by status
    jurusan_order_map = {j: i for i, j in enumerate(JURUSAN_ORDER)}
    df_prodi['jurusan_order'] = df_prodi['Jurusan'].map(lambda x: jurusan_order_map.get(x, 999))
    df_prodi = df_prodi.sort_values(['jurusan_order', 'Has_Akreditasi'], ascending=[True, False])

    # Create figure
    fig_height = max(10, len(df_prodi) * 0.6)
    fig, ax = plt.subplots(figsize=(14, fig_height))

    y_pos = np.arange(len(df_prodi))

    # Colors: Green for accredited, Gray for not
    colors = []
    for _, row in df_prodi.iterrows():
        if row['Has_Akreditasi']:
            colors.append('#2E7D32')  # Green for accredited
        else:
            colors.append('#BDBDBD')  # Gray for not accredited

    # Create bars (all same width = 1 for visual comparison)
    bars = ax.barh(y_pos, [1] * len(df_prodi),
                   color=colors, edgecolor='#1a1a1a',
                   linewidth=1.5, alpha=0.88, height=0.75)

    # Add status text on bars
    for idx, (bar, row) in enumerate(zip(bars, df_prodi.itertuples())):
        status_text = 'Akreditasi Internasional' if row.Has_Akreditasi else 'Belum Terakreditasi Internasional'
        text_color = 'white' if row.Has_Akreditasi else '#666666'
        ax.text(0.02, bar.get_y() + bar.get_height()/2,
                status_text,
                ha='left', va='center',
                fontsize=10, fontweight='700',
                color=text_color)

    # Add separator lines between jurusan
    jurusan_list = df_prodi['Jurusan'].tolist()
    current_jurusan = None
    for i, jurusan in enumerate(jurusan_list):
        if current_jurusan is not None and jurusan != current_jurusan:
            ax.axhline(y=i-0.5, color='#333333', linestyle='-',
                      linewidth=1.5, alpha=0.6, zorder=2)
        current_jurusan = jurusan

    # Styling
    ax.set_yticks(y_pos)
    labels = [label.replace('Program Studi ', '') for label in df_prodi['Program Studi']]
    ax.set_yticklabels(labels, fontsize=10, fontweight='600')
    ax.set_xlim(0, 1.2)
    ax.set_xticks([])  # Hide x-axis ticks
    ax.set_xlabel('')

    # Title
    total_prodi = len(df_penyebut)
    total_akreditasi = len(df_pembilang)
    persentase = (total_akreditasi / total_prodi * 100) if total_prodi > 0 else 0

    ax.set_title(f'IKU 81: Status Akreditasi Internasional Program Studi\n'
                f'{total_akreditasi} dari {total_prodi} prodi ({persentase:.1f}%) memiliki akreditasi internasional',
                fontsize=13, fontweight='900', pad=20)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='#2E7D32', edgecolor='#1a1a1a',
                      linewidth=1.5, label='Akreditasi Internasional'),
        mpatches.Patch(facecolor='#BDBDBD', edgecolor='#1a1a1a',
                      linewidth=1.5, label='Belum Terakreditasi Internasional')
    ]
    ax.legend(handles=legend_elements, loc='upper right', frameon=True,
              framealpha=0.95, edgecolor='0.2', fontsize=10)

    plt.tight_layout()

    saved_files = save_figure(fig, 'IKU_81_breakdown_overview')
    plt.close()

    return saved_files


def create_iku_81_detail(df_pembilang, df_penyebut):
    """Chart: Detail Akreditasi - Info lembaga dan tanggal"""

    # If no data, create simple info chart
    if len(df_pembilang) == 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'Belum ada program studi dengan akreditasi internasional',
                ha='center', va='center', fontsize=14, fontweight='600')
        ax.axis('off')
        saved_files = save_figure(fig, 'IKU_81_breakdown_detail')
        plt.close()
        return saved_files

    # Create detail table visualization
    fig, ax = plt.subplots(figsize=(14, max(6, len(df_pembilang) * 1.5)))

    # Hide axes
    ax.axis('off')

    # Create table data
    table_data = []
    for _, row in df_pembilang.iterrows():
        prodi = str(row.get('Program Studi', '-'))
        jenjang = str(row.get('Jenjang Pendidikan', '-'))
        peringkat = str(row.get('Peringkat Akreditasi', '-'))
        lembaga = str(row.get('Lembaga Akreditasi', '-'))

        # Format dates
        tgl_sk = row.get('Tanggal SK', '-')
        tgl_exp = row.get('Tanggal Kadaluarsa', '-')

        if pd.notna(tgl_sk) and hasattr(tgl_sk, 'strftime'):
            tgl_sk = tgl_sk.strftime('%Y-%m-%d')
        if pd.notna(tgl_exp) and hasattr(tgl_exp, 'strftime'):
            tgl_exp = tgl_exp.strftime('%Y-%m-%d')

        table_data.append([prodi, jenjang, peringkat, lembaga, str(tgl_sk), str(tgl_exp)])

    # Column headers
    columns = ['Program Studi', 'Jenjang', 'Peringkat', 'Lembaga Akreditasi', 'Tanggal SK', 'Kadaluarsa']

    # Create table
    table = ax.table(cellText=table_data,
                     colLabels=columns,
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.18, 0.08, 0.12, 0.25, 0.12, 0.12])

    # Style table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 2.0)

    # Style header
    for i, col in enumerate(columns):
        cell = table[(0, i)]
        cell.set_facecolor('#2E7D32')
        cell.set_text_props(color='white', fontweight='bold')

    # Style data cells
    for i in range(len(table_data)):
        for j in range(len(columns)):
            cell = table[(i + 1, j)]
            cell.set_facecolor('#E8F5E9' if i % 2 == 0 else 'white')

    # Title
    total_prodi = len(df_penyebut)
    total_akreditasi = len(df_pembilang)

    ax.set_title(f'IKU 81: Detail Program Studi dengan Akreditasi Internasional\n'
                f'{total_akreditasi} Program Studi Terakreditasi Internasional',
                fontsize=13, fontweight='900', pad=20, y=0.98)

    plt.tight_layout()

    saved_files = save_figure(fig, 'IKU_81_breakdown_detail')
    plt.close()

    return saved_files


def create_iku_81_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 81"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 81...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('81', 'pembilang')
    df_penyebut = read_excel_iku('81', 'penyebut')

    # Generate semua charts
    all_files = []

    print("    -> Overview (Status Akreditasi per Prodi)...")
    all_files.extend(create_iku_81_overview(df_pembilang, df_penyebut))

    print("    -> Detail Akreditasi (Tabel Info)...")
    all_files.extend(create_iku_81_detail(df_pembilang, df_penyebut))

    print(f"  -> Breakdown IKU 81 selesai (2 charts)")
    return all_files


if __name__ == "__main__":
    create_iku_81_breakdown()
