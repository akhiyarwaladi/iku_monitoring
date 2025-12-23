"""
============================================================================
IKU 31 BREAKDOWN: Tridharma di PT Lain
============================================================================
Visualisasi breakdown untuk IKU 31 (Charts Terpisah):
1. Top 15 Dosen Paling Aktif
2. Pie Chart: Penelitian vs Pengabdian
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

# REMOVED: create_iku_31_distribusi_prodi() - duplikasi dengan main chart
# REMOVED: create_iku_31_jenis_kegiatan() - sudah ada di chart statistik

def create_iku_31_statistik(df_pembilang, df_penyebut):
    """Chart 3: Statistik Summary - Consistent Style"""

    # Data processing dengan verifikasi
    # Total kegiatan = jumlah baris (setiap baris = 1 kegiatan)
    total_kegiatan = len(df_pembilang)

    # Dosen aktif = unique NIP yang punya kegiatan
    total_dosen_aktif = df_pembilang['NIP'].nunique()

    # Total dosen FST
    total_dosen_fst = len(df_penyebut)

    # Persentase dosen yang aktif
    persentase_dosen_aktif = (total_dosen_aktif / total_dosen_fst * 100) if total_dosen_fst > 0 else 0

    # Rata-rata kegiatan per dosen aktif
    rata_rata_per_aktif = total_kegiatan / total_dosen_aktif if total_dosen_aktif > 0 else 0

    # Top 10 Kegiatan (nama kegiatan spesifik)
    top_kegiatan = df_pembilang['Kegiatan'].value_counts().head(10)

    # Breakdown jenis kegiatan
    jenis_breakdown = df_pembilang['Jenis'].value_counts()

    # Create figure - extra height untuk multi-line labels
    # TOP kegiatan butuh lebih banyak ruang karena text panjang
    fig_height = max(10, len(top_kegiatan) * 0.7)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, fig_height))

    # Suptitle dengan info summary
    fig.suptitle(f'IKU 31: Statistik Summary - Kegiatan Tridharma di PT Lain\n' +
                 f'Total: {total_kegiatan} kegiatan | {total_dosen_aktif}/{total_dosen_fst} dosen aktif ({persentase_dosen_aktif:.1f}%) | Rata-rata: {rata_rata_per_aktif:.1f} per dosen',
                 fontsize=12, fontweight='bold', y=0.98)

    # ===== CHART 1: Top 10 Kegiatan (Left) =====
    y_pos = np.arange(len(top_kegiatan))
    colors_kegiatan = ['#3498DB', '#E74C3C', '#F39C12', '#1ABC9C', '#9B59B6',
                       '#E85D75', '#70AD47', '#5B9BD5', '#ED7D31', '#9966CC']

    bars1 = ax1.barh(y_pos, top_kegiatan.values,
                     color=colors_kegiatan[:len(top_kegiatan)],
                     edgecolor='black', linewidth=1.2, alpha=0.85, height=0.75)

    # Labels pada bars
    for bar, count in zip(bars1, top_kegiatan.values):
        width = bar.get_width()
        ax1.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=9, fontweight='bold')

    # Styling ax1 dengan word wrapping untuk labels panjang
    ax1.set_yticks(y_pos)
    # Wrap text ke max 35 karakter per line agar tidak terpotong
    kegiatan_labels = ['\n'.join(textwrap.wrap(name, width=35)) for name in top_kegiatan.index]
    ax1.set_yticklabels(kegiatan_labels, fontsize=8, fontweight='500')
    ax1.set_xlabel('Frekuensi', fontsize=11, fontweight='bold')
    ax1.set_title('Top 10 Kegiatan Tridharma', fontsize=11, fontweight='bold', pad=15)
    ax1.xaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0)
    ax1.set_axisbelow(True)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_linewidth(1.2)
    ax1.spines['bottom'].set_linewidth(1.2)
    ax1.invert_yaxis()

    # ===== CHART 2: Jenis Kegiatan (Right) =====
    y_pos2 = np.arange(len(jenis_breakdown))
    colors_jenis = ['#70AD47', '#ED7D31', '#F39C12']

    bars2 = ax2.barh(y_pos2, jenis_breakdown.values,
                     color=colors_jenis[:len(jenis_breakdown)],
                     edgecolor='black', linewidth=1.2, alpha=0.85, height=0.75)

    # Labels pada bars
    for bar, count in zip(bars2, jenis_breakdown.values):
        width = bar.get_width()
        ax2.text(width + 1, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=9, fontweight='bold')

    # Styling ax2
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(jenis_breakdown.index, fontsize=10, fontweight='500')
    ax2.set_xlabel('Jumlah Kegiatan', fontsize=11, fontweight='bold')
    ax2.set_title('Breakdown Jenis Kegiatan', fontsize=11, fontweight='bold', pad=15)
    ax2.xaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0)
    ax2.set_axisbelow(True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_linewidth(1.2)
    ax2.spines['bottom'].set_linewidth(1.2)
    ax2.invert_yaxis()

    # Adjust layout dengan lebih banyak ruang kiri untuk long labels
    plt.tight_layout(rect=[0.15, 0, 1, 0.95])

    # Save
    saved_files = save_figure(fig, 'IKU_31_breakdown_statistik')
    plt.close()

    return saved_files

def create_iku_31_dosen_showcase(df_pembilang, df_penyebut):
    """Chart 3: Showcase Dosen Aktif - Visual Card Style"""

    # Merge untuk mendapatkan jurusan
    df_merged = df_pembilang.merge(df_penyebut[['NIP', 'Jurusan']], on='NIP', how='left')

    # Get unique dosen (ambil 24 dosen pertama untuk display)
    dosen_list = df_merged[['NIP', 'Nama', 'Jurusan']].drop_duplicates('NIP').head(24)
    dosen_list = dosen_list.sort_values('Jurusan')

    # Create figure dengan style modern
    fig = plt.figure(figsize=(14, 10), facecolor='white')

    # Title
    fig.text(0.5, 0.96, 'IKU 31: Dosen Aktif Tridharma di PT Lain',
             ha='center', fontsize=14, fontweight='bold', color='#2C3E50')
    fig.text(0.5, 0.93, f'Featured {len(dosen_list)} dari {df_pembilang["NIP"].nunique()} Dosen Aktif',
             ha='center', fontsize=10, color='#7F8C8D', style='italic')

    # Group by jurusan
    jurusan_groups = dosen_list.groupby('Jurusan')

    # Layout parameters
    y_start = 0.88
    y_spacing = 0.35
    card_height = 0.06
    card_width = 0.22
    cards_per_row = 4

    for jurusan_name, group in jurusan_groups:
        # Jurusan header
        color = JURUSAN_COLORS.get(jurusan_name, {}).get('base', '#5B9BD5')

        fig.text(0.08, y_start, f'● {jurusan_name}',
                fontsize=11, fontweight='bold', color=color)
        fig.text(0.92, y_start, f'({len(group)} dosen)',
                ha='right', fontsize=9, color='#7F8C8D')

        y_start -= 0.05

        # Draw cards for each dosen
        for idx, (_, dosen) in enumerate(group.iterrows()):
            row = idx // cards_per_row
            col = idx % cards_per_row

            x = 0.08 + col * (card_width + 0.01)
            y = y_start - row * (card_height + 0.01)

            # Card background
            from matplotlib.patches import FancyBboxPatch
            card = FancyBboxPatch((x, y - card_height), card_width, card_height,
                                   boxstyle="round,pad=0.005",
                                   facecolor=color, alpha=0.15,
                                   edgecolor=color, linewidth=1.5,
                                   transform=fig.transFigure)
            fig.add_artist(card)

            # Dosen name (truncate if too long)
            name = dosen['Nama']
            if len(name) > 28:
                name = name[:25] + '...'

            fig.text(x + card_width/2, y - card_height/2, name,
                    ha='center', va='center', fontsize=7.5,
                    color='#2C3E50', transform=fig.transFigure)

        # Update y_start for next jurusan
        rows_used = (len(group) - 1) // cards_per_row + 1
        y_start -= (rows_used * (card_height + 0.01) + 0.08)

        if y_start < 0.1:  # Stop if running out of space
            break

    # Footer note
    if df_pembilang['NIP'].nunique() > len(dosen_list):
        fig.text(0.5, 0.02, f'* Menampilkan {len(dosen_list)} dari {df_pembilang["NIP"].nunique()} dosen aktif',
                ha='center', fontsize=8, style='italic', color='#95A5A6')

    # Save
    saved_files = save_figure(fig, 'IKU_31_breakdown_dosen_showcase')
    plt.close()

    return saved_files

def create_iku_31_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 31 (charts terpisah)"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 31...")

    # Setup style
    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('31', 'pembilang')
    df_penyebut = read_excel_iku('31', 'penyebut')

    # Generate semua charts terpisah (tanpa duplikasi)
    all_files = []

    print("    → Dosen Showcase (Featured Contributors)...")
    all_files.extend(create_iku_31_dosen_showcase(df_pembilang, df_penyebut))

    print("    → Statistik Summary (Top Kegiatan & Jenis)...")
    all_files.extend(create_iku_31_statistik(df_pembilang, df_penyebut))

    print(f"  ✅ Breakdown IKU 31 selesai (2 charts)")
    return all_files

if __name__ == "__main__":
    create_iku_31_breakdown()
