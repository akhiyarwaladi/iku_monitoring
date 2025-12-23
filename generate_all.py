"""
============================================================================
GENERATE ALL VISUALIZATIONS
Master script untuk generate semua visualisasi IKU
============================================================================
Script ini akan menjalankan:
1. Main visualizations (summary per prodi - horizontal & vertical)
2. All breakdown charts (IKU 31, 33, 41, 42)
============================================================================
"""

import sys
from pathlib import Path

# Import main visualization
from main_visualize_iku import main as create_main_visualizations

# Import breakdowns
sys.path.append(str(Path(__file__).parent / 'breakdown'))
from breakdown.iku_31_breakdown import create_iku_31_breakdown
from breakdown.iku_33_breakdown import create_iku_33_breakdown
from breakdown.iku_41_breakdown import create_iku_41_breakdown
from breakdown.iku_42_breakdown import create_iku_42_breakdown


def generate_all():
    """Generate semua visualisasi IKU (main + breakdowns)"""

    print("="*80)
    print("GENERATING ALL IKU VISUALIZATIONS")
    print("="*80)

    all_files = []

    # Step 1: Generate main visualizations
    print("\n" + "="*80)
    print("STEP 1: MAIN VISUALIZATIONS (Summary per Prodi)")
    print("="*80)
    main_files = create_main_visualizations()
    all_files.extend(main_files if main_files else [])

    # Step 2: Generate breakdowns
    print("\n" + "="*80)
    print("STEP 2: BREAKDOWN VISUALIZATIONS (Detail Charts)")
    print("="*80)

    # IKU 31 breakdown
    iku31_files = create_iku_31_breakdown()
    all_files.extend(iku31_files)

    # IKU 33 breakdown
    iku33_files = create_iku_33_breakdown()
    all_files.extend(iku33_files)

    # IKU 41 breakdown
    iku41_files = create_iku_41_breakdown()
    all_files.extend(iku41_files)

    # IKU 42 breakdown
    iku42_files = create_iku_42_breakdown()
    all_files.extend(iku42_files)

    # Summary
    print("\n" + "="*80)
    print("GENERATION COMPLETE!")
    print("="*80)
    print(f"\n✅ Total files generated: {len(all_files)}")
    print(f"   - Main visualizations: {len(main_files)}")
    print(f"   - IKU 31 breakdowns: {len(iku31_files)}")
    print(f"   - IKU 33 breakdowns: {len(iku33_files)}")
    print(f"   - IKU 41 breakdowns: {len(iku41_files)}")
    print(f"   - IKU 42 breakdowns: {len(iku42_files)}")
    print("\n📁 Output directory: output/")
    print("   ├── png/ (PNG files at 300 DPI)")
    print("   └── svg/ (SVG vector files)")
    print("\n" + "="*80)

    return all_files


if __name__ == "__main__":
    generate_all()
