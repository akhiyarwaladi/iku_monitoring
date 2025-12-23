"""
============================================================================
IKU 33 BREAKDOWN: Bimbingan Mahasiswa Luar Prodi
============================================================================
Visualisasi breakdown untuk IKU 33 (Charts Terpisah):
1. Top Program Mahasiswa
2. Top 10 Dosen Pembimbing
3. Statistik Summary
============================================================================
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import matplotlib.pyplot as plt
import textwrap
from visualization_config import *

def create_iku_33_top_programs(df_pembilang):
    """Chart 1: Top Program Mahasiswa"""

    # Data processing
    top_programs = df_pembilang['Nama Program'].value_counts().head(10)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))

    colors_map = ['#70AD47', '#5B9BD5', '#ED7D31', '#9966CC',
                  '#E85D75', '#FFC000', '#A8D08D', '#F4B183',
                  '#C5A8E0', '#BDC3C7']

    y_pos = range(len(top_programs))
    bars = ax.barh(y_pos, top_programs.values,
                   color=colors_map[:len(top_programs)],
                   edgecolor='black', linewidth=1.2,
                   alpha=0.85, height=0.7)

    # Labels
    for bar, jumlah in zip(bars, top_programs.values):
        width = bar.get_width()
        ax.text(width + 0.8, bar.get_y() + bar.get_height()/2,
                f'{int(jumlah)}',
                ha='left', va='center', fontsize=10, fontweight='bold')

    # Styling
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_programs.index, fontsize=9.5, fontweight='500')
    ax.set_xlabel('Jumlah Mahasiswa', fontsize=11, fontweight='bold')
    ax.set_title('IKU 33: Top 10 Program Bimbingan Mahasiswa\nLuar Program Studi',
                 fontsize=12, fontweight='bold', pad=20)
    ax.grid(axis='x', linestyle=':', alpha=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)
    ax.invert_yaxis()

    plt.tight_layout()

    # Save
    saved_files = save_figure(fig, 'IKU_33_breakdown_top_programs')
    plt.close()

    return saved_files

# REMOVED: create_iku_33_distribusi_prodi() - duplikasi dengan main chart

def create_iku_33_statistik(df_pembilang, df_penyebut):
    """Chart 3: Statistik Summary - Consistent Style"""

    # Data processing dengan verifikasi
    total_mahasiswa = len(df_pembilang)
    total_dosen = df_pembilang['NIP'].nunique()
    total_dosen_fst = len(df_penyebut)
    persentase_dosen = (total_dosen / total_dosen_fst * 100) if total_dosen_fst > 0 else 0
    rata_rata_per_dosen = total_mahasiswa / total_dosen if total_dosen > 0 else 0

    # Nama Program (kategori umum: Magang Dudi, Studi Independen, dll)
    nama_program = df_pembilang['Nama Program'].value_counts()

    # Top 10 Paket Program (nama spesifik program)
    top_paket = df_pembilang['Paket Program'].value_counts().head(10)

    # Create figure - extra height untuk multi-line labels
    fig_height = max(10, max(len(nama_program), len(top_paket)) * 0.7)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17, fig_height))

    # Suptitle dengan info summary
    fig.suptitle(f'IKU 33: Statistik Summary - Bimbingan Mahasiswa Luar Program Studi\n' +
                 f'Total: {total_mahasiswa} mahasiswa | {total_dosen}/{total_dosen_fst} dosen aktif ({persentase_dosen:.1f}%) | Rata-rata: {rata_rata_per_dosen:.1f} per dosen',
                 fontsize=12, fontweight='bold', y=0.98)

    # ===== CHART 1: Nama Program / Kategori (Left) =====
    y_pos = np.arange(len(nama_program))
    colors_program = ['#70AD47', '#5B9BD5', '#ED7D31', '#9966CC', '#E85D75']

    bars1 = ax1.barh(y_pos, nama_program.values,
                     color=colors_program[:len(nama_program)],
                     edgecolor='black', linewidth=1.2, alpha=0.85, height=0.75)

    # Labels pada bars
    for bar, count in zip(bars1, nama_program.values):
        width = bar.get_width()
        ax1.text(width + 0.8, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=9, fontweight='bold')

    # Styling ax1
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(nama_program.index, fontsize=9, fontweight='500')
    ax1.set_xlabel('Jumlah Mahasiswa', fontsize=11, fontweight='bold')
    ax1.set_title('Kategori Program Bimbingan', fontsize=11, fontweight='bold', pad=15)
    ax1.xaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0)
    ax1.set_axisbelow(True)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_linewidth(1.2)
    ax1.spines['bottom'].set_linewidth(1.2)
    ax1.invert_yaxis()

    # ===== CHART 2: Top 10 Paket Program (Right) =====
    y_pos2 = np.arange(len(top_paket))
    colors_paket = ['#70AD47', '#5B9BD5', '#ED7D31', '#9966CC',
                    '#E85D75', '#FFC000', '#A8D08D', '#F4B183',
                    '#C5A8E0', '#BDC3C7']

    bars2 = ax2.barh(y_pos2, top_paket.values,
                     color=colors_paket[:len(top_paket)],
                     edgecolor='black', linewidth=1.2, alpha=0.85, height=0.75)

    # Labels pada bars
    for bar, count in zip(bars2, top_paket.values):
        width = bar.get_width()
        ax2.text(width + 0.15, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=9, fontweight='bold')

    # Styling ax2 dengan word wrapping untuk nama paket yang panjang
    ax2.set_yticks(y_pos2)
    # Wrap text ke max 45 karakter per line
    paket_labels = ['\n'.join(textwrap.wrap(name, width=45)) for name in top_paket.index]
    ax2.set_yticklabels(paket_labels, fontsize=7.5, fontweight='500')
    ax2.set_xlabel('Jumlah Mahasiswa', fontsize=11, fontweight='bold')
    ax2.set_title('Top 10 Paket Program Spesifik', fontsize=11, fontweight='bold', pad=15)
    ax2.xaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0)
    ax2.set_axisbelow(True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_linewidth(1.2)
    ax2.spines['bottom'].set_linewidth(1.2)
    ax2.invert_yaxis()

    # Adjust layout dengan lebih banyak ruang untuk multi-line labels
    plt.tight_layout(rect=[0.08, 0, 1, 0.95])

    # Save
    saved_files = save_figure(fig, 'IKU_33_breakdown_statistik')
    plt.close()

    return saved_files

def create_iku_33_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 33 (charts terpisah)"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 33...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('33', 'pembilang')
    df_penyebut = read_excel_iku('33', 'penyebut')

    # Generate semua charts terpisah (tanpa duplikasi)
    all_files = []

    print("    → Statistik Summary (Kategori Program & Detail Paket)...")
    all_files.extend(create_iku_33_statistik(df_pembilang, df_penyebut))

    print(f"  ✅ Breakdown IKU 33 selesai (1 chart)")
    return all_files

if __name__ == "__main__":
    create_iku_33_breakdown()
