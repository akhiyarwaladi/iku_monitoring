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
import textwrap
import numpy as np
from visualization_config import (
    BREAKDOWN_STYLE, JURUSAN_COLORS,
    save_figure, setup_publication_style
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
    grouped = grouped.sort_values('Count', ascending=True)

    # Create figure dengan height yang cukup
    style = BREAKDOWN_STYLE
    fig_height = max(style['min_fig_height'],
                     len(grouped) * style['fig_height_per_item'])
    fig, ax = plt.subplots(figsize=(16, fig_height))

    y_pos = np.arange(len(grouped))

    # Warna berdasarkan jurusan
    colors = [JURUSAN_COLORS.get(j, {}).get('base', '#5B9BD5')
              for j in grouped[jurusan_col]]

    # Buat bars
    bars = ax.barh(y_pos, grouped['Count'].values,
                   color=colors, edgecolor='black',
                   linewidth=1.2, alpha=0.85, height=style['bar_height'])

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
                fontweight='bold',
                color=count_color)

    # Styling
    ax.set_yticks(y_pos)
    labels = [label.replace('Program Studi ', '') for label in grouped[groupby_col]]
    ax.set_yticklabels(labels, fontsize=style['prodi_label_size'], fontweight='500')
    ax.set_xlabel(xlabel, fontsize=style['xlabel_size'], fontweight='bold')
    ax.set_title(chart_title, fontsize=style['title_size'], fontweight='bold', pad=20)
    ax.grid(axis='x', linestyle=':', alpha=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)

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
        left_colors = ['#5B9BD5'] * len(left_data)

    bars1 = ax1.barh(y_pos1, left_data.values,
                     color=left_colors, edgecolor='black',
                     linewidth=1.2, alpha=0.85, height=0.75)

    # Labels pada bars
    for bar, count in zip(bars1, left_data.values):
        width = bar.get_width()
        ax1.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=10, fontweight='bold')

    # Styling ax1
    ax1.set_yticks(y_pos1)
    left_labels = ['\n'.join(textwrap.wrap(name, width=left_wrap_width))
                   for name in left_data.index]
    ax1.set_yticklabels(left_labels, fontsize=10, fontweight='500')
    ax1.set_xlabel(left_xlabel, fontsize=12, fontweight='bold')
    ax1.set_title(left_title, fontsize=12, fontweight='bold', pad=15)
    ax1.xaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0)
    ax1.set_axisbelow(True)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_linewidth(1.2)
    ax1.spines['bottom'].set_linewidth(1.2)
    ax1.invert_yaxis()

    # RIGHT CHART
    y_pos2 = np.arange(len(right_data))
    if right_colors is None:
        right_colors = ['#E74C3C'] * len(right_data)

    bars2 = ax2.barh(y_pos2, right_data.values,
                     color=right_colors, edgecolor='black',
                     linewidth=1.2, alpha=0.85, height=0.75)

    # Labels pada bars
    for bar, count in zip(bars2, right_data.values):
        width = bar.get_width()
        ax2.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                f'{int(count)}',
                ha='left', va='center', fontsize=10, fontweight='bold')

    # Styling ax2
    ax2.set_yticks(y_pos2)
    right_labels = ['\n'.join(textwrap.wrap(name, width=right_wrap_width))
                    for name in right_data.index]
    ax2.set_yticklabels(right_labels, fontsize=10, fontweight='500')
    ax2.set_xlabel(right_xlabel, fontsize=12, fontweight='bold')
    ax2.set_title(right_title, fontsize=12, fontweight='bold', pad=15)
    ax2.xaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, linewidth=1.0)
    ax2.set_axisbelow(True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_linewidth(1.2)
    ax2.spines['bottom'].set_linewidth(1.2)
    ax2.invert_yaxis()

    # Main title
    if main_title:
        fig.suptitle(main_title, fontsize=13, fontweight='bold', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95] if main_title else None)

    # Save
    saved_files = save_figure(fig, filename_base)
    plt.close()

    return saved_files
