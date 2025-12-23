"""
============================================================================
IKU 31 BREAKDOWN: Tridharma di PT Lain
============================================================================
Visualisasi breakdown untuk IKU 31 (Charts Terpisah):
1. Dosen Annotated - Bar chart dengan nama dosen per prodi
2. Statistik Summary - Top kegiatan dan jenis kegiatan
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

def create_iku_31_dosen_annotated(df_pembilang, df_penyebut):
    """Chart: Bar Chart dengan Nama Dosen Aktif per Prodi"""

    # Get unique dosen aktif (unique NIP)
    dosen_aktif = df_pembilang[['NIP', 'Nama']].drop_duplicates(subset='NIP')

    # Join dengan penyebut untuk dapat Program Studi dan Jurusan
    df_dosen = dosen_aktif.merge(
        df_penyebut[['NIP', 'Program Studi', 'Jurusan']],
        on='NIP',
        how='left'
    )

    # Group by Program Studi dan kumpulkan nama-nama dosen
    prodi_groups = df_dosen.groupby('Program Studi').agg({
        'Nama': list,
        'Jurusan': 'first'
    }).reset_index()

    # Hitung jumlah dosen per prodi
    prodi_groups['Count'] = prodi_groups['Nama'].apply(len)
    prodi_groups = prodi_groups.sort_values('Count', ascending=True)

    # Create figure dengan height yang cukup
    fig_height = max(10, len(prodi_groups) * 0.8)
    fig, ax = plt.subplots(figsize=(16, fig_height))

    y_pos = np.arange(len(prodi_groups))

    # Warna berdasarkan jurusan
    colors = []
    for jurusan in prodi_groups['Jurusan']:
        colors.append(JURUSAN_COLORS.get(jurusan, {}).get('base', '#5B9BD5'))

    # Buat bars
    bars = ax.barh(y_pos, prodi_groups['Count'].values,
                   color=colors, edgecolor='black',
                   linewidth=1.2, alpha=0.85, height=0.7)

    # Tambahkan nama-nama dosen di samping bar
    for idx, (bar, row) in enumerate(zip(bars, prodi_groups.itertuples())):
        count = row.Count
        nama_list = row.Nama

        # Format nama dosen
        if count <= 6:
            # Tampilkan semua nama untuk prodi dengan ≤6 dosen
            all_names = [n.split(',')[0].strip() for n in nama_list]
            nama_text = ', '.join(all_names)
        else:
            # Tampilkan 2 nama pertama + "dan X lainnya" untuk >6 dosen
            first_names = [n.split(',')[0].strip() for n in nama_list[:2]]
            nama_text = ', '.join(first_names) + f' dan {count-2} lainnya'

        # Wrap text dengan width lebih kecil agar nama banyak di-split ke bawah
        wrapped_text = '\n'.join(textwrap.wrap(nama_text, width=60))

        # Tampilkan text di samping bar
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                wrapped_text,
                ha='left', va='center', fontsize=12,
                color='#333333')

        # Tampilkan count di dalam bar
        ax.text(bar.get_width() - 0.3, bar.get_y() + bar.get_height()/2,
                f'{count}',
                ha='right', va='center', fontsize=10, fontweight='bold',
                color='white' if count > 5 else '#333333')

    # Styling
    ax.set_yticks(y_pos)
    prodi_labels = [p.replace('Program Studi ', '') for p in prodi_groups['Program Studi']]
    ax.set_yticklabels(prodi_labels, fontsize=14, fontweight='500')
    ax.set_xlabel('Jumlah Dosen Aktif', fontsize=13, fontweight='bold')
    ax.set_title('IKU 31: Dosen Aktif Tridharma di PT Lain per Program Studi\\ndengan Daftar Nama',
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', linestyle=':', alpha=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)

    # Expand x-axis untuk memberi ruang text annotations (lebih compact)
    max_count = max(prodi_groups['Count'])
    ax.set_xlim(0, max_count * 1.3)

    plt.tight_layout()

    # Save
    saved_files = save_figure(fig, 'IKU_31_breakdown_dosen_annotated')
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

    print("    → Dosen Annotated (Bar dengan Nama Dosen)...")
    all_files.extend(create_iku_31_dosen_annotated(df_pembilang, df_penyebut))

    print("    → Statistik Summary (Top Kegiatan & Jenis)...")
    all_files.extend(create_iku_31_statistik(df_pembilang, df_penyebut))

    print(f"  ✅ Breakdown IKU 31 selesai (2 charts)")
    return all_files

if __name__ == "__main__":
    create_iku_31_breakdown()
