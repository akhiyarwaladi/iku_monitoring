"""
============================================================================
IKU 42 BREAKDOWN: Pengajar Praktisi
============================================================================
Visualisasi breakdown untuk IKU 42 (Charts Terpisah):
1. Tabel Daftar Praktisi
2. Distribusi per Jurusan
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

def create_iku_42_tabel_praktisi(df_pembilang):
    """Chart 1: Tabel Daftar Praktisi"""

    # Data processing
    df_praktisi = df_pembilang[['Nama', 'Program Studi', 'Jurusan']].copy()
    df_praktisi['Program Studi'] = df_praktisi['Program Studi'].str.replace('Program Studi ', '')
    df_praktisi = df_praktisi.sort_values(['Jurusan', 'Program Studi', 'Nama'])
    df_praktisi['No'] = range(1, len(df_praktisi) + 1)

    # Create figure untuk tabel (full table, semua data)
    total = len(df_praktisi)
    rows_per_page = 40
    fig_height = max(10, rows_per_page * 0.35)

    fig, ax = plt.subplots(figsize=(14, fig_height))
    ax.axis('tight')
    ax.axis('off')

    # Ambil semua data untuk tabel
    table_data = df_praktisi.head(rows_per_page)[['No', 'Nama', 'Program Studi', 'Jurusan']].values

    table = ax.table(cellText=table_data,
                     colLabels=['No', 'Nama Dosen', 'Program Studi', 'Jurusan'],
                     cellLoc='left',
                     loc='center',
                     colWidths=[0.06, 0.44, 0.30, 0.20])

    # Styling tabel
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1, 1.6)

    # Header styling
    for i in range(4):
        cell = table[(0, i)]
        cell.set_facecolor('#5B9BD5')
        cell.set_text_props(weight='bold', color='white', fontsize=10)
        cell.set_edgecolor('white')
        cell.set_linewidth(1.5)

    # Alternate row colors dengan grouping per jurusan
    current_jurusan = None
    color_toggle = True

    for i in range(1, len(table_data) + 1):
        jurusan = table_data[i-1][3]

        # Reset color toggle saat ganti jurusan
        if jurusan != current_jurusan:
            color_toggle = not color_toggle
            current_jurusan = jurusan

        for j in range(4):
            cell = table[(i, j)]
            if color_toggle:
                cell.set_facecolor('#F0F0F0')
            else:
                cell.set_facecolor('#FFFFFF')
            cell.set_edgecolor('#CCCCCC')

    ax.set_title('IKU 42: Daftar Pengajar Praktisi\nFakultas Sains & Teknologi',
                 fontsize=13, fontweight='bold', pad=20, loc='left')

    if total > rows_per_page:
        ax.text(0.5, -0.02, f'* Menampilkan {rows_per_page} dari {total} praktisi',
                transform=ax.transAxes, ha='center',
                fontsize=9, style='italic', color='#666666')

    plt.tight_layout()

    # Save
    saved_files = save_figure(fig, 'IKU_42_breakdown_tabel_praktisi')
    plt.close()

    return saved_files

def create_iku_42_distribusi_jurusan(df_pembilang):
    """Chart 2: Distribusi per Jurusan"""

    # Data processing
    jurusan_dist = df_pembilang['Jurusan'].value_counts()

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))

    colors_jurusan = [JURUSAN_COLORS.get(j, {}).get('base', '#5B9BD5')
                      for j in jurusan_dist.index]

    y_pos = range(len(jurusan_dist))
    bars = ax.barh(y_pos, jurusan_dist.values,
                   color=colors_jurusan, edgecolor='black',
                   linewidth=1.2, alpha=0.85, height=0.7)

    # Labels
    for bar, jumlah in zip(bars, jurusan_dist.values):
        width = bar.get_width()
        ax.text(width + 0.8, bar.get_y() + bar.get_height()/2,
                f'{int(jumlah)}',
                ha='left', va='center', fontsize=11, fontweight='bold')

    # Styling
    ax.set_yticks(y_pos)
    ax.set_yticklabels(jurusan_dist.index, fontsize=10, fontweight='500')
    ax.set_xlabel('Jumlah Praktisi', fontsize=11, fontweight='bold')
    ax.set_title('IKU 42: Distribusi Pengajar Praktisi per Jurusan',
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
    saved_files = save_figure(fig, 'IKU_42_breakdown_distribusi_jurusan')
    plt.close()

    return saved_files

def create_iku_42_praktisi_annotated(df_pembilang):
    """Chart: Bar Chart dengan Nama Praktisi per Prodi"""

    # Group by Program Studi dan kumpulkan nama-nama dosen
    prodi_groups = df_pembilang.groupby('Program Studi').agg({
        'Nama': list,
        'Jurusan': 'first'
    }).reset_index()

    # Hitung jumlah praktisi per prodi
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
            # Split ke multiple lines (3 nama per line) agar tidak terlalu panjang
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
    ax.set_xlabel('Jumlah Praktisi', fontsize=13, fontweight='bold')
    ax.set_title('IKU 42: Distribusi Pengajar Praktisi per Program Studi\ndengan Daftar Nama',
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
    saved_files = save_figure(fig, 'IKU_42_breakdown_praktisi_annotated')
    plt.close()

    return saved_files

def create_iku_42_statistik(df_pembilang, df_penyebut):
    """Chart 3: Statistik Summary - Consistent Style"""

    # Data processing dengan verifikasi
    total_praktisi = len(df_pembilang)
    total_dosen_fst = len(df_penyebut)
    persentase = (total_praktisi / total_dosen_fst * 100) if total_dosen_fst > 0 else 0

    # Distribusi per jurusan
    jurusan_dist = df_pembilang['Jurusan'].value_counts()

    # Distribusi per program studi (top 10)
    prodi_dist = df_pembilang['Program Studi'].value_counts().head(10)
    prodi_dist.index = [p.replace('Program Studi ', '') for p in prodi_dist.index]

    # Create figure - simple layout seperti chart lainnya
    fig_height = max(8, max(len(jurusan_dist), len(prodi_dist)) * 0.45)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, fig_height))

    # Suptitle dengan info summary
    fig.suptitle(f'IKU 42: Statistik Summary - Pengajar dari Kalangan Praktisi\n' +
                 f'Total: {total_praktisi} praktisi | {total_dosen_fst} dosen FST | Persentase: {persentase:.1f}%',
                 fontsize=12, fontweight='bold', y=0.98)

    # ===== CHART 1: Distribusi per Jurusan (Left) =====
    y_pos = np.arange(len(jurusan_dist))
    colors_jurusan = [JURUSAN_COLORS.get(j, {}).get('base', '#5B9BD5')
                      for j in jurusan_dist.index]

    bars1 = ax1.barh(y_pos, jurusan_dist.values,
                     color=colors_jurusan, edgecolor='black',
                     linewidth=1.2, alpha=0.85, height=0.75)

    # Labels pada bars
    for bar, count in zip(bars1, jurusan_dist.values):
        width = bar.get_width()
        ax1.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=9, fontweight='bold')

    # Styling ax1
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(jurusan_dist.index, fontsize=9, fontweight='500')
    ax1.set_xlabel('Jumlah Praktisi', fontsize=11, fontweight='bold')
    ax1.set_title('Distribusi per Jurusan', fontsize=11, fontweight='bold', pad=15)
    ax1.xaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0)
    ax1.set_axisbelow(True)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_linewidth(1.2)
    ax1.spines['bottom'].set_linewidth(1.2)
    ax1.invert_yaxis()

    # ===== CHART 2: Top 10 Program Studi (Right) =====
    y_pos2 = np.arange(len(prodi_dist))
    colors_prodi = ['#3498DB', '#E74C3C', '#F39C12', '#1ABC9C', '#9B59B6',
                    '#E85D75', '#70AD47', '#5B9BD5', '#ED7D31', '#9966CC']

    bars2 = ax2.barh(y_pos2, prodi_dist.values,
                     color=colors_prodi[:len(prodi_dist)],
                     edgecolor='black', linewidth=1.2, alpha=0.85, height=0.75)

    # Labels pada bars
    for bar, count in zip(bars2, prodi_dist.values):
        width = bar.get_width()
        ax2.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=9, fontweight='bold')

    # Styling ax2
    ax2.set_yticks(y_pos2)
    prodi_labels = [name[:35] + '...' if len(name) > 35 else name for name in prodi_dist.index]
    ax2.set_yticklabels(prodi_labels, fontsize=9, fontweight='500')
    ax2.set_xlabel('Jumlah Praktisi', fontsize=11, fontweight='bold')
    ax2.set_title('Top 10 Program Studi', fontsize=11, fontweight='bold', pad=15)
    ax2.xaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0)
    ax2.set_axisbelow(True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_linewidth(1.2)
    ax2.spines['bottom'].set_linewidth(1.2)
    ax2.invert_yaxis()

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Save
    saved_files = save_figure(fig, 'IKU_42_breakdown_statistik')
    plt.close()

    return saved_files

def create_iku_42_breakdown():
    """Membuat semua breakdown visualizations untuk IKU 42 (charts terpisah)"""

    print("\n  [Breakdown] Membuat visualisasi breakdown IKU 42...")

    setup_publication_style()

    # Baca data
    df_pembilang = read_excel_iku('42', 'pembilang')
    df_penyebut = read_excel_iku('42', 'penyebut')

    # Generate semua charts terpisah (tanpa duplikasi)
    all_files = []

    print("    → Praktisi Annotated (Bar dengan Nama Dosen)...")
    all_files.extend(create_iku_42_praktisi_annotated(df_pembilang))

    print(f"  ✅ Breakdown IKU 42 selesai (1 chart)")
    return all_files

if __name__ == "__main__":
    create_iku_42_breakdown()
