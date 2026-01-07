"""
============================================================================
SISTEM VISUALISASI IKU FAKULTAS SAINS & TEKNOLOGI
Universitas Jambi
============================================================================

Script terpusat untuk visualisasi semua IKU dengan standar publikasi
internasional.

Struktur Modular:
- config.py       : Konfigurasi global, warna, metadata
- utils.py        : Fungsi utility (I/O, setup style, helpers)
- processors.py   : Fungsi pemrosesan data per IKU
- visualizations.py : Fungsi visualisasi (charts)

Naming Convention (sesuai dokumen resmi):
- PDF IKU 1.1 = Dashboard IKU 1 = Excel IKU 1 (11+12+13) → Target 60%
- PDF IKU 1.2 = Dashboard IKU 2 = Excel IKU 2 (21+22+23) → Target 30%
- PDF IKU 2.1 = Dashboard IKU 3 = Excel IKU 3 (31+33) → Target 25%
- PDF IKU 2.2 = Dashboard IKU 4 = Excel IKU 4 (41+42) → Target 20.14%

Author: Tim IKU FST
Version: 2.0 (Modular)
Last Updated: 2026-01-07

Referensi:
- Ten guidelines for effective data visualization (Environmental Modelling & Software)
- Nature, Science, IEEE publication standards
- ColorBrewer2.org colorblind-safe palettes
============================================================================
"""

import sys
import argparse
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# Import from modules
from config import CONFIG, ALL_IKU, IKU_METADATA, IKU_EXPANSION
from utils import (
    setup_publication_style,
    read_excel_iku,
    cleanup_output_folder,
    calculate_overall_stats
)
from processors import (
    IKU_PROCESSORS,
    COMBINED_PROCESSORS,
    process_iku_1_combined,
    process_iku_2_combined,
    process_iku_3_combined,
    process_iku_4_combined,
    process_iku_5_combined,
    process_iku_6_combined,
    process_iku_7_combined,
    process_iku_8_combined
)
from visualizations import (
    create_vertical_bar_chart,
    create_summary_dashboard,
    create_breakdown_donut_charts,
    create_main_iku_donut,
    create_overall_achievement_dashboard,
    create_overall_achievement_bullet,
    create_overall_achievement_cards,
    create_overall_achievement_bullet_4x2,
    create_overall_achievement_thermometer,
    create_overall_achievement_waffle
)

# Import category breakdown functions
from breakdown.iku_11_breakdown import create_iku_11_breakdown
from breakdown.iku_12_breakdown import create_iku_12_breakdown
from breakdown.iku_13_breakdown import create_iku_13_breakdown
from breakdown.iku_21_breakdown import create_iku_21_breakdown
from breakdown.iku_22_breakdown import create_iku_22_breakdown
from breakdown.iku_23_breakdown import create_iku_23_breakdown
from breakdown.iku_31_breakdown import create_iku_31_breakdown
from breakdown.iku_33_breakdown import create_iku_33_breakdown
from breakdown.iku_41_breakdown import create_iku_41_breakdown
from breakdown.iku_42_breakdown import create_iku_42_breakdown
from breakdown.iku_71_breakdown import create_iku_71_breakdown
from breakdown.iku_81_breakdown import create_iku_81_breakdown

# Mapping IKU to breakdown function
CATEGORY_BREAKDOWN_FUNCTIONS = {
    '11': create_iku_11_breakdown,
    '12': create_iku_12_breakdown,
    '13': create_iku_13_breakdown,
    '21': create_iku_21_breakdown,
    '22': create_iku_22_breakdown,
    '23': create_iku_23_breakdown,
    '31': create_iku_31_breakdown,
    '33': create_iku_33_breakdown,
    '41': create_iku_41_breakdown,
    '42': create_iku_42_breakdown,
    '71': create_iku_71_breakdown,
    '81': create_iku_81_breakdown,
}


# ============================================================================
# MAIN ORCHESTRATION
# ============================================================================

