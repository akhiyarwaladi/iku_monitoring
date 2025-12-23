"""
============================================================================
IKU 42 MAIN: Summary Per Prodi
============================================================================
Visualisasi summary untuk IKU 42:
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


def create_iku_42_main():
    """Generate main visualizations untuk IKU 42"""

    print("\n" + "="*70)
    print("IKU 42: Persentase Pengajar yang Berasal dari Kalangan Praktisi")
    print("="*70)

    setup_publication_style()
    all_files = process_single_iku('42')

    return all_files


if __name__ == "__main__":
    create_iku_42_main()
