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
from visualization_config import read_excel_iku, setup_publication_style
from breakdown_utils import create_dual_bar_chart


def create_iku_41_statistik(df_pembilang, df_penyebut):
    """Chart: Statistik Summary - Top Lembaga dan Top Bidang"""

    # Data processing
    total_sertifikat = len(df_pembilang)
    total_dosen_bersertifikat = df_pembilang['NIP'].nunique()
    total_dosen_fst = len(df_penyebut)
    persentase_dosen = (total_dosen_bersertifikat / total_dosen_fst * 100) if total_dosen_fst > 0 else 0

    # Top 10 Lembaga Sertifikasi
    top_lembaga = df_pembilang['Lembaga Sertifikasi'].value_counts().head(10)

    # Top 10 Bidang Sertifikasi
    top_bidang = df_pembilang['Bidang Sertifikasi'].value_counts().head(10)

    # Create main title
    main_title = (f'IKU 41: Statistik Summary - Dosen dengan Sertifikat DUDI\n'
                  f'Total: {total_sertifikat} sertifikat | {total_dosen_bersertifikat} dosen '
                  f'({persentase_dosen:.1f}% dari {total_dosen_fst} dosen FST)')

    return create_dual_bar_chart(
        left_data=top_lembaga,
        right_data=top_bidang,
        left_title='Top 10 Lembaga Penerbit',
        right_title='Top 10 Bidang Sertifikasi',
        main_title=main_title,
        left_xlabel='Jumlah Sertifikat',
        right_xlabel='Jumlah Sertifikat',
        filename_base='IKU_41_breakdown_statistik',
        left_colors=None,  # Use automatic colorblind palette
        right_colors=None,  # Use automatic Set2 palette
        left_wrap_width=35,
        right_wrap_width=35
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