def process_single_iku(iku_number):
    """
    Proses satu IKU lengkap: baca data, proses, visualisasi

    Parameters:
    -----------
    iku_number : str
        Nomor IKU (1, 11, 12, 13, 21, 22, 23, 31, 33, 41, 42)

    Returns:
    --------
    dict : {'data': DataFrame, 'stats': dict, 'files': list}
    """
    print(f"\n{'='*70}")
    print(f"IKU {iku_number}: {IKU_METADATA[iku_number]['title']}")
    print(f"{'='*70}")

    try:
        # Special handling untuk IKU gabungan (1, 2, 3, 4)
        if iku_number in COMBINED_PROCESSORS:
            process_func, entity_type, sub_ikus = COMBINED_PROCESSORS[iku_number]

            print(f"  [1/3] Menggabungkan data IKU {sub_ikus}...")
            data, stats, df_pembilang, df_penyebut = process_func()

            print("  [2/3] Statistik gabungan:")
            print(f"        Pembilang: {stats['pembilang']} {entity_type}")
            print(f"        Penyebut: {stats['penyebut']} {entity_type}")
            print(f"        Persentase: {stats['persentase']}%")

            # Buat visualisasi (hanya vertical untuk IKU gabungan)
            print("  [3/3] Membuat visualisasi (vertical only)...")
            target = CONFIG['target_values'].get(iku_number)
            files = []
            files.append(create_vertical_bar_chart(data, iku_number, target))

            print(f"  ✅ IKU {iku_number} (Gabungan) selesai diproses\n")

            return {
                'data': data,
                'stats': stats,
                'files': files
            }

        # Standard processing untuk IKU lainnya
        # 1. Baca data
        print("  [1/4] Membaca data...")
        df_pembilang = read_excel_iku(iku_number, 'pembilang')
        df_penyebut = read_excel_iku(iku_number, 'penyebut')

        # 2. Hitung statistik keseluruhan
        print("  [2/4] Menghitung statistik...")
        stats = calculate_overall_stats(df_pembilang, df_penyebut)
        print(f"        Pembilang: {stats['pembilang']}")
        print(f"        Penyebut: {stats['penyebut']}")
        print(f"        Persentase: {stats['persentase']}%")

        # 3. Proses data per prodi
        print("  [3/4] Memproses data per program studi...")
        if iku_number in IKU_PROCESSORS:
            data = IKU_PROCESSORS[iku_number](df_pembilang, df_penyebut)
        else:
            raise ValueError(f"IKU number tidak valid: {iku_number}")

        # 4. Buat visualisasi (vertical only - standardized)
        print("  [4/4] Membuat visualisasi (vertical only)...")
        target = CONFIG['target_values'].get(iku_number)
        files = []
        files.append(create_vertical_bar_chart(data, iku_number, target))

        print(f"  ✅ IKU {iku_number} selesai diproses\n")

        return {
            'data': data,
            'stats': stats,
            'files': files
        }

    except Exception as e:
        print(f"  ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return None


def main(iku_list=None, skip_breakdown=False, skip_dashboard=False, skip_cleanup=False, only_4x2=False):
    """
    Main function - Orchestrate seluruh proses visualisasi

    Parameters:
    -----------
    iku_list : list, optional
        List IKU yang akan diproses (default: semua IKU)
    skip_breakdown : bool
        Jika True, skip pembuatan breakdown charts
    skip_dashboard : bool
        Jika True, skip pembuatan summary dashboard
    skip_cleanup : bool
        Jika True, tidak menghapus file output sebelumnya
    only_4x2 : bool
        Jika True, hanya generate overall achievement dashboard 4x2
    """
    # Default: proses semua IKU
    if iku_list is None:
        iku_list = ALL_IKU.copy()

    # Expand IKU gabungan jika dipilih
    expanded_list = []
    for iku in iku_list:
        if iku in IKU_EXPANSION:
            for sub_iku in IKU_EXPANSION[iku]:
                if sub_iku not in expanded_list:
                    expanded_list.append(sub_iku)
        else:
            if iku not in expanded_list:
                expanded_list.append(iku)
    iku_list = expanded_list

    print("="*70)
    print("SISTEM VISUALISASI IKU FAKULTAS SAINS & TEKNOLOGI")
    print("Standar Publikasi Internasional (Modular v2.0)")
    print("="*70)
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output directory: {CONFIG['base_path'] / CONFIG['output_dir']}")
    print(f"Resolution: {CONFIG['dpi']} DPI")
    print(f"IKU yang diproses: {', '.join(iku_list)}")

    # Clean output folder (opsional)
    if not skip_cleanup:
        cleanup_output_folder()

    # Setup matplotlib style
    setup_publication_style()

    # Handle 4x2-only mode
    if only_4x2:
        print(f"\n{'='*70}")
        print("MODE: 4x2 ONLY - OVERALL ACHIEVEMENT DASHBOARD")
        print(f"{'='*70}")

        # Collect stats for all main IKUs (1-8)
        all_stats = {}

        # Process combined IKUs to get stats
        combined_ikus = {
            '1': process_iku_1_combined,
            '2': process_iku_2_combined,
            '3': process_iku_3_combined,
            '4': process_iku_4_combined,
            '5': process_iku_5_combined,
            '6': process_iku_6_combined,
            '7': process_iku_7_combined,
            '8': process_iku_8_combined
        }

        for iku_num, process_func in combined_ikus.items():
            try:
                print(f"  Collecting stats for IKU {iku_num}...")
                data, stats, df_pembilang, df_penyebut = process_func()
                all_stats[iku_num] = stats
            except Exception as e:
                print(f"  ⚠️  Error collecting IKU {iku_num}: {e}")

        # Create 4x2 dashboards (all 6 styles)
        print(f"\n{'='*70}")
        print("MEMBUAT OVERALL ACHIEVEMENT DASHBOARDS (6 STYLES)")
        print(f"{'='*70}")

        print("\n  [Style 1] Donut/Gauge Chart (4x2 Grid)...")
        create_overall_achievement_dashboard(all_stats)
        print("    ✅ IKU_overall_achievement_4x2.png")

        print("\n  [Style 2] Bullet Chart (Vertical List)...")
        create_overall_achievement_bullet(all_stats)
        print("    ✅ IKU_overall_achievement_bullet.png")

        print("\n  [Style 3] KPI Cards (Modern Dashboard)...")
        create_overall_achievement_cards(all_stats)
        print("    ✅ IKU_overall_achievement_cards.png")

        print("\n  [Style 4] Bullet Chart (4x2 Grid - Compact)...")
        create_overall_achievement_bullet_4x2(all_stats)
        print("    ✅ IKU_overall_achievement_bullet_4x2.png")

        print("\n  [Style 5] Thermometer Chart (4x2 Grid)...")
        create_overall_achievement_thermometer(all_stats)
        print("    ✅ IKU_overall_achievement_thermometer.png")

        print("\n  [Style 6] Waffle Chart (4x2 Grid)...")
        create_overall_achievement_waffle(all_stats)
        print("    ✅ IKU_overall_achievement_waffle.png")

        print("\n  ✅ Semua overall achievement dashboards selesai dibuat (6 styles)")

        return {'stats': all_stats}

    # Process IKU yang dipilih
    all_results = {}
    all_stats = {}
    all_data = {}

    for iku in iku_list:
        if iku not in ALL_IKU:
            print(f"\n⚠️  IKU {iku} tidak valid. IKU yang tersedia: {', '.join(ALL_IKU)}")
            continue
        result = process_single_iku(iku)
        if result:
            all_results[iku] = result
            all_stats[iku] = result['stats']
            all_data[iku] = result['data']

    # Buat summary dashboard (opsional)
    if all_stats and not skip_dashboard:
        print(f"\n{'='*70}")
        print("MEMBUAT SUMMARY DASHBOARD")
        print(f"{'='*70}")
        create_summary_dashboard(all_stats, all_data)

    # Buat breakdown donut charts (opsional)
    if not skip_breakdown:
        print(f"\n{'='*70}")
        print("MEMBUAT BREAKDOWN DONUT CHARTS")
        print(f"{'='*70}")

        # Define main IKU groups and their sub-components
        iku_groups = {
            '1': ['11', '12', '13'],
            '2': ['21', '22', '23'],
            '3': ['31', '33'],
            '4': ['41', '42'],
            # IKU 5 and 6 are number-based, use combined stats directly
            '7': ['71'],
            '8': ['81']
        }

        for main_iku, sub_ikus in iku_groups.items():
            # Check if we have stats for this main IKU's sub-components
            sub_iku_stats = {s: all_stats[s] for s in sub_ikus if s in all_stats}

            if sub_iku_stats:
                print(f"\n  IKU {main_iku} breakdown ({', '.join(sub_iku_stats.keys())})...")
                create_breakdown_donut_charts(main_iku, sub_iku_stats)

                # Also create main IKU donut if combined stats available
                if main_iku in all_stats:
                    create_main_iku_donut(main_iku, all_stats[main_iku])

        # Special handling for IKU 5 and 6 (number-based, no sub-IKU breakdown)
        for num_based_iku in ['5', '6']:
            if num_based_iku in all_stats:
                print(f"\n  IKU {num_based_iku} (number-based)...")
                create_main_iku_donut(num_based_iku, all_stats[num_based_iku])

        print("\n  ✅ Breakdown donut charts selesai dibuat")

        # Generate category breakdowns for each sub-IKU
        print(f"\n{'='*70}")
        print("MEMBUAT CATEGORY BREAKDOWN CHARTS")
        print(f"{'='*70}")

        for iku in iku_list:
            if iku in CATEGORY_BREAKDOWN_FUNCTIONS:
                try:
                    CATEGORY_BREAKDOWN_FUNCTIONS[iku]()
                except Exception as e:
                    print(f"  ⚠️  Error creating breakdown for IKU {iku}: {e}")

        print("\n  ✅ Category breakdown charts selesai dibuat")

    # Create overall achievement dashboard (4x2 grid)
    if all_stats:
        print(f"\n{'='*70}")
        print("MEMBUAT OVERALL ACHIEVEMENT DASHBOARD (4x2)")
        print(f"{'='*70}")
        create_overall_achievement_dashboard(all_stats)
        print("  ✅ Overall achievement dashboard selesai dibuat")

    # Print summary
    print(f"\n{'='*70}")
    print("RINGKASAN HASIL")
    print(f"{'='*70}")
    for iku, stats in all_stats.items():
        iku_title = IKU_METADATA[iku]['title'].split(':')[0] if ':' in IKU_METADATA[iku]['title'] else f"IKU {iku}"
        print(f"{iku_title}: {stats['persentase']}% ({stats['pembilang']}/{stats['penyebut']})")

    print(f"\n{'='*70}")
    print("VISUALISASI SELESAI ✅")
    print(f"{'='*70}")
    print("\nStandar Publikasi yang Diterapkan:")
    print(f"  ✓ Font: {CONFIG['font_name'][0]} {CONFIG['font_size']}pt")
    print(f"  ✓ Resolution: {CONFIG['dpi']} DPI (publication quality)")
    print(f"  ✓ Color Palette: Colorblind-friendly (ColorBrewer)")
    print(f"  ✓ Line Width: {CONFIG['axes_linewidth']}pt (Nature/IEEE standard)")
    print("  ✓ Data-ink Ratio: Maximized")
    print("\nReferensi:")
    print("  - Environmental Modelling & Software (Ten Guidelines)")
    print("  - Nature, Science, IEEE standards")
    print("  - ColorBrewer2.org")

    return all_results


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Sistem Visualisasi IKU Fakultas Sains & Teknologi (Modular v2.0)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
Contoh penggunaan:
  python main_visualize_iku.py                    # Generate semua IKU
  python main_visualize_iku.py --iku 1            # Generate IKU 1 (gabungan 11,12,13)
  python main_visualize_iku.py --iku 31 33        # Generate IKU 31 dan 33 saja
  python main_visualize_iku.py --iku 4 --no-breakdown --no-dashboard  # IKU 4 saja

IKU yang tersedia: {", ".join(ALL_IKU)}

Mapping IKU (sesuai dokumen resmi):
  IKU 1 (PDF 1.1) = 11+12+13 (Lulusan)      → Target 60%
  IKU 2 (PDF 1.2) = 21+22+23 (Mahasiswa)    → Target 30%
  IKU 3 (PDF 2.1) = 31+33 (Dosen Tridharma) → Target 25%
  IKU 4 (PDF 2.2) = 41+42 (Dosen DUDI)      → Target 20.14%
        '''
    )

    parser.add_argument(
        '--iku', '-i',
        nargs='+',
        choices=ALL_IKU,
        metavar='IKU',
        help=f'Pilih IKU yang akan di-generate (default: semua). Pilihan: {", ".join(ALL_IKU)}'
    )

    parser.add_argument(
        '--no-breakdown',
        action='store_true',
        help='Skip pembuatan breakdown charts'
    )

    parser.add_argument(
        '--no-dashboard',
        action='store_true',
        help='Skip pembuatan summary dashboard'
    )

    parser.add_argument(
        '--no-cleanup',
        action='store_true',
        help='Jangan hapus file output sebelumnya'
    )

    parser.add_argument(
        '--4x2-only',
        action='store_true',
        dest='only_4x2',
        help='Hanya generate overall achievement dashboard 4x2'
    )

    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_arguments()
        results = main(
            iku_list=args.iku,
            skip_breakdown=args.no_breakdown,
            skip_dashboard=args.no_dashboard,
            skip_cleanup=args.no_cleanup,
            only_4x2=args.only_4x2
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Proses dibatalkan oleh user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
