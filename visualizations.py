"""
============================================================================
VISUALIZATIONS - SISTEM VISUALISASI IKU
============================================================================

Modul ini berisi semua fungsi visualisasi untuk IKU.

Author: Tim IKU FST
Version: 2.0 (Modular)
Last Updated: 2026-01-07
============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Wedge, FancyBboxPatch
from matplotlib.lines import Line2D
import textwrap

from config import CONFIG, COLORS, IKU_METADATA, JURUSAN_COLORS, JURUSAN_ORDER
from utils import sort_by_jurusan, assign_colors_by_jurusan, save_figure


# ============================================================================
# HORIZONTAL BAR CHART
# ============================================================================

def create_horizontal_bar_chart(data, iku_number, target=None):
    """
    Membuat horizontal bar chart berkualitas publikasi dengan grouping jurusan

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    iku_number : str
        Nomor IKU
    target : float, optional
        Nilai target untuk garis vertikal

    Returns:
    --------
    list : List of saved file paths
    """
    metadata = IKU_METADATA[iku_number]

    # Sort berdasarkan jurusan
    data_sorted = sort_by_jurusan(data.copy())

    # Assign colors
    colors = assign_colors_by_jurusan(data_sorted)

    prodi_list = data_sorted['Program Studi'].tolist()
    persentase_list = data_sorted['Persentase'].tolist()
    pembilang_list = data_sorted['Pembilang'].tolist()
    penyebut_list = data_sorted['Penyebut'].tolist()
    jurusan_list = data_sorted['Jurusan'].tolist()

    # Create figure dengan tinggi yang dinamis
    fig_height = max(6, len(prodi_list) * 0.4)
    fig, ax = plt.subplots(figsize=(11, fig_height))

    # Horizontal bars dengan edge yang lebih tegas
    y_pos = np.arange(len(prodi_list))
    bars = ax.barh(y_pos, persentase_list, color=colors,
                   edgecolor='#1a1a1a', linewidth=1.5,
                   alpha=0.88, height=0.75)

    # Tambahkan separator antar jurusan dengan garis horizontal
    current_jurusan = None
    for i, jurusan in enumerate(jurusan_list):
        if current_jurusan is not None and jurusan != current_jurusan:
            ax.axhline(y=i-0.5, color='#333333', linestyle='-',
                      linewidth=1.5, alpha=0.6, zorder=2)
        current_jurusan = jurusan

    # Target line
    if target:
        ax.axvline(x=target, color=COLORS['target'], linestyle='--',
                   linewidth=CONFIG['target_linewidth'], label=f'Target ({target}%)', zorder=3, alpha=0.95)

    # Labels pada bars - semua di luar dengan warna hitam
    for i, (bar, persen, pembilang, penyebut) in enumerate(zip(bars, persentase_list, pembilang_list, penyebut_list)):
        width = bar.get_width()
        persen_str = f'{int(persen)}' if persen == int(persen) else f'{persen:.1f}'
        label = f'{persen_str}% ({pembilang}/{penyebut})'

        ax.text(width + 1.5, bar.get_y() + bar.get_height()/2,
               label, ha='left', va='center',
               fontsize=11, fontweight='900', color='black')

    # Y-labels
    y_labels = [f"{prodi}" for prodi in prodi_list]

    # Styling
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels, fontsize=10, fontweight='600')
    ax.set_xlabel('Persentase (%)', fontsize=12, fontweight='700')
    ax.set_title(f"{metadata['title']}\n{metadata['subtitle']}",
                 fontsize=13, fontweight='900', pad=20)

    # Grid
    ax.xaxis.grid(True, linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax.set_axisbelow(True)

    # Spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # X-axis limit
    max_val = max(persentase_list) if persentase_list else 100
    if target:
        max_val = max(max_val, target)
    ax.set_xlim(0, max_val * 1.15)

    # Legend untuk jurusan
    legend_elements = [Patch(facecolor=JURUSAN_COLORS[j]['base'],
                             edgecolor='black', linewidth=1.0, label=j)
                      for j in JURUSAN_ORDER if j in jurusan_list]
    legend_elements = legend_elements[::-1]

    if target:
        legend_elements.append(Line2D([0], [0], color=COLORS['target'],
                                      linewidth=CONFIG['target_linewidth'], linestyle='--',
                                      label=f'Target ({target}%)'))

    ax.legend(handles=legend_elements, loc='upper right',
             fontsize=10, framealpha=0.95, edgecolor='black', fancybox=False)

    plt.tight_layout()

    saved_files = save_figure(fig, f'IKU_{iku_number}_horizontal')
    plt.close()

    return saved_files


# ============================================================================
# VERTICAL BAR CHART
# ============================================================================

def create_vertical_bar_chart(data, iku_number, target=None):
    """
    Membuat vertical bar chart berkualitas publikasi dengan grouping jurusan

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame dengan kolom: Program Studi, Pembilang, Penyebut, Persentase
    iku_number : str
        Nomor IKU
    target : float, optional
        Nilai target untuk garis horizontal

    Returns:
    --------
    list : List of saved file paths
    """
    metadata = IKU_METADATA[iku_number]

    # Sort berdasarkan jurusan
    data_sorted = sort_by_jurusan(data.copy())

    # Assign colors based on jurusan
    colors = assign_colors_by_jurusan(data_sorted)

    prodi_list = data_sorted['Program Studi'].tolist()
    persentase_list = data_sorted['Persentase'].tolist()
    pembilang_list = data_sorted['Pembilang'].tolist()
    penyebut_list = data_sorted['Penyebut'].tolist()
    jurusan_list = data_sorted['Jurusan'].tolist()

    # Buat figure dengan width yang lebih lebar untuk spacing
    fig_width = max(14, len(prodi_list) * 1.0)
    fig, ax = plt.subplots(figsize=(fig_width, 7))

    # Vertical bars
    x_pos = np.arange(len(prodi_list))
    bars = ax.bar(x_pos, persentase_list, color=colors,
                  edgecolor='#1a1a1a', linewidth=1.5,
                  alpha=0.88, width=0.75)

    # Tambahkan separator antar jurusan dengan garis vertikal
    current_jurusan = None
    for i, jurusan in enumerate(jurusan_list):
        if current_jurusan is not None and jurusan != current_jurusan:
            ax.axvline(x=i-0.5, color='#333333', linestyle='-',
                      linewidth=2.0, alpha=0.6, zorder=2)
        current_jurusan = jurusan

    # Target line
    if target:
        ax.axhline(y=target, color=COLORS['target'], linestyle='--',
                   linewidth=CONFIG['target_linewidth'], label=f'Target ({target}%)', zorder=3, alpha=0.95)

    # Hitung offset proporsional berdasarkan range data
    max_val = max(persentase_list) if persentase_list else 100
    if target:
        max_val = max(max_val, target)
    label_offset = max_val * 0.02

    # Label di atas bars
    for bar, persen, pembilang, penyebut in zip(bars, persentase_list, pembilang_list, penyebut_list):
        height = bar.get_height()
        persen_str = f'{int(persen)}' if persen == int(persen) else f'{persen:.1f}'
        label = f'{persen_str}%\n({pembilang}/{penyebut})'
        ax.text(bar.get_x() + bar.get_width()/2., height + label_offset,
                label, ha='center', va='bottom', fontsize=10, fontweight='900')

    # Styling - X-axis labels dengan multi-line wrapping
    wrapped_labels = ['\n'.join(textwrap.wrap(prodi, width=12)) for prodi in prodi_list]
    ax.set_xticks(x_pos)
    ax.set_xticklabels(wrapped_labels, rotation=0, ha='center', fontsize=10, fontweight='600')
    ax.set_ylabel('Persentase (%)', fontsize=12, fontweight='700')
    ax.set_title(f"{metadata['title']}\n{metadata['subtitle']}",
                 fontsize=13, fontweight='900', pad=15)

    # Grid
    ax.yaxis.grid(True, linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax.set_axisbelow(True)

    # Spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # Y-axis limit
    ax.set_ylim(0, max_val * 1.15)

    # Legend untuk jurusan
    legend_elements = [Patch(facecolor=JURUSAN_COLORS[j]['base'],
                             edgecolor='black', linewidth=1.0, label=j)
                      for j in JURUSAN_ORDER if j in jurusan_list]
    if target:
        legend_elements.append(Line2D([0], [0], color=COLORS['target'],
                                      linewidth=CONFIG['target_linewidth'], linestyle='--',
                                      label=f'Target ({target}%)'))

    # Posisi legend: upper left untuk IKU 1 & 2, upper right untuk lainnya
    legend_loc = 'upper left' if iku_number in ['1', '11', '12', '13', '2', '21', '22', '23'] else 'upper right'
    ax.legend(handles=legend_elements, loc=legend_loc,
             fontsize=10, framealpha=0.95, edgecolor='black', fancybox=False)

    plt.tight_layout()

    saved_files = save_figure(fig, f'IKU_{iku_number}_vertical')
    plt.close()

    return saved_files


# ============================================================================
# BREAKDOWN DONUT CHARTS
# ============================================================================

# Mapping for breakdown components based on Dashboard PDF
IKU_BREAKDOWN_CONFIG = {
    '1': {
        'sub_ikus': ['11', '12', '13'],
        'main_title': 'IKU 1.1: Lulusan Bekerja/Studi Lanjut/Wiraswasta',
        'target': 60
    },
    '2': {
        'sub_ikus': ['21', '22', '23'],
        'main_title': 'IKU 1.2: Mahasiswa Berkegiatan di Luar Prodi/Meraih Prestasi',
        'target': 30
    },
    '3': {
        'sub_ikus': ['31', '33'],
        'main_title': 'IKU 2.1: Dosen Tridharma di PT Lain/Membimbing',
        'target': 25
    },
    '4': {
        'sub_ikus': ['41', '42'],
        'main_title': 'IKU 2.2: Dosen Sertifikat DUDI/Pengajar Praktisi',
        'target': 20.14
    },
    '5': {
        'sub_ikus': ['51'],
        'main_title': 'IKU 5: Luaran Dosen Rekognisi Internasional',
        'target': 5,
        'is_number_based': True,
        'unit': 'luaran'
    },
    '6': {
        'sub_ikus': ['62'],
        'main_title': 'IKU 6: Kerjasama per Program Studi',
        'target': 2,
        'is_number_based': True,
        'unit': 'per prodi'
    },
    '7': {
        'sub_ikus': ['71'],
        'main_title': 'IKU 7: Mata Kuliah PJBL/Case Method',
        'target': 50
    },
    '8': {
        'sub_ikus': ['81'],
        'main_title': 'IKU 8: Prodi Akreditasi Internasional',
        'target': 10
    }
}

# Short labels for donut charts
DONUT_LABELS = {
    '11': 'Bekerja',
    '12': 'Studi Lanjut',
    '13': 'Wiraswasta',
    '21': 'MBKM',
    '22': 'Prestasi',
    '23': 'Karya/HKI',
    '31': 'Tridharma\ndi PT Lain',
    '33': 'Membimbing\nMahasiswa',
    '41': 'Sertifikat\nDUDI',
    '42': 'Pengajar\nPraktisi',
    '51': 'Luaran\nRekognisi',
    '62': 'Kerjasama',
    '71': 'PJBL/Case\nMethod',
    '81': 'Akreditasi\nInternasional'
}

# Colors for each sub-IKU donut
DONUT_COLORS = {
    '11': '#5B9BD5',  # Blue
    '12': '#70AD47',  # Green
    '13': '#ED7D31',  # Orange
    '21': '#9966CC',  # Purple
    '22': '#E85D75',  # Pink/Red
    '23': '#00B0F0',  # Cyan
    '31': '#5B9BD5',  # Blue
    '33': '#70AD47',  # Green
    '41': '#ED7D31',  # Orange
    '42': '#9966CC',  # Purple
    '51': '#FF6B6B',  # Coral Red - Luaran Rekognisi
    '62': '#4ECDC4',  # Teal - Kerjasama
    '71': '#00B0F0',  # Cyan - Mata Kuliah
    '81': '#2E7D32',  # Dark Green - Akreditasi
}


def create_breakdown_donut_charts(main_iku, sub_iku_stats):
    """
    Membuat donut charts untuk breakdown komponen setiap IKU utama
    DUAL RING DESIGN: Outer ring = Target, Inner ring = Actual
    Visual comparison: immediately see if actual exceeds target

    Parameters:
    -----------
    main_iku : str
        Nomor IKU utama ('1', '2', '3', atau '4')
    sub_iku_stats : dict
        Dictionary berisi statistik untuk setiap sub-IKU
        Format: {'11': {'pembilang': x, 'penyebut': y, 'persentase': z}, ...}

    Returns:
    --------
    list : List of saved file paths
    """
    from matplotlib.patches import FancyBboxPatch, Wedge, Circle
    from matplotlib.collections import PatchCollection

    if main_iku not in IKU_BREAKDOWN_CONFIG:
        print(f"  ⚠️  IKU {main_iku} tidak memiliki konfigurasi breakdown")
        return []

    config = IKU_BREAKDOWN_CONFIG[main_iku]
    sub_ikus = config['sub_ikus']
    main_title = config['main_title']
    target = config['target']

    # Filter only available sub-IKUs
    available_sub_ikus = [s for s in sub_ikus if s in sub_iku_stats]

    if not available_sub_ikus:
        print(f"  ⚠️  Tidak ada data sub-IKU untuk IKU {main_iku}")
        return []

    num_charts = len(available_sub_ikus)

    # Create figure
    fig_width = 5.0 * num_charts
    fig_height = 6.5
    fig, axes = plt.subplots(1, num_charts, figsize=(fig_width, fig_height))

    if num_charts == 1:
        axes = [axes]

    for idx, sub_iku in enumerate(available_sub_ikus):
        ax = axes[idx]
        stats = sub_iku_stats.get(sub_iku, {'pembilang': 0, 'penyebut': 1, 'persentase': 0})

        pct = stats['persentase']
        pembilang = stats['pembilang']
        penyebut = stats['penyebut']

        # Determine status and colors
        achieved = pct >= target
        if achieved:
            actual_color = '#28a745'  # Green
            status_color = '#28a745'
            status_bg = '#d4edda'
            status_text = '✓ ACHIEVED'
            diff_text = f'+{pct - target:.1f}%'
        else:
            actual_color = DONUT_COLORS.get(sub_iku, '#5B9BD5')
            status_color = '#dc3545'
            status_bg = '#f8d7da'
            status_text = 'GAP'
            diff_text = f'-{target - pct:.1f}%'

        # === OUTER RING: TARGET (gray, thinner) ===
        # Background track (full circle)
        outer_bg = Wedge((0, 0), 1.15, 0, 360, width=0.12,
                        facecolor='#E0E0E0', edgecolor='white', linewidth=2)
        ax.add_patch(outer_bg)

        # Target fill - clockwise from 12 o'clock
        target_angle = 360 * (target / 100)
        outer_fill = Wedge((0, 0), 1.15, 90 - target_angle, 90, width=0.12,
                          facecolor='#9E9E9E', edgecolor='white', linewidth=2)
        ax.add_patch(outer_fill)

        # === INNER RING: ACTUAL (colored, thicker) ===
        # Background track (full circle)
        inner_bg = Wedge((0, 0), 0.98, 0, 360, width=0.22,
                        facecolor='#F5F5F5', edgecolor='white', linewidth=2)
        ax.add_patch(inner_bg)

        # Actual fill - clockwise from 12 o'clock
        actual_angle = 360 * (min(pct, 100) / 100)
        inner_fill = Wedge((0, 0), 0.98, 90 - actual_angle, 90, width=0.22,
                          facecolor=actual_color, edgecolor='white', linewidth=2)
        ax.add_patch(inner_fill)

        # === CENTER: White circle background ===
        center_circle = Circle((0, 0), 0.72, facecolor='white', edgecolor='none')
        ax.add_patch(center_circle)

        # === CENTER TEXT ===
        # Large percentage
        pct_str = f'{pct:.1f}%' if pct != int(pct) else f'{int(pct)}%'
        ax.text(0, 0.12, pct_str,
               ha='center', va='center',
               fontsize=36, fontweight='900', color='#1a1a1a')

        # Fraction
        ax.text(0, -0.18, f'{pembilang}/{penyebut}',
               ha='center', va='center',
               fontsize=12, color='#666666', fontweight='600')

        # === LABEL (category name) ===
        label = DONUT_LABELS.get(sub_iku, f'IKU {sub_iku}')
        label_clean = label.replace('\n', ' ')
        ax.text(0, -1.28, label_clean,
               ha='center', va='center',
               fontsize=14, fontweight='bold', color='#333333')

        # === 2-COLUMN LAYOUT: Legend (left) | Status (right) ===
        row_y = -1.58

        # LEFT COLUMN: Legend
        # Target
        ax.plot([-1.18], [row_y + 0.12], 's', markersize=10, color='#9E9E9E', zorder=5)
        ax.text(-1.05, row_y + 0.12, f'Target {target}%',
               ha='left', va='center', fontsize=11, fontweight='700', color='#666666')
        # Realisasi
        ax.plot([-1.18], [row_y - 0.12], 's', markersize=10, color=actual_color, zorder=5)
        ax.text(-1.05, row_y - 0.12, f'Realisasi {pct:.1f}%',
               ha='left', va='center', fontsize=11, fontweight='700', color='#666666')

        # RIGHT COLUMN: Status Badge
        badge = FancyBboxPatch((0.18, row_y - 0.22), 1.12, 0.44,
                               boxstyle="round,pad=0.02,rounding_size=0.10",
                               facecolor=status_bg, edgecolor=status_color,
                               linewidth=2.5, transform=ax.transData, zorder=5)
        ax.add_patch(badge)

        ax.text(0.74, row_y, f'{status_text}\n{diff_text}',
               ha='center', va='center',
               fontsize=13, color=status_color, fontweight='900', zorder=6,
               linespacing=1.1)

        ax.set_xlim(-1.45, 1.45)
        ax.set_ylim(-1.95, 1.35)
        ax.set_aspect('equal')
        ax.axis('off')

    # Title
    fig.suptitle(main_title,
                 fontsize=15, fontweight='bold', y=0.97, color='#1a1a1a')

    fig.text(0.5, 0.92, 'Fakultas Sains & Teknologi 2025',
             ha='center', fontsize=10, color='#666666')

    plt.tight_layout(rect=[0, 0.02, 1, 0.90])

    saved_files = save_figure(fig, f'IKU_{main_iku}_breakdown_donut')
    plt.close()

    return saved_files


def create_main_iku_donut(main_iku, combined_stats):
    """
    Membuat single donut chart untuk IKU utama (combined)
    DUAL RING DESIGN: Outer ring = Target, Inner ring = Actual

    Parameters:
    -----------
    main_iku : str
        Nomor IKU utama ('1', '2', '3', atau '4')
    combined_stats : dict
        Statistik gabungan {'pembilang': x, 'penyebut': y, 'persentase': z}

    Returns:
    --------
    list : List of saved file paths
    """
    from matplotlib.patches import FancyBboxPatch, Wedge, Circle

    if main_iku not in IKU_BREAKDOWN_CONFIG:
        return []

    config = IKU_BREAKDOWN_CONFIG[main_iku]
    main_title = config['main_title']
    target = config['target']

    pct = combined_stats['persentase']
    pembilang = combined_stats['pembilang']
    penyebut = combined_stats['penyebut']

    # Create figure
    fig, ax = plt.subplots(figsize=(6, 7))

    # Determine status and colors
    if pct >= target:
        actual_color = '#28a745'  # Green
        status_text = '✓ ACHIEVED'
        status_color = '#28a745'
        status_bg = '#d4edda'
        diff_text = f'+{pct - target:.1f}%'
    elif pct >= target * 0.7:
        actual_color = '#ffc107'  # Yellow
        status_text = 'GAP'
        status_color = '#856404'
        status_bg = '#fff3cd'
        diff_text = f'-{target - pct:.1f}%'
    else:
        actual_color = '#dc3545'  # Red
        status_text = 'GAP'
        status_color = '#dc3545'
        status_bg = '#f8d7da'
        diff_text = f'-{target - pct:.1f}%'

    # === OUTER RING: TARGET (gray, thinner) ===
    outer_bg = Wedge((0, 0), 1.2, 0, 360, width=0.14,
                    facecolor='#E0E0E0', edgecolor='white', linewidth=2)
    ax.add_patch(outer_bg)

    target_angle = 360 * (target / 100)
    outer_fill = Wedge((0, 0), 1.2, 90 - target_angle, 90, width=0.14,
                      facecolor='#9E9E9E', edgecolor='white', linewidth=2)
    ax.add_patch(outer_fill)

    # === INNER RING: ACTUAL (colored, thicker) ===
    inner_bg = Wedge((0, 0), 1.0, 0, 360, width=0.25,
                    facecolor='#F5F5F5', edgecolor='white', linewidth=2)
    ax.add_patch(inner_bg)

    actual_angle = 360 * (min(pct, 100) / 100)
    inner_fill = Wedge((0, 0), 1.0, 90 - actual_angle, 90, width=0.25,
                      facecolor=actual_color, edgecolor='white', linewidth=2)
    ax.add_patch(inner_fill)

    # === CENTER: White circle ===
    center_circle = Circle((0, 0), 0.70, facecolor='white', edgecolor='none')
    ax.add_patch(center_circle)

    # === CENTER TEXT ===
    pct_str = f'{pct:.2f}%' if pct != int(pct) else f'{int(pct)}%'
    ax.text(0, 0.12, pct_str,
           ha='center', va='center',
           fontsize=40, fontweight='900', color='#1a1a1a')

    ax.text(0, -0.20, f'{pembilang}/{penyebut}',
           ha='center', va='center',
           fontsize=14, color='#666666', fontweight='600')

    # === LABEL ===
    ax.text(0, -1.38, 'COMBINED',
           ha='center', va='center',
           fontsize=14, fontweight='bold', color='#888888')

    # === 2-COLUMN LAYOUT: Legend (left) | Status (right) ===
    row_y = -1.72

    # LEFT COLUMN: Legend (stacked)
    # Target
    ax.plot([-1.25], [row_y + 0.14], 's', markersize=12, color='#9E9E9E', zorder=5)
    ax.text(-1.10, row_y + 0.14, f'Target {target}%',
           ha='left', va='center', fontsize=13, fontweight='700', color='#666666')
    # Realisasi
    ax.plot([-1.25], [row_y - 0.14], 's', markersize=12, color=actual_color, zorder=5)
    ax.text(-1.10, row_y - 0.14, f'Realisasi {pct:.1f}%',
           ha='left', va='center', fontsize=13, fontweight='700', color='#666666')

    # RIGHT COLUMN: Status Badge
    badge = FancyBboxPatch((0.22, row_y - 0.26), 1.22, 0.52,
                           boxstyle="round,pad=0.02,rounding_size=0.12",
                           facecolor=status_bg, edgecolor=status_color,
                           linewidth=2.5, transform=ax.transData, zorder=5)
    ax.add_patch(badge)

    ax.text(0.83, row_y, f'{status_text}\n{diff_text}',
           ha='center', va='center',
           fontsize=15, color=status_color, fontweight='900', zorder=6,
           linespacing=1.1)

    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-2.10, 1.42)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    fig.suptitle(main_title,
                fontsize=15, fontweight='bold', y=0.97, color='#1a1a1a')

    fig.text(0.5, 0.92, 'Fakultas Sains & Teknologi 2025',
             ha='center', fontsize=10, color='#666666')

    plt.tight_layout(rect=[0, 0.02, 1, 0.90])

    saved_files = save_figure(fig, f'IKU_{main_iku}_main_donut')
    plt.close()

    return saved_files


# ============================================================================
# SUMMARY DASHBOARD
# ============================================================================

def create_summary_dashboard(all_stats, all_data):
    """
    Membuat dashboard summary untuk semua IKU dengan desain modern dan compact

    Parameters:
    -----------
    all_stats : dict
        Dictionary berisi statistik keseluruhan untuk setiap IKU
    all_data : dict
        Dictionary berisi data detail untuk setiap IKU

    Returns:
    --------
    list : List of saved file paths
    """
    num_iku = len(all_stats)
    fig, axes = plt.subplots(1, num_iku, figsize=(3.5 * num_iku, 6))

    if num_iku == 1:
        axes = [axes]

    iku_list = sorted(all_stats.keys())

    for idx, iku in enumerate(iku_list):
        ax = axes[idx]
        metadata = IKU_METADATA[iku]
        stats = all_stats.get(iku, {'pembilang': 0, 'penyebut': 1, 'persentase': 0})

        # Donut chart
        pct = stats['persentase']
        sizes = [pct, 100 - pct]

        color_map = {
            '1': '#5B9BD5', '11': '#5B9BD5', '12': '#70AD47', '13': '#ED7D31',
            '2': '#9966CC', '21': '#9966CC', '22': '#E85D75', '23': '#7F8C8D',
            '3': '#5B9BD5', '31': '#5B9BD5', '33': '#70AD47',
            '4': '#ED7D31', '41': '#ED7D31', '42': '#9966CC'
        }
        colors_donut = [color_map.get(iku, '#70AD47'), '#E8E8E8']

        wedges, texts, autotexts = ax.pie(
            sizes,
            colors=colors_donut,
            autopct='',
            startangle=90,
            wedgeprops=dict(width=0.35, edgecolor='white', linewidth=2.5),
            textprops={'fontsize': 10, 'fontweight': 'bold'}
        )

        ax.text(0, 0.08, f'{pct:.1f}%',
               ha='center', va='center',
               fontsize=24, fontweight='bold', color='#333333')

        ax.text(0, -0.22, f'{stats["pembilang"]}/{stats["penyebut"]}',
               ha='center', va='center',
               fontsize=9, color='#666666', fontweight='500')

        title_text = f"IKU {iku}\n{textwrap.fill(metadata['title'], width=28)}"
        ax.set_title(title_text,
                    fontsize=9, fontweight='bold',
                    pad=12, linespacing=1.2)

    plt.suptitle('Ringkasan Pencapaian IKU\nFakultas Sains & Teknologi',
                 fontsize=12, fontweight='bold', y=0.99, linespacing=1.1)

    plt.tight_layout(rect=[0, 0, 1, 0.93])

    saved_files = save_figure(fig, 'IKU_summary_dashboard')
    plt.close()

    return saved_files


def create_overall_achievement_dashboard(all_stats):
    """
    Membuat dashboard capaian keseluruhan 8 IKU dalam layout 4x2 grid
    Berdasarkan best practice KPI dashboard design

    Parameters:
    -----------
    all_stats : dict
        Dictionary berisi statistik untuk IKU 1-8

    Returns:
    --------
    list : List of saved file paths
    """
    # IKU yang akan ditampilkan (main combined IKUs only)
    main_ikus = ['1', '2', '3', '4', '5', '6', '7', '8']

    # Filter hanya IKU yang tersedia
    available_ikus = [iku for iku in main_ikus if iku in all_stats]

    if len(available_ikus) == 0:
        print("  ⚠️  Tidak ada data IKU gabungan untuk dashboard")
        return []

    # Create 4x2 grid
    fig, axes = plt.subplots(2, 4, figsize=(20, 12))
    axes_flat = axes.flatten()

    # IKU Titles for each main IKU
    IKU_TITLES = {
        '1': 'Lulusan\nBekerja/Studi/Wiraswasta',
        '2': 'Mahasiswa\nBerkegiatan/Prestasi',
        '3': 'Dosen Tridharma\ndi PT Lain',
        '4': 'Dosen Sertifikat\nDUDI/Praktisi',
        '5': 'Luaran Dosen\nRekognisi Internasional',
        '6': 'Kerjasama\nper Program Studi',
        '7': 'Mata Kuliah\nPJBL/Case Method',
        '8': 'Prodi Akreditasi\nInternasional'
    }

    # Target values
    TARGETS = {
        '1': 60, '2': 30, '3': 25, '4': 20.14,
        '5': 5, '6': 2, '7': 50, '8': 10
    }

    # Number-based IKUs
    NUMBER_BASED = ['5', '6']

    for idx, iku in enumerate(main_ikus):
        ax = axes_flat[idx]

        if iku in all_stats:
            stats = all_stats[iku]
            pct = stats['persentase']
            pembilang = stats['pembilang']
            penyebut = stats['penyebut']
            target = TARGETS.get(iku, 0)

            is_number_based = iku in NUMBER_BASED

            # Determine status
            if pct >= 100:  # Target achieved (for percentage-based: pct >= target)
                actual_color = '#28a745'  # Green
                status_text = 'ACHIEVED'
                status_color = '#28a745'
                status_bg = '#d4edda'
            elif pct >= 70:
                actual_color = '#ffc107'  # Yellow
                status_text = 'ON TRACK'
                status_color = '#856404'
                status_bg = '#fff3cd'
            else:
                actual_color = '#dc3545'  # Red
                status_text = 'GAP'
                status_color = '#dc3545'
                status_bg = '#f8d7da'

            # For percentage-based, check against actual target
            if not is_number_based:
                if pct >= target:
                    actual_color = '#28a745'
                    status_text = 'ACHIEVED'
                    status_color = '#28a745'
                    status_bg = '#d4edda'
                    diff_text = f'+{pct - target:.1f}%'
                elif pct >= target * 0.7:
                    actual_color = '#ffc107'
                    status_text = 'ON TRACK'
                    status_color = '#856404'
                    status_bg = '#fff3cd'
                    diff_text = f'-{target - pct:.1f}%'
                else:
                    actual_color = '#dc3545'
                    status_text = 'GAP'
                    status_color = '#dc3545'
                    status_bg = '#f8d7da'
                    diff_text = f'-{target - pct:.1f}%'
            else:
                # For number-based
                diff_text = f'+{pct - 100:.1f}%' if pct >= 100 else f'-{100 - pct:.1f}%'

            # === DUAL RING DONUT ===
            # Outer ring - Target (gray)
            if is_number_based:
                target_angle = 360 * min(1, 100 / pct) if pct > 0 else 360
            else:
                target_angle = 360 * (target / 100)

            outer_bg = Wedge((0, 0), 1.15, 0, 360, width=0.12,
                            facecolor='#E8E8E8', edgecolor='white', linewidth=2)
            ax.add_patch(outer_bg)

            outer_fill = Wedge((0, 0), 1.15, 90 - target_angle, 90, width=0.12,
                              facecolor='#9E9E9E', edgecolor='white', linewidth=2)
            ax.add_patch(outer_fill)

            # Inner ring - Actual (colored)
            actual_angle = 360 * min(pct / 100, 1) if not is_number_based else 360

            inner_bg = Wedge((0, 0), 0.98, 0, 360, width=0.18,
                            facecolor='#F5F5F5', edgecolor='white', linewidth=2)
            ax.add_patch(inner_bg)

            inner_fill = Wedge((0, 0), 0.98, 90 - actual_angle, 90, width=0.18,
                              facecolor=actual_color, edgecolor='white', linewidth=2)
            ax.add_patch(inner_fill)

            # Center text
            if is_number_based:
                center_text = f'{pembilang}'
                sub_text = f'Target: {penyebut}'
            else:
                center_text = f'{pct:.1f}%'
                sub_text = f'{pembilang}/{penyebut}'

            ax.text(0, 0.08, center_text,
                   ha='center', va='center',
                   fontsize=28, fontweight='bold', color='#333333')

            ax.text(0, -0.25, sub_text,
                   ha='center', va='center',
                   fontsize=11, color='#666666', fontweight='600')

            # IKU number badge
            ax.text(0, 0.75, f'IKU {iku}',
                   ha='center', va='center',
                   fontsize=14, fontweight='bold', color='#333333',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                            edgecolor='#CCCCCC', linewidth=1.5))

            # Title below donut
            ax.text(0, -1.45, IKU_TITLES.get(iku, f'IKU {iku}'),
                   ha='center', va='center',
                   fontsize=11, fontweight='bold', color='#333333',
                   linespacing=1.2)

            # Status badge
            badge = FancyBboxPatch((-0.65, -2.05), 1.3, 0.35,
                                   boxstyle="round,pad=0.02,rounding_size=0.10",
                                   facecolor=status_bg, edgecolor=status_color,
                                   linewidth=2, transform=ax.transData)
            ax.add_patch(badge)

            ax.text(0, -1.88, f'{status_text} {diff_text}',
                   ha='center', va='center',
                   fontsize=12, color=status_color, fontweight='bold')

            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-2.3, 1.3)

        else:
            # No data for this IKU
            ax.text(0, 0, f'IKU {iku}\nNo Data',
                   ha='center', va='center',
                   fontsize=14, color='#999999', fontweight='bold')
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-2.3, 1.3)

        ax.set_aspect('equal')
        ax.axis('off')

    # Main title
    fig.suptitle('CAPAIAN IKU FAKULTAS SAINS & TEKNOLOGI',
                fontsize=20, fontweight='bold', y=0.98, color='#1a1a1a')

    fig.text(0.5, 0.94, 'Universitas Jambi 2025',
            ha='center', fontsize=14, color='#666666', style='italic')

    # Legend at bottom
    fig.text(0.5, 0.02,
            '■ Target (Outer Ring)    ■ Realisasi (Inner Ring)    |    Green = Achieved    Yellow = On Track    Red = Gap',
            ha='center', fontsize=11, color='#666666')

    plt.tight_layout(rect=[0.02, 0.05, 0.98, 0.92])

    saved_files = save_figure(fig, 'IKU_overall_achievement_4x2')
    plt.close()

    return saved_files


def create_overall_achievement_bullet(all_stats):
    """
    Membuat dashboard capaian keseluruhan 8 IKU dalam format Bullet Chart
    Bullet chart invented by Stephen Few as space-efficient alternative to gauges

    Parameters:
    -----------
    all_stats : dict
        Dictionary berisi statistik semua IKU {iku_number: stats_dict}

    Returns:
    --------
    list : List of saved file paths
    """
    # Main IKUs to display (1-8)
    main_ikus = ['1', '2', '3', '4', '5', '6', '7', '8']

    # IKU labels
    iku_labels = {
        '1': 'IKU 1: Lulusan Bekerja/\nStudi/Wiraswasta',
        '2': 'IKU 2: Mahasiswa\nBerkegiatan/Prestasi',
        '3': 'IKU 3: Dosen Tridharma\ndi PT Lain',
        '4': 'IKU 4: Dosen Sertifikat\nDUDI/Praktisi',
        '5': 'IKU 5: Luaran Dosen\nRekognisi Internasional',
        '6': 'IKU 6: Kerjasama\nper Program Studi',
        '7': 'IKU 7: Mata Kuliah\nPJBL/Case Method',
        '8': 'IKU 8: Prodi Akreditasi\nInternasional'
    }

    # Targets (percentage-based for most, except 5 and 6)
    targets = {
        '1': 60, '2': 30, '3': 25, '4': 20.14,
        '5': 100,  # Will show as % of target (5)
        '6': 100,  # Will show as % of target (2 per prodi)
        '7': 50, '8': 10
    }

    NUMBER_BASED = ['5', '6']

    # Create figure
    fig, ax = plt.subplots(figsize=(16, 10))

    y_positions = np.arange(len(main_ikus))[::-1]  # Reverse for top-to-bottom
    bar_height = 0.6

    # Color scheme for qualitative ranges (light to dark)
    range_colors = ['#f0f0f0', '#d9d9d9', '#bdbdbd']  # Poor, Satisfactory, Good

    for idx, iku in enumerate(main_ikus):
        y = y_positions[idx]
        target = targets.get(iku, 50)

        if iku in all_stats:
            stats = all_stats[iku]
            pembilang = stats['pembilang']
            penyebut = stats['penyebut']

            if iku in NUMBER_BASED:
                # Number-based: show actual vs target as percentage
                if iku == '5':
                    actual_pct = (pembilang / 5) * 100  # Target is 5
                else:
                    actual_pct = (pembilang / 2) * 100  # Target is 2 per prodi
                value_text = f'{pembilang}' if iku == '5' else f'{pembilang:.2f}'
                target_text = 'Target: 5' if iku == '5' else 'Target: 2/prodi'
            else:
                actual_pct = stats['persentase']
                value_text = f'{actual_pct:.1f}%'
                target_text = f'Target: {target}%'

            # Determine status color
            if actual_pct >= target:
                bar_color = '#2E7D32'  # Green - achieved
                status = 'ACHIEVED'
            elif actual_pct >= target * 0.8:
                bar_color = '#F9A825'  # Yellow - on track
                status = 'ON TRACK'
            else:
                bar_color = '#C62828'  # Red - gap
                status = 'GAP'

            # Draw qualitative range backgrounds (scaled to max 150% for over-achievers)
            max_range = max(150, actual_pct + 20)
            range_widths = [max_range * 0.5, max_range * 0.75, max_range]

            for i, width in enumerate(range_widths):
                ax.barh(y, width, height=bar_height * 1.5, left=0,
                       color=range_colors[i], edgecolor='none', zorder=1)

            # Draw actual value bar (thinner, on top)
            ax.barh(y, min(actual_pct, max_range), height=bar_height * 0.6, left=0,
                   color=bar_color, edgecolor='#1a1a1a', linewidth=1, zorder=3)

            # Draw target marker (vertical line)
            ax.plot([target, target], [y - bar_height * 0.75, y + bar_height * 0.75],
                   color='#1a1a1a', linewidth=3, zorder=4)

            # Add value text at end of bar
            text_x = min(actual_pct, max_range) + 3
            ax.text(text_x, y, value_text, va='center', ha='left',
                   fontsize=12, fontweight='bold', color=bar_color)

            # Add status badge
            badge_x = max_range + 25
            badge_color = bar_color
            ax.text(badge_x, y, status, va='center', ha='left',
                   fontsize=10, fontweight='bold', color='white',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=badge_color,
                            edgecolor='none', alpha=0.9))

            # Add fraction text
            if iku not in NUMBER_BASED:
                ax.text(badge_x + 60, y, f'({pembilang}/{penyebut})',
                       va='center', ha='left', fontsize=9, color='#666666')
            else:
                ax.text(badge_x + 60, y, target_text,
                       va='center', ha='left', fontsize=9, color='#666666')

        else:
            # No data
            ax.text(50, y, 'No Data', va='center', ha='center',
                   fontsize=11, color='#999999', style='italic')

    # Y-axis labels
    ax.set_yticks(y_positions)
    ax.set_yticklabels([iku_labels[iku] for iku in main_ikus],
                       fontsize=11, fontweight='600')

    # X-axis
    ax.set_xlim(0, 220)
    ax.set_xlabel('Persentase Capaian (%)', fontsize=12, fontweight='600')
    ax.set_xticks([0, 25, 50, 75, 100, 125, 150])
    ax.tick_params(axis='x', labelsize=10)

    # Grid
    ax.xaxis.grid(True, linestyle='--', alpha=0.4, zorder=0)
    ax.set_axisbelow(True)

    # Spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # Title
    ax.set_title('CAPAIAN IKU FAKULTAS SAINS & TEKNOLOGI\nUniversitas Jambi 2025',
                fontsize=16, fontweight='bold', pad=20, color='#1a1a1a')

    # Legend
    legend_elements = [
        Patch(facecolor='#f0f0f0', edgecolor='#999999', label='Poor (<50%)'),
        Patch(facecolor='#d9d9d9', edgecolor='#999999', label='Satisfactory (50-75%)'),
        Patch(facecolor='#bdbdbd', edgecolor='#999999', label='Good (>75%)'),
        Line2D([0], [0], color='#1a1a1a', linewidth=3, label='Target'),
        Patch(facecolor='#2E7D32', edgecolor='none', label='Achieved'),
        Patch(facecolor='#F9A825', edgecolor='none', label='On Track'),
        Patch(facecolor='#C62828', edgecolor='none', label='Gap'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', ncol=4,
             frameon=True, framealpha=0.95, fontsize=9)

    plt.tight_layout()

    saved_files = save_figure(fig, 'IKU_overall_achievement_bullet')
    plt.close()

    return saved_files


def create_overall_achievement_cards(all_stats):
    """
    Membuat dashboard capaian keseluruhan 8 IKU dalam format Modern KPI Cards
    Style: Large metric + progress bar + trend indicator

    Parameters:
    -----------
    all_stats : dict
        Dictionary berisi statistik semua IKU {iku_number: stats_dict}

    Returns:
    --------
    list : List of saved file paths
    """
    # Main IKUs to display (1-8)
    main_ikus = ['1', '2', '3', '4', '5', '6', '7', '8']

    # IKU short labels
    iku_labels = {
        '1': 'Lulusan\nBekerja/Studi/Wiraswasta',
        '2': 'Mahasiswa\nBerkegiatan/Prestasi',
        '3': 'Dosen Tridharma\ndi PT Lain',
        '4': 'Dosen Sertifikat\nDUDI/Praktisi',
        '5': 'Luaran Dosen\nRekognisi Internasional',
        '6': 'Kerjasama\nper Program Studi',
        '7': 'Mata Kuliah\nPJBL/Case Method',
        '8': 'Prodi Akreditasi\nInternasional'
    }

    # Targets
    targets = {
        '1': 60, '2': 30, '3': 25, '4': 20.14,
        '5': 5,   # Actual number target
        '6': 2,   # Per prodi target
        '7': 50, '8': 10
    }

    NUMBER_BASED = ['5', '6']

    # Create figure with 4x2 grid
    fig = plt.figure(figsize=(20, 12))

    # Create grid for cards
    gs = fig.add_gridspec(2, 4, hspace=0.35, wspace=0.25,
                          left=0.05, right=0.95, top=0.88, bottom=0.08)

    for idx, iku in enumerate(main_ikus):
        row = idx // 4
        col = idx % 4

        # Create card subplot
        ax = fig.add_subplot(gs[row, col])

        # Card background
        card_bg = FancyBboxPatch((0, 0), 1, 1,
                                  boxstyle="round,pad=0.02,rounding_size=0.05",
                                  facecolor='white', edgecolor='#e0e0e0',
                                  linewidth=2, transform=ax.transAxes,
                                  zorder=0)
        ax.add_patch(card_bg)

        if iku in all_stats:
            stats = all_stats[iku]
            pembilang = stats['pembilang']
            penyebut = stats['penyebut']
            target = targets.get(iku, 50)

            if iku in NUMBER_BASED:
                if iku == '5':
                    actual_pct = (pembilang / target) * 100
                    value_display = f'{int(pembilang)}'
                    fraction_text = f'Target: {target}'
                else:
                    actual_pct = (pembilang / target) * 100
                    value_display = f'{pembilang:.2f}'
                    fraction_text = f'Target: {target}/prodi'
            else:
                actual_pct = stats['persentase']
                value_display = f'{actual_pct:.1f}%'
                fraction_text = f'{pembilang}/{penyebut}'

            # Determine status
            diff = actual_pct - target if iku not in NUMBER_BASED else actual_pct - 100
            if actual_pct >= (100 if iku in NUMBER_BASED else target):
                status_color = '#2E7D32'
                status_text = 'ACHIEVED'
                arrow = '▲'
            elif actual_pct >= (80 if iku in NUMBER_BASED else target * 0.8):
                status_color = '#F9A825'
                status_text = 'ON TRACK'
                arrow = '▶'
            else:
                status_color = '#C62828'
                status_text = 'GAP'
                arrow = '▼'

            # IKU number badge (top-left)
            ax.text(0.08, 0.92, f'IKU {iku}', transform=ax.transAxes,
                   fontsize=11, fontweight='bold', color='white',
                   ha='left', va='top',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='#424242',
                            edgecolor='none'))

            # Main value (large, centered)
            ax.text(0.5, 0.58, value_display, transform=ax.transAxes,
                   fontsize=36, fontweight='bold', color=status_color,
                   ha='center', va='center')

            # Fraction/target text below main value
            ax.text(0.5, 0.38, fraction_text, transform=ax.transAxes,
                   fontsize=12, color='#666666',
                   ha='center', va='center')

            # Progress bar background
            bar_y = 0.22
            bar_height = 0.06
            bar_width = 0.84
            bar_x = 0.08

            # Background bar
            bg_bar = FancyBboxPatch((bar_x, bar_y), bar_width, bar_height,
                                    boxstyle="round,pad=0.01,rounding_size=0.02",
                                    facecolor='#e0e0e0', edgecolor='none',
                                    transform=ax.transAxes, zorder=1)
            ax.add_patch(bg_bar)

            # Progress bar (filled portion)
            fill_pct = min(actual_pct / (100 if iku in NUMBER_BASED else target), 1.5)
            fill_width = bar_width * min(fill_pct, 1.0)
            fill_bar = FancyBboxPatch((bar_x, bar_y), fill_width, bar_height,
                                      boxstyle="round,pad=0.01,rounding_size=0.02",
                                      facecolor=status_color, edgecolor='none',
                                      transform=ax.transAxes, zorder=2)
            ax.add_patch(fill_bar)

            # Target marker on progress bar
            if iku not in NUMBER_BASED:
                target_x = bar_x + bar_width * (target / 100)
                ax.plot([target_x, target_x], [bar_y - 0.02, bar_y + bar_height + 0.02],
                       color='#1a1a1a', linewidth=2, transform=ax.transAxes, zorder=3)

            # Status badge with arrow (bottom)
            diff_text = f'+{abs(diff):.1f}%' if diff >= 0 else f'-{abs(diff):.1f}%'
            ax.text(0.5, 0.08, f'{arrow} {status_text} {diff_text}',
                   transform=ax.transAxes,
                   fontsize=11, fontweight='bold', color=status_color,
                   ha='center', va='center')

            # IKU label (top, below badge)
            ax.text(0.5, 0.78, iku_labels[iku], transform=ax.transAxes,
                   fontsize=10, color='#424242', fontweight='600',
                   ha='center', va='center', linespacing=1.2)

        else:
            # No data
            ax.text(0.5, 0.5, f'IKU {iku}\nNo Data',
                   transform=ax.transAxes,
                   fontsize=14, color='#999999',
                   ha='center', va='center', fontweight='bold')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    # Main title
    fig.suptitle('CAPAIAN IKU FAKULTAS SAINS & TEKNOLOGI',
                fontsize=20, fontweight='bold', y=0.96, color='#1a1a1a')

    fig.text(0.5, 0.92, 'Universitas Jambi 2025',
            ha='center', fontsize=14, color='#666666', style='italic')

    # Legend at bottom
    fig.text(0.5, 0.03,
            '▲ Achieved (Green)    ▶ On Track (Yellow)    ▼ Gap (Red)    |    Progress bar shows achievement vs target',
            ha='center', fontsize=11, color='#666666')

    saved_files = save_figure(fig, 'IKU_overall_achievement_cards')
    plt.close()

    return saved_files


def create_overall_achievement_bullet_4x2(all_stats):
    """
    Membuat dashboard bullet chart dalam format 4x2 grid (compact)
    Based on Stephen Few's bullet chart design

    Parameters:
    -----------
    all_stats : dict
        Dictionary berisi statistik semua IKU {iku_number: stats_dict}

    Returns:
    --------
    list : List of saved file paths
    """
    main_ikus = ['1', '2', '3', '4', '5', '6', '7', '8']

    iku_labels = {
        '1': 'Lulusan Bekerja/Studi',
        '2': 'Mahasiswa Prestasi',
        '3': 'Dosen Tridharma',
        '4': 'Dosen DUDI/Praktisi',
        '5': 'Luaran Rekognisi',
        '6': 'Kerjasama/Prodi',
        '7': 'MK PJBL/Case',
        '8': 'Akreditasi Intl'
    }

    targets = {
        '1': 60, '2': 30, '3': 25, '4': 20.14,
        '5': 100, '6': 100, '7': 50, '8': 10
    }

    NUMBER_BASED = ['5', '6']

    # Create 4x2 grid
    fig, axes = plt.subplots(2, 4, figsize=(18, 8))
    axes = axes.flatten()

    for idx, iku in enumerate(main_ikus):
        ax = axes[idx]
        target = targets.get(iku, 50)

        if iku in all_stats:
            stats = all_stats[iku]
            pembilang = stats['pembilang']
            penyebut = stats['penyebut']

            if iku in NUMBER_BASED:
                if iku == '5':
                    actual_pct = (pembilang / 5) * 100
                    value_text = f'{int(pembilang)}'
                else:
                    actual_pct = (pembilang / 2) * 100
                    value_text = f'{pembilang:.1f}'
            else:
                actual_pct = stats['persentase']
                value_text = f'{actual_pct:.1f}%'

            # Status color
            if actual_pct >= target:
                bar_color = '#2E7D32'
                status = 'ACHIEVED'
            elif actual_pct >= target * 0.8:
                bar_color = '#F9A825'
                status = 'ON TRACK'
            else:
                bar_color = '#C62828'
                status = 'GAP'

            # Qualitative ranges (background)
            max_val = max(120, actual_pct + 10)
            range_colors = ['#f5f5f5', '#e0e0e0', '#bdbdbd']

            for i, pct in enumerate([0.4, 0.7, 1.0]):
                ax.barh(0, max_val * pct, height=0.7, color=range_colors[i],
                       edgecolor='none', zorder=1)

            # Actual value bar
            ax.barh(0, min(actual_pct, max_val), height=0.35, color=bar_color,
                   edgecolor='#1a1a1a', linewidth=0.5, zorder=3)

            # Target marker
            ax.plot([target, target], [-0.4, 0.4], color='#1a1a1a',
                   linewidth=3, zorder=4)

            # IKU badge
            ax.text(0.02, 0.95, f'IKU {iku}', transform=ax.transAxes,
                   fontsize=10, fontweight='bold', color='white',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='#424242',
                            edgecolor='none'), va='top')

            # Value and status at right
            ax.text(max_val + 2, 0, f'{value_text}', va='center', ha='left',
                   fontsize=14, fontweight='bold', color=bar_color)

            # Title below
            ax.set_title(iku_labels[iku], fontsize=11, fontweight='600',
                        pad=5, color='#333333')

            # Status badge at bottom
            ax.text(0.5, -0.25, status, transform=ax.transAxes,
                   ha='center', va='top', fontsize=9, fontweight='bold',
                   color='white',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=bar_color,
                            edgecolor='none', alpha=0.9))

            ax.set_xlim(0, max_val + 25)
            ax.set_ylim(-0.6, 0.6)

        else:
            ax.text(0.5, 0.5, f'IKU {iku}\nNo Data', transform=ax.transAxes,
                   ha='center', va='center', fontsize=12, color='#999999')

        ax.set_yticks([])
        ax.set_xticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

    # Title
    fig.suptitle('CAPAIAN IKU FAKULTAS SAINS & TEKNOLOGI',
                fontsize=18, fontweight='bold', y=0.98, color='#1a1a1a')
    fig.text(0.5, 0.93, 'Universitas Jambi 2025 | Bullet Chart Style',
            ha='center', fontsize=12, color='#666666', style='italic')

    # Legend
    fig.text(0.5, 0.02,
            '█ Achieved   █ On Track   █ Gap   |   ▌Target Line   |   Background: Poor → Satisfactory → Good',
            ha='center', fontsize=10, color='#666666')

    plt.tight_layout(rect=[0.02, 0.05, 0.98, 0.91])

    saved_files = save_figure(fig, 'IKU_overall_achievement_bullet_4x2')
    plt.close()

    return saved_files


def create_overall_achievement_thermometer(all_stats):
    """
    Membuat dashboard thermometer chart dalam format 4x2 grid
    Thermometer style showing fill level against target

    Parameters:
    -----------
    all_stats : dict
        Dictionary berisi statistik semua IKU {iku_number: stats_dict}

    Returns:
    --------
    list : List of saved file paths
    """
    main_ikus = ['1', '2', '3', '4', '5', '6', '7', '8']

    iku_labels = {
        '1': 'Lulusan\nBekerja/Studi',
        '2': 'Mahasiswa\nPrestasi',
        '3': 'Dosen\nTridharma',
        '4': 'Dosen\nDUDI/Praktisi',
        '5': 'Luaran\nRekognisi',
        '6': 'Kerjasama\nper Prodi',
        '7': 'MK PJBL/\nCase Method',
        '8': 'Akreditasi\nInternasional'
    }

    targets = {
        '1': 60, '2': 30, '3': 25, '4': 20.14,
        '5': 100, '6': 100, '7': 50, '8': 10
    }

    NUMBER_BASED = ['5', '6']

    # Create 4x2 grid
    fig, axes = plt.subplots(2, 4, figsize=(18, 12))
    axes = axes.flatten()

    for idx, iku in enumerate(main_ikus):
        ax = axes[idx]
        target = targets.get(iku, 50)

        if iku in all_stats:
            stats = all_stats[iku]
            pembilang = stats['pembilang']
            penyebut = stats['penyebut']

            if iku in NUMBER_BASED:
                if iku == '5':
                    actual_pct = (pembilang / 5) * 100
                    value_text = f'{int(pembilang)}'
                    sub_text = 'Target: 5'
                else:
                    actual_pct = (pembilang / 2) * 100
                    value_text = f'{pembilang:.2f}'
                    sub_text = 'Target: 2/prodi'
            else:
                actual_pct = stats['persentase']
                value_text = f'{actual_pct:.1f}%'
                sub_text = f'{pembilang}/{penyebut}'

            # Status color
            if actual_pct >= target:
                fill_color = '#2E7D32'
                status = 'ACHIEVED'
            elif actual_pct >= target * 0.8:
                fill_color = '#F9A825'
                status = 'ON TRACK'
            else:
                fill_color = '#C62828'
                status = 'GAP'

            # Draw thermometer outline
            thermo_width = 0.4
            thermo_height = 0.65
            bulb_radius = 0.12
            thermo_x = 0.3
            thermo_bottom = 0.2

            # Background tube
            tube_bg = FancyBboxPatch(
                (thermo_x, thermo_bottom), thermo_width, thermo_height,
                boxstyle="round,pad=0.02,rounding_size=0.05",
                facecolor='#e8e8e8', edgecolor='#999999', linewidth=2,
                transform=ax.transAxes, zorder=1
            )
            ax.add_patch(tube_bg)

            # Fill level (capped at 100% of tube height for display)
            fill_height = min(actual_pct / 100, 1.2) * thermo_height * 0.9
            if fill_height > 0:
                tube_fill = FancyBboxPatch(
                    (thermo_x + 0.02, thermo_bottom + 0.02),
                    thermo_width - 0.04, fill_height,
                    boxstyle="round,pad=0.01,rounding_size=0.03",
                    facecolor=fill_color, edgecolor='none',
                    transform=ax.transAxes, zorder=2
                )
                ax.add_patch(tube_fill)

            # Bulb at bottom
            bulb = plt.Circle((thermo_x + thermo_width/2, thermo_bottom - 0.02),
                             bulb_radius, facecolor=fill_color, edgecolor='#999999',
                             linewidth=2, transform=ax.transAxes, zorder=3)
            ax.add_patch(bulb)

            # Target line marker
            target_y = thermo_bottom + (target / 100) * thermo_height * 0.9
            ax.plot([thermo_x - 0.05, thermo_x + thermo_width + 0.05],
                   [target_y, target_y], color='#1a1a1a', linewidth=2,
                   linestyle='--', transform=ax.transAxes, zorder=4)
            ax.text(thermo_x + thermo_width + 0.08, target_y, f'Target\n{target}%',
                   transform=ax.transAxes, fontsize=8, va='center', ha='left',
                   color='#666666')

            # IKU badge
            ax.text(0.5, 0.98, f'IKU {iku}', transform=ax.transAxes,
                   fontsize=12, fontweight='bold', color='white', ha='center',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='#424242',
                            edgecolor='none'), va='top')

            # Main value (right side)
            ax.text(0.85, 0.55, value_text, transform=ax.transAxes,
                   fontsize=24, fontweight='bold', color=fill_color,
                   ha='center', va='center')

            ax.text(0.85, 0.45, sub_text, transform=ax.transAxes,
                   fontsize=10, color='#666666', ha='center', va='center')

            # Status badge
            ax.text(0.5, 0.05, status, transform=ax.transAxes,
                   fontsize=11, fontweight='bold', color='white', ha='center',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor=fill_color,
                            edgecolor='none', alpha=0.95))

            # Label
            ax.text(0.15, 0.55, iku_labels[iku], transform=ax.transAxes,
                   fontsize=10, fontweight='600', color='#333333',
                   ha='center', va='center', linespacing=1.3)

        else:
            ax.text(0.5, 0.5, f'IKU {iku}\nNo Data', transform=ax.transAxes,
                   ha='center', va='center', fontsize=12, color='#999999')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    # Title
    fig.suptitle('CAPAIAN IKU FAKULTAS SAINS & TEKNOLOGI',
                fontsize=18, fontweight='bold', y=0.98, color='#1a1a1a')
    fig.text(0.5, 0.94, 'Universitas Jambi 2025 | Thermometer Style',
            ha='center', fontsize=12, color='#666666', style='italic')

    # Legend
    fig.text(0.5, 0.01,
            '🌡️ Fill level shows achievement   |   -- Target line   |   Green = Achieved   Yellow = On Track   Red = Gap',
            ha='center', fontsize=10, color='#666666')

    plt.tight_layout(rect=[0.01, 0.03, 0.99, 0.92])

    saved_files = save_figure(fig, 'IKU_overall_achievement_thermometer')
    plt.close()

    return saved_files


def create_overall_achievement_waffle(all_stats):
    """
    Membuat dashboard waffle chart dalam format 4x2 grid
    Each IKU shows a 10x10 grid representing percentage achievement

    Parameters:
    -----------
    all_stats : dict
        Dictionary berisi statistik semua IKU {iku_number: stats_dict}

    Returns:
    --------
    list : List of saved file paths
    """
    main_ikus = ['1', '2', '3', '4', '5', '6', '7', '8']

    iku_labels = {
        '1': 'Lulusan Bekerja/Studi',
        '2': 'Mahasiswa Prestasi',
        '3': 'Dosen Tridharma',
        '4': 'Dosen DUDI/Praktisi',
        '5': 'Luaran Rekognisi',
        '6': 'Kerjasama/Prodi',
        '7': 'MK PJBL/Case',
        '8': 'Akreditasi Intl'
    }

    targets = {
        '1': 60, '2': 30, '3': 25, '4': 20.14,
        '5': 100, '6': 100, '7': 50, '8': 10
    }

    NUMBER_BASED = ['5', '6']

    # Create 4x2 grid
    fig, axes = plt.subplots(2, 4, figsize=(18, 10))
    axes = axes.flatten()

    for idx, iku in enumerate(main_ikus):
        ax = axes[idx]
        target = targets.get(iku, 50)

        if iku in all_stats:
            stats = all_stats[iku]
            pembilang = stats['pembilang']
            penyebut = stats['penyebut']

            if iku in NUMBER_BASED:
                if iku == '5':
                    actual_pct = min((pembilang / 5) * 100, 100)
                    value_text = f'{int(pembilang)}'
                    sub_text = 'Target: 5'
                else:
                    actual_pct = min((pembilang / 2) * 100, 100)
                    value_text = f'{pembilang:.2f}'
                    sub_text = 'Target: 2'
            else:
                actual_pct = min(stats['persentase'], 100)
                value_text = f'{stats["persentase"]:.1f}%'
                sub_text = f'{pembilang}/{penyebut}'

            # Status color
            raw_pct = stats['persentase'] if iku not in NUMBER_BASED else (pembilang / (5 if iku == '5' else 2)) * 100
            if raw_pct >= target:
                fill_color = '#2E7D32'
                status = 'ACHIEVED'
            elif raw_pct >= target * 0.8:
                fill_color = '#F9A825'
                status = 'ON TRACK'
            else:
                fill_color = '#C62828'
                status = 'GAP'

            # Draw 10x10 waffle grid
            grid_size = 10
            cell_size = 0.08
            start_x = 0.1
            start_y = 0.25

            filled_cells = int(actual_pct)  # Number of cells to fill (out of 100)

            for row in range(grid_size):
                for col in range(grid_size):
                    cell_idx = row * grid_size + col
                    x = start_x + col * cell_size
                    y = start_y + (grid_size - 1 - row) * cell_size  # Bottom to top

                    if cell_idx < filled_cells:
                        color = fill_color
                    else:
                        color = '#e0e0e0'

                    rect = plt.Rectangle((x, y), cell_size * 0.9, cell_size * 0.9,
                                         facecolor=color, edgecolor='white',
                                         linewidth=0.5, transform=ax.transAxes)
                    ax.add_patch(rect)

            # IKU badge
            ax.text(0.5, 0.98, f'IKU {iku}', transform=ax.transAxes,
                   fontsize=11, fontweight='bold', color='white', ha='center',
                   bbox=dict(boxstyle='round,pad=0.35', facecolor='#424242',
                            edgecolor='none'), va='top')

            # Title
            ax.text(0.5, 0.88, iku_labels[iku], transform=ax.transAxes,
                   fontsize=10, fontweight='600', color='#333333',
                   ha='center', va='center')

            # Value (right side of waffle)
            ax.text(0.95, 0.55, value_text, transform=ax.transAxes,
                   fontsize=20, fontweight='bold', color=fill_color,
                   ha='right', va='center')

            ax.text(0.95, 0.45, sub_text, transform=ax.transAxes,
                   fontsize=9, color='#666666', ha='right', va='center')

            # Status badge at bottom
            ax.text(0.5, 0.08, status, transform=ax.transAxes,
                   fontsize=10, fontweight='bold', color='white', ha='center',
                   bbox=dict(boxstyle='round,pad=0.35', facecolor=fill_color,
                            edgecolor='none', alpha=0.95))

            # Target indicator text
            ax.text(0.5, 0.17, f'Target: {target}%', transform=ax.transAxes,
                   fontsize=8, color='#888888', ha='center', va='center')

        else:
            ax.text(0.5, 0.5, f'IKU {iku}\nNo Data', transform=ax.transAxes,
                   ha='center', va='center', fontsize=12, color='#999999')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    # Title
    fig.suptitle('CAPAIAN IKU FAKULTAS SAINS & TEKNOLOGI',
                fontsize=18, fontweight='bold', y=0.98, color='#1a1a1a')
    fig.text(0.5, 0.94, 'Universitas Jambi 2025 | Waffle Chart Style',
            ha='center', fontsize=12, color='#666666', style='italic')

    # Legend
    fig.text(0.5, 0.01,
            '■ Each square = 1%   |   Filled squares show achievement   |   Green = Achieved   Yellow = On Track   Red = Gap',
            ha='center', fontsize=10, color='#666666')

    plt.tight_layout(rect=[0.01, 0.03, 0.99, 0.92])

    saved_files = save_figure(fig, 'IKU_overall_achievement_waffle')
    plt.close()

    return saved_files
