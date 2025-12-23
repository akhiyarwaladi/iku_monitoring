"""
============================================================================
BREAKDOWN UTILITIES
Fungsi-fungsi umum untuk breakdown charts
============================================================================
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap
import numpy as np
from visualization_config import (
    BREAKDOWN_STYLE, JURUSAN_COLORS, JURUSAN_ORDER,
    save_figure, setup_publication_style, get_prodi_color
)

def create_annotated_bar_chart(df_data,
                                 groupby_col='Program Studi',
                                 name_col='Nama',
                                 jurusan_col='Jurusan',
                                 chart_title='',
                                 xlabel='Jumlah',
                                 filename_base='',
                                 max_names_full=6):
    """
    Membuat horizontal bar chart dengan nama-nama di-annotate di samping bar

    Parameters:
    -----------
    df_data : pd.DataFrame
        DataFrame dengan kolom name_col, groupby_col, dan jurusan_col
    groupby_col : str
        Kolom untuk grouping (biasanya 'Program Studi')
    name_col : str
        Kolom yang berisi nama (biasanya 'Nama')
    jurusan_col : str
        Kolom yang berisi jurusan
    chart_title : str
        Judul chart
    xlabel : str
        Label untuk x-axis
    filename_base : str
        Base filename untuk save
    max_names_full : int
        Maksimal jumlah untuk menampilkan semua nama

    Returns:
    --------
    list : List of saved file paths
    """

    # Group by dan kumpulkan nama-nama
    grouped = df_data.groupby(groupby_col).agg({
        name_col: list,
        jurusan_col: 'first'
    }).reset_index()

    # Hitung jumlah per group
    grouped['Count'] = grouped[name_col].apply(len)

    # Sort by jurusan first (untuk grouping yang bermakna), then by count within jurusan
    # Tambahkan jurusan_order untuk sorting
    jurusan_order_map = {j: i for i, j in enumerate(JURUSAN_ORDER)}
    grouped['jurusan_order'] = grouped[jurusan_col].map(
        lambda x: jurusan_order_map.get(x, 999)
    )

    # Sort: jurusan ascending (untuk grouping), count ascending within jurusan (bottom to top)
    grouped = grouped.sort_values(['jurusan_order', 'Count'], ascending=[True, True])

    # Create figure dengan height yang cukup
    style = BREAKDOWN_STYLE
    fig_height = max(style['min_fig_height'],
                     len(grouped) * style['fig_height_per_item'])
    fig, ax = plt.subplots(figsize=(16, fig_height))

    y_pos = np.arange(len(grouped))

    # Warna berdasarkan jurusan dengan gradient (match dengan main charts)
    # Hitung jumlah prodi per jurusan
    jurusan_counts = grouped[jurusan_col].value_counts().to_dict()

    # Assign colors dalam urutan yang sama dengan dataframe
    colors = []
    jurusan_idx = {}  # Track current index within each jurusan

    for _, row in grouped.iterrows():
        prodi_name = row[groupby_col]
        jurusan = row[jurusan_col]

        # Initialize index for this jurusan if first time
        if jurusan not in jurusan_idx:
            jurusan_idx[jurusan] = 0

        # Get color with gradient
        total_in_jurusan = jurusan_counts[jurusan]
        idx = jurusan_idx[jurusan]
        color = get_prodi_color(prodi_name, idx, total_in_jurusan)
        colors.append(color)

        # Increment index for this jurusan
        jurusan_idx[jurusan] += 1

    # Buat bars (styling match dengan main charts)
    bars = ax.barh(y_pos, grouped['Count'].values,
                   color=colors, edgecolor='#1a1a1a',
                   linewidth=1.5, alpha=0.88, height=0.75)

    # Tambahkan separator lines antar jurusan (match dengan main charts)
    jurusan_list = grouped[jurusan_col].tolist()
    current_jurusan = None
    for i, jurusan in enumerate(jurusan_list):
        if current_jurusan is not None and jurusan != current_jurusan:
            # Garis separator tegas
            ax.axhline(y=i-0.5, color='#333333', linestyle='-',
                      linewidth=1.5, alpha=0.6, zorder=2)
        current_jurusan = jurusan

    # Tambahkan nama-nama di samping bar
    for idx, (bar, row) in enumerate(zip(bars, grouped.itertuples())):
        count = row.Count
        nama_list = getattr(row, name_col.replace(' ', '_'))

        # Format nama
        if count <= max_names_full:
            # Tampilkan semua nama
            all_names = [n.split(',')[0].strip() for n in nama_list]
            nama_text = ', '.join(all_names)
        else:
            # Tampilkan 2 nama pertama + "dan X lainnya"
            first_names = [n.split(',')[0].strip() for n in nama_list[:2]]
            nama_text = ', '.join(first_names) + f' dan {count-2} lainnya'

        # Wrap text
        wrapped_text = '\n'.join(textwrap.wrap(nama_text, width=style['text_wrap_width']))

        # Tampilkan text di samping bar
        ax.text(bar.get_width() + style['annotation_offset_x'],
                bar.get_y() + bar.get_height()/2,
                wrapped_text,
                ha='left', va='center',
                fontsize=style['faculty_name_size'],
                color=style['annotation_color'])

        # Tampilkan count di dalam bar
        count_color = (style['count_color_dark'] if count > style['count_threshold']
                      else style['count_color_light'])
        ax.text(bar.get_width() + style['count_offset_x'],
                bar.get_y() + bar.get_height()/2,
                f'{count}',
                ha='right', va='center',
                fontsize=style['count_label_size'],
                fontweight='900',
                color=count_color)

    # Styling (match dengan main charts)
    ax.set_yticks(y_pos)
    labels = [label.replace('Program Studi ', '') for label in grouped[groupby_col]]
    ax.set_yticklabels(labels, fontsize=10, fontweight='600')
    ax.set_xlabel(xlabel, fontsize=12, fontweight='700')
    ax.set_title(chart_title, fontsize=13, fontweight='900', pad=20)
    ax.grid(axis='x', linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # Expand x-axis untuk memberi ruang text annotations
    max_count = max(grouped['Count'])
    ax.set_xlim(0, max_count * style['x_axis_multiplier'])

    plt.tight_layout()

    # Save
    saved_files = save_figure(fig, filename_base)
    plt.close()

    return saved_files


def create_dual_bar_chart(left_data, right_data,
                          left_title='', right_title='',
                          main_title='',
                          left_xlabel='', right_xlabel='',
                          filename_base='',
                          left_colors=None, right_colors=None,
                          left_wrap_width=35, right_wrap_width=35):
    """
    Membuat figure dengan 2 horizontal bar charts side-by-side

    Parameters:
    -----------
    left_data : pd.Series
        Data untuk chart kiri (index = labels, values = counts)
    right_data : pd.Series
        Data untuk chart kanan
    left_title, right_title : str
        Subtitle untuk masing-masing chart
    main_title : str
        Main title di atas kedua chart
    left_xlabel, right_xlabel : str
        X-axis labels
    filename_base : str
        Base filename untuk save
    left_colors, right_colors : list
        List warna untuk bars
    left_wrap_width, right_wrap_width : int
        Text wrapping width

    Returns:
    --------
    list : List of saved file paths
    """

    style = BREAKDOWN_STYLE

    # Determine figure height
    max_items = max(len(left_data), len(right_data))
    fig_height = max(style['min_fig_height'], max_items * 0.7)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, fig_height))

    # LEFT CHART
    y_pos1 = np.arange(len(left_data))
    if left_colors is None:
        # Use colorblind-friendly palette untuk variasi visual
        palette = sns.color_palette("colorblind", n_colors=len(left_data))
        left_colors = palette

    bars1 = ax1.barh(y_pos1, left_data.values,
                     color=left_colors, edgecolor='#1a1a1a',
                     linewidth=1.5, alpha=0.88, height=0.75)

    # Labels pada bars
    for bar, count in zip(bars1, left_data.values):
        width = bar.get_width()
        ax1.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=10, fontweight='900')

    # Styling ax1 (match dengan main charts)
    ax1.set_yticks(y_pos1)
    left_labels = ['\n'.join(textwrap.wrap(name, width=left_wrap_width))
                   for name in left_data.index]
    ax1.set_yticklabels(left_labels, fontsize=10, fontweight='600')
    ax1.set_xlabel(left_xlabel, fontsize=12, fontweight='700')
    ax1.set_title(left_title, fontsize=13, fontweight='900', pad=15)
    ax1.xaxis.grid(True, linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax1.set_axisbelow(True)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_linewidth(1.5)
    ax1.spines['bottom'].set_linewidth(1.5)
    ax1.invert_yaxis()

    # RIGHT CHART
    y_pos2 = np.arange(len(right_data))
    if right_colors is None:
        # Use warm palette untuk right chart (berbeda dari left)
        palette = sns.color_palette("Set2", n_colors=len(right_data))
        right_colors = palette

    bars2 = ax2.barh(y_pos2, right_data.values,
                     color=right_colors, edgecolor='#1a1a1a',
                     linewidth=1.5, alpha=0.88, height=0.75)

    # Labels pada bars
    for bar, count in zip(bars2, right_data.values):
        width = bar.get_width()
        ax2.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=10, fontweight='900')

    # Styling ax2 (match dengan main charts)
    ax2.set_yticks(y_pos2)
    right_labels = ['\n'.join(textwrap.wrap(name, width=right_wrap_width))
                    for name in right_data.index]
    ax2.set_yticklabels(right_labels, fontsize=10, fontweight='600')
    ax2.set_xlabel(right_xlabel, fontsize=12, fontweight='700')
    ax2.set_title(right_title, fontsize=13, fontweight='900', pad=15)
    ax2.xaxis.grid(True, linestyle=':', alpha=0.6, zorder=0, linewidth=0.8)
    ax2.set_axisbelow(True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_linewidth(1.5)
    ax2.spines['bottom'].set_linewidth(1.5)
    ax2.invert_yaxis()

    # Main title (match dengan main charts)
    if main_title:
        fig.suptitle(main_title, fontsize=13, fontweight='900', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95] if main_title else None)

    # Save
    saved_files = save_figure(fig, filename_base)
    plt.close()

    return saved_files
