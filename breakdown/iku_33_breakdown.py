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
from visualization_config import read_excel_iku, setup_publication_style
from breakdown_utils import create_dual_bar_chart


def create_iku_33_statistik(df_pembilang, df_penyebut):
    """Chart: Statistik Summary - Kategori Program dan Paket Program"""

    # Data processing
    total_mahasiswa = len(df_pembilang)
    total_dosen_aktif = df_pembilang['NIP'].nunique()
    total_dosen_fst = len(df_penyebut)
    persentase_dosen = (total_dosen_aktif / total_dosen_fst * 100) if total_dosen_fst > 0 else 0

    # Nama Program (kategori umum: Magang Dudi, Studi Independen, dll)
    nama_program = df_pembilang['Nama Program'].value_counts()

    # Top 10 Paket Program (nama spesifik program)
    top_paket = df_pembilang['Paket Program'].value_counts().head(10)

    # Prepare colors
    program_colors = ['#3498DB', '#E74C3C', '#F39C12', '#1ABC9C', '#9B59B6'][:len(nama_program)]
    paket_colors = ['#3498DB', '#E74C3C', '#F39C12', '#1ABC9C', '#9B59B6',
                    '#E85D75', '#70AD47', '#5B9BD5', '#ED7D31', '#9966CC'][:len(top_paket)]

    # Create main title
    main_title = (f'IKU 33: Statistik Summary - Bimbingan Mahasiswa Luar Prodi\n'
                  f'Total: {total_mahasiswa} mahasiswa | {total_dosen_aktif} dosen '
                  f'({persentase_dosen:.1f}% dari {total_dosen_fst} dosen FST)')

    return create_dual_bar_chart(
        left_data=nama_program,
        right_data=top_paket,
        left_title='Kategori Program Bimbingan',
        right_title='Top 10 Paket Program Spesifik',
        main_title=main_title,
        left_xlabel='Jumlah Mahasiswa',
        right_xlabel='Jumlah Mahasiswa',
        filename_base='IKU_33_breakdown_statistik',
        left_colors=program_colors,
        right_colors=paket_colors,
        left_wrap_width=40,
        right_wrap_width=45
    )


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
