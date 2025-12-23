"""
============================================================================
IKU 41 BREAKDOWN: Sertifikat DUDI
============================================================================
Visualisasi breakdown untuk IKU 41 (Charts Terpisah):
1. Top Lembaga Sertifikasi
2. Top Bidang Sertifikasi
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

def create_iku_41_top_lembaga(df_pembilang):
    """Chart 1: Top Lembaga Sertifikasi"""

    # Data processing
    top_lembaga = df_pembilang['Lembaga Sertifikasi'].value_counts().head(12)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 9))

    y_pos = range(len(top_lembaga))
    bars = ax.barh(y_pos, top_lembaga.values,
                   color='#70AD47', edgecolor='black',
                   linewidth=1.2, alpha=0.85, height=0.7)

    # Labels
    for bar, jumlah in zip(bars, top_lembaga.values):
        width = bar.get_width()
        ax.text(width + 0.2, bar.get_y() + bar.get_height()/2,
                f'{int(jumlah)}',
                ha='left', va='center', fontsize=9, fontweight='bold')

    # Styling
    ax.set_yticks(y_pos)
    labels = [label[:50] + '...' if len(label) > 50 else label for label in top_lembaga.index]
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel('Jumlah Sertifikat', fontsize=11, fontweight='bold')
    ax.set_title('IKU 41: Top 12 Lembaga Sertifikasi\nSertifikat Kompetensi DUDI',
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
    saved_files = save_figure(fig, 'IKU_41_breakdown_top_lembaga')
    plt.close()

    return saved_files

def create_iku_41_top_bidang(df_pembilang):
    """Chart 2: Top Bidang Sertifikasi"""

    # Data processing
    top_bidang = df_pembilang['Bidang Sertifikasi'].value_counts().head(12)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 9))

    y_pos = range(len(top_bidang))
    bars = ax.barh(y_pos, top_bidang.values,
                   color='#ED7D31', edgecolor='black',
                   linewidth=1.2, alpha=0.85, height=0.7)

    # Labels
    for bar, jumlah in zip(bars, top_bidang.values):
        width = bar.get_width()
        ax.text(width + 0.2, bar.get_y() + bar.get_height()/2,
                f'{int(jumlah)}',
                ha='left', va='center', fontsize=9, fontweight='bold')

    # Styling
    ax.set_yticks(y_pos)
    labels = [label[:55] + '...' if len(label) > 55 else label for label in top_bidang.index]
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel('Jumlah Sertifikat', fontsize=11, fontweight='bold')
    ax.set_title('IKU 41: Top 12 Bidang Sertifikasi\nSertifikat Kompetensi DUDI',
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
    saved_files = save_figure(fig, 'IKU_41_breakdown_top_bidang')
    plt.close()

    return saved_files

def create_iku_41_statistik(df_pembilang, df_penyebut):
    """Chart 3: Statistik Summary - Consistent Style"""

    # Data processing dengan verifikasi
    total_sertifikat = len(df_pembilang)
    total_dosen = df_pembilang['NIP'].nunique()
    total_dosen_fst = len(df_penyebut)
    persentase_dosen = (total_dosen / total_dosen_fst * 100) if total_dosen_fst > 0 else 0
    rata_rata_per_dosen = total_sertifikat / total_dosen if total_dosen > 0 else 0

    # Top 10 lembaga
    top_lembaga = df_pembilang['Lembaga Sertifikasi'].value_counts().head(10)

    # Top 10 bidang
    top_bidang = df_pembilang['Bidang Sertifikasi'].value_counts().head(10)

    # Create figure - extra height untuk multi-line labels
    fig_height = max(10, max(len(top_lembaga), len(top_bidang)) * 0.7)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17, fig_height))

    # Suptitle dengan info summary
    fig.suptitle(f'IKU 41: Statistik Summary - Sertifikat Kompetensi/Profesi DUDI\n' +
                 f'Total: {total_sertifikat} sertifikat | {total_dosen}/{total_dosen_fst} dosen bersertifikat ({persentase_dosen:.1f}%) | Rata-rata: {rata_rata_per_dosen:.1f} per dosen',
                 fontsize=12, fontweight='bold', y=0.98)

    # ===== CHART 1: Top 10 Lembaga (Left) =====
    y_pos = np.arange(len(top_lembaga))
    colors_lemb = ['#3498DB', '#E74C3C', '#F39C12', '#1ABC9C', '#9B59B6',
                   '#E85D75', '#70AD47', '#5B9BD5', '#ED7D31', '#9966CC']

    bars1 = ax1.barh(y_pos, top_lembaga.values,
                     color=colors_lemb[:len(top_lembaga)],
                     edgecolor='black', linewidth=1.2, alpha=0.85, height=0.75)

    # Labels pada bars
    for bar, count in zip(bars1, top_lembaga.values):
        width = bar.get_width()
        ax1.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=9, fontweight='bold')

    # Styling ax1 dengan word wrapping
    ax1.set_yticks(y_pos)
    # Wrap text ke max 35 karakter per line
    lemb_labels = ['\n'.join(textwrap.wrap(name, width=35)) for name in top_lembaga.index]
    ax1.set_yticklabels(lemb_labels, fontsize=8, fontweight='500')
    ax1.set_xlabel('Jumlah Sertifikat', fontsize=11, fontweight='bold')
    ax1.set_title('Top 10 Lembaga Sertifikasi', fontsize=11, fontweight='bold', pad=15)
    ax1.xaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0)
    ax1.set_axisbelow(True)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_linewidth(1.2)
    ax1.spines['bottom'].set_linewidth(1.2)
    ax1.invert_yaxis()

    # ===== CHART 2: Top 10 Bidang (Right) =====
    y_pos2 = np.arange(len(top_bidang))

    bars2 = ax2.barh(y_pos2, top_bidang.values,
                     color=colors_lemb[:len(top_bidang)],
                     edgecolor='black', linewidth=1.2, alpha=0.85, height=0.75)

    # Labels pada bars
    for bar, count in zip(bars2, top_bidang.values):
        width = bar.get_width()
        ax2.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=9, fontweight='bold')

    # Styling ax2 dengan word wrapping
    ax2.set_yticks(y_pos2)
    # Wrap text ke max 35 karakter per line
    bidang_labels = ['\n'.join(textwrap.wrap(name, width=35)) for name in top_bidang.index]
    ax2.set_yticklabels(bidang_labels, fontsize=8, fontweight='500')
    ax2.set_xlabel('Jumlah Sertifikat', fontsize=11, fontweight='bold')
    ax2.set_title('Top 10 Bidang Sertifikasi', fontsize=11, fontweight='bold', pad=15)
    ax2.xaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0)
    ax2.set_axisbelow(True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_linewidth(1.2)
    ax2.spines['bottom'].set_linewidth(1.2)
    ax2.invert_yaxis()

    # Adjust layout dengan lebih banyak ruang untuk multi-line labels
    plt.tight_layout(rect=[0.12, 0, 1, 0.95])

    # Save
    saved_files = save_figure(fig, 'IKU_41_breakdown_statistik')
    plt.close()

    return saved_files

# REMOVED: create_iku_41_distribusi_jurusan() - duplikasi dengan main chart

def create_iku_41_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 41 (charts terpisah)"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 41...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('41', 'pembilang')
    df_penyebut = read_excel_iku('41', 'penyebut')

    # Generate semua charts terpisah (tanpa duplikasi)
    all_files = []

    print("    → Statistik Summary (Top Lembaga & Top Bidang)...")
    all_files.extend(create_iku_41_statistik(df_pembilang, df_penyebut))

    print(f"  ✅ Breakdown IKU 41 selesai (1 chart)")
    return all_files

if __name__ == "__main__":
    create_iku_41_breakdown()
