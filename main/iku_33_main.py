"""
============================================================================
IKU 33 MAIN: Summary Per Prodi
============================================================================
Visualisasi summary untuk IKU 33:
1. Horizontal bar chart
2. Vertical bar chart
============================================================================
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from main_visualize_iku import (
    setup_publication_style,
    process_single_iku
)


def create_iku_33_main():
    """Generate main visualizations untuk IKU 33"""

    print("\n" + "="*70)
    print("IKU 33: Persentase Dosen Membimbing Mahasiswa Berkegiatan di Luar Program Studi")
    print("="*70)

    setup_publication_style()
    all_files = process_single_iku('33')

    return all_files


if __name__ == "__main__":
    create_iku_33_main()
