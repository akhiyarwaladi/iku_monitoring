"""
============================================================================
IKU 42 BREAKDOWN: Pengajar Praktisi
============================================================================
Visualisasi breakdown untuk IKU 42:
1. Dosen Annotated - Bar chart dengan nama praktisi per prodi
============================================================================
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from visualization_config import read_excel_iku, setup_publication_style
from breakdown_utils import create_annotated_bar_chart


def create_iku_42_praktisi_annotated(df_pembilang):
    """Chart: Bar Chart dengan Nama Praktisi per Prodi"""

    return create_annotated_bar_chart(
        df_data=df_pembilang,
        groupby_col='Program Studi',
        name_col='Nama',
        jurusan_col='Jurusan',
        chart_title='IKU 42: Distribusi Pengajar Praktisi per Program Studi\ndengan Daftar Nama',
        xlabel='Jumlah Praktisi',
        filename_base='IKU_42_breakdown_praktisi_annotated',
        max_names_full=6
    )


def create_iku_42_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 42"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 42...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('42', 'pembilang')

    # Generate chart
    all_files = []

    print("    → Praktisi Annotated (Bar dengan Nama Dosen)...")
    all_files.extend(create_iku_42_praktisi_annotated(df_pembilang))

    print(f"  ✅ Breakdown IKU 42 selesai (1 chart)")
    return all_files


if __name__ == "__main__":
    create_iku_42_breakdown()
