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
from visualization_config import (
    read_excel_iku, setup_publication_style, JURUSAN_COLORS
)
from breakdown_utils import create_annotated_bar_chart, create_dual_bar_chart


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


def create_iku_31_statistik(df_pembilang, df_penyebut):
    """Chart: Statistik Summary - Top Kegiatan dan Jenis"""

    # Data processing
    total_kegiatan = len(df_pembilang)
    total_dosen_aktif = df_pembilang['NIP'].nunique()
    total_dosen_fst = len(df_penyebut)
    persentase_dosen_aktif = (total_dosen_aktif / total_dosen_fst * 100) if total_dosen_fst > 0 else 0
    rata_rata_per_aktif = total_kegiatan / total_dosen_aktif if total_dosen_aktif > 0 else 0

    # Top 10 Kegiatan (nama kegiatan spesifik)
    top_kegiatan = df_pembilang['Kegiatan'].value_counts().head(10)

    # Breakdown jenis kegiatan
    jenis_breakdown = df_pembilang['Jenis'].value_counts()

    # Prepare colors for jenis
    jenis_colors = []
    color_map = {
        'Penelitian': '#3498DB',
        'Pengabdian': '#E74C3C',
        'Pendidikan': '#F39C12'
    }
    for jenis in jenis_breakdown.index:
        jenis_colors.append(color_map.get(jenis, '#5B9BD5'))

    # Create main title
    main_title = (f'IKU 31: Statistik Summary - Dosen Aktif Tridharma di PT Lain\n'
                  f'Total: {total_kegiatan} kegiatan | {total_dosen_aktif} dosen aktif '
                  f'({persentase_dosen_aktif:.1f}% dari {total_dosen_fst} dosen FST) | '
                  f'Rata-rata: {rata_rata_per_aktif:.1f} kegiatan/dosen')

    return create_dual_bar_chart(
        left_data=top_kegiatan,
        right_data=jenis_breakdown,
        left_title='Top 10 Kegiatan Tridharma Spesifik',
        right_title='Breakdown Jenis Kegiatan',
        main_title=main_title,
        left_xlabel='Jumlah Kegiatan',
        right_xlabel='Jumlah Kegiatan',
        filename_base='IKU_31_breakdown_statistik',
        left_colors=None,  # Use default colorblind palette
        right_colors=jenis_colors,  # Keep custom colors for jenis
        left_wrap_width=35,
        right_wrap_width=40
    )


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
