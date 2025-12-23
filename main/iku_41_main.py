"""
============================================================================
IKU 41 MAIN: Summary Per Prodi
============================================================================
Visualisasi summary untuk IKU 41:
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


def create_iku_41_main():
    """Generate main visualizations untuk IKU 41"""

    print("\n" + "="*70)
    print("IKU 41: Persentase Dosen Memiliki Sertifikat Kompetensi/Profesi DUDI")
    print("="*70)

    setup_publication_style()
    all_files = process_single_iku('41')

    return all_files


if __name__ == "__main__":
    create_iku_41_main()
