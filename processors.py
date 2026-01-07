"""
============================================================================
DATA PROCESSORS - SISTEM VISUALISASI IKU
============================================================================

Modul ini berisi semua fungsi pemrosesan data untuk setiap IKU.

Author: Tim IKU FST
Version: 2.0 (Modular)
Last Updated: 2026-01-07
============================================================================
"""

import pandas as pd
from utils import read_excel_iku


# ============================================================================
# IKU 1 PROCESSORS (Lulusan - IKU 1.1 PDF)
# ============================================================================

def process_iku_11(df_pembilang, df_penyebut):
    """
    Proses data IKU 11 - Lulusan yang Memiliki Pekerjaan
    """
    penyebut_prodi = df_penyebut.groupby('Prodi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang.groupby('Prodi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Prodi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result = result.rename(columns={'Prodi': 'Program Studi'})
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result


def process_iku_12(df_pembilang, df_penyebut):
    """
    Proses data IKU 12 - Lulusan yang Melanjutkan Studi
    """
    penyebut_prodi = df_penyebut.groupby('Prodi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang.groupby('Prodi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Prodi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result = result.rename(columns={'Prodi': 'Program Studi'})
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result


def process_iku_13(df_pembilang, df_penyebut):
    """
    Proses data IKU 13 - Lulusan yang Berwiraswasta
    """
    penyebut_prodi = df_penyebut.groupby('Prodi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang.groupby('Prodi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Prodi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result = result.rename(columns={'Prodi': 'Program Studi'})
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result


def process_iku_1_combined():
    """
    Proses data IKU 1 Gabungan - Kombinasi IKU 11, 12, 13
    (Lulusan Bekerja + Studi Lanjut + Wiraswasta)
    Sesuai IKU 1.1 PDF: Target 60%
    """
    print("  → Membaca dan menggabungkan data IKU 11, 12, 13...")

    df11_pembilang = read_excel_iku('11', 'pembilang')
    df12_pembilang = read_excel_iku('12', 'pembilang')
    df13_pembilang = read_excel_iku('13', 'pembilang')
    df_penyebut = read_excel_iku('11', 'penyebut')

    print(f"    - IKU 11 (Bekerja): {len(df11_pembilang)} lulusan")
    print(f"    - IKU 12 (Studi Lanjut): {len(df12_pembilang)} lulusan")
    print(f"    - IKU 13 (Wiraswasta): {len(df13_pembilang)} lulusan")
    print(f"    - Total Penyebut: {len(df_penyebut)} lulusan")

    cols_to_keep = ['NIM', 'Nama', 'Prodi']

    df11_subset = df11_pembilang[cols_to_keep].copy()
    df11_subset['Sumber'] = 'Bekerja'

    df12_subset = df12_pembilang[cols_to_keep].copy()
    df12_subset['Sumber'] = 'Studi Lanjut'

    df13_subset = df13_pembilang[cols_to_keep].copy()
    df13_subset['Sumber'] = 'Wiraswasta'

    df_combined = pd.concat([df11_subset, df12_subset, df13_subset], ignore_index=True)
    df_pembilang_combined = df_combined.drop_duplicates(subset=['NIM'], keep='first')

    print(f"    - Gabungan unik: {len(df_pembilang_combined)} lulusan")

    total_pembilang = len(df_pembilang_combined)
    total_penyebut = len(df_penyebut)
    persentase_total = (total_pembilang / total_penyebut * 100) if total_penyebut > 0 else 0

    stats = {
        'pembilang': total_pembilang,
        'penyebut': total_penyebut,
        'persentase': round(persentase_total, 2)
    }

    penyebut_prodi = df_penyebut.groupby('Prodi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang_combined.groupby('Prodi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Prodi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result = result.rename(columns={'Prodi': 'Program Studi'})
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result, stats, df_pembilang_combined, df_penyebut


# ============================================================================
# IKU 2 PROCESSORS (Mahasiswa - IKU 1.2 PDF)
# ============================================================================

def process_iku_21(df_pembilang, df_penyebut):
    """
    Proses data IKU 21 - Mahasiswa yang Mengikuti Kegiatan MBKM
    """
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang.groupby('Program Studi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result


def process_iku_22(df_pembilang, df_penyebut):
    """
    Proses data IKU 22 - Mahasiswa yang Meraih Prestasi
    Note: File pembilang tidak memiliki kolom 'Program Studi', perlu join dengan penyebut
    """
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')

    pembilang_with_prodi = df_pembilang.merge(
        df_penyebut[['NIM', 'Program Studi']],
        on='NIM',
        how='left'
    )
    pembilang_prodi = pembilang_with_prodi.groupby('Program Studi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result


def process_iku_23(df_pembilang, df_penyebut):
    """
    Proses data IKU 23 - Mahasiswa yang Memiliki HKI
    """
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang.groupby('Program Studi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result


def process_iku_2_combined():
    """
    Proses data IKU 2 Gabungan - Kombinasi IKU 21, 22, 23
    (Mahasiswa MBKM + Prestasi + HKI)
    Sesuai IKU 1.2 PDF: Target 30%
    """
    print("  → Membaca dan menggabungkan data IKU 21, 22, 23...")

    df21_pembilang = read_excel_iku('21', 'pembilang')
    df22_pembilang = read_excel_iku('22', 'pembilang')
    df23_pembilang = read_excel_iku('23', 'pembilang')
    df_penyebut = read_excel_iku('21', 'penyebut')

    print(f"    - IKU 21 (MBKM): {len(df21_pembilang)} mahasiswa")
    print(f"    - IKU 22 (Prestasi): {len(df22_pembilang)} mahasiswa")
    print(f"    - IKU 23 (HKI): {len(df23_pembilang)} mahasiswa")
    print(f"    - Total Penyebut: {len(df_penyebut)} mahasiswa")

    # IKU 21 sudah punya Program Studi
    df21_subset = df21_pembilang[['NIM', 'Nama', 'Program Studi']].copy()
    df21_subset['Sumber'] = 'MBKM'

    # IKU 22 TIDAK punya Program Studi, perlu join dengan penyebut
    df22_with_prodi = df22_pembilang.merge(
        df_penyebut[['NIM', 'Nama', 'Program Studi']].drop_duplicates(),
        on='NIM', how='left', suffixes=('', '_y')
    )
    df22_subset = df22_with_prodi[['NIM', 'Nama_y', 'Program Studi']].copy()
    df22_subset.columns = ['NIM', 'Nama', 'Program Studi']
    df22_subset['Sumber'] = 'Prestasi'

    # IKU 23 sudah punya Program Studi
    df23_subset = df23_pembilang[['NIM', 'Nama', 'Program Studi']].copy()
    df23_subset['Sumber'] = 'HKI'

    df_combined = pd.concat([df21_subset, df22_subset, df23_subset], ignore_index=True)
    df_pembilang_combined = df_combined.drop_duplicates(subset=['NIM'], keep='first')

    print(f"    - Gabungan unik: {len(df_pembilang_combined)} mahasiswa")

    total_pembilang = len(df_pembilang_combined)
    total_penyebut = len(df_penyebut)
    persentase_total = (total_pembilang / total_penyebut * 100) if total_penyebut > 0 else 0

    stats = {
        'pembilang': total_pembilang,
        'penyebut': total_penyebut,
        'persentase': round(persentase_total, 2)
    }

    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang_combined.groupby('Program Studi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result, stats, df_pembilang_combined, df_penyebut


# ============================================================================
# IKU 3 PROCESSORS (Dosen Tridharma - IKU 2.1 PDF)
# ============================================================================

def process_iku_31(df_pembilang, df_penyebut):
    """
    Proses data IKU 31 - Tridharma di PT Lain
    """
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')

    pembilang_with_prodi = df_pembilang.merge(
        df_penyebut[['NIP', 'Program Studi']],
        on='NIP',
        how='left'
    )
    pembilang_prodi = pembilang_with_prodi.groupby('Program Studi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result


def normalize_prodi_name(name):
    """Helper function to normalize Program Studi names"""
    if pd.isna(name):
        return name
    name = str(name).strip()
    if not name.startswith('Program Studi'):
        if name == 'Analis Kimia':
            return 'Program Studi Analis Kimia (D3)'
        elif name == 'Kimia Industri':
            return 'Program Studi Kimia Industri (D3)'
        else:
            return f'Program Studi {name}'
    return name


def process_iku_33(df_pembilang, df_penyebut):
    """
    Proses data IKU 33 - Membimbing Mahasiswa Luar Prodi
    """
    df_pembilang = df_pembilang.copy()
    df_pembilang['Program Studi'] = df_pembilang['Program Studi'].apply(normalize_prodi_name)

    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang.groupby('Program Studi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result


def process_iku_3_combined():
    """
    Proses data IKU 3 Gabungan - Kombinasi IKU 31, 33
    (Dosen Tridharma di PT Lain + Membimbing Mahasiswa Luar Prodi)
    Sesuai IKU 2.1 PDF: Target 25%
    """
    print("  → Membaca dan menggabungkan data IKU 31, 33...")

    df31_pembilang = read_excel_iku('31', 'pembilang')
    df33_pembilang = read_excel_iku('33', 'pembilang')
    df_penyebut = read_excel_iku('31', 'penyebut')

    print(f"    - IKU 31 (Tridharma): {len(df31_pembilang)} dosen")
    print(f"    - IKU 33 (Bimbingan): {len(df33_pembilang)} dosen")
    print(f"    - Total Penyebut: {len(df_penyebut)} dosen")

    # IKU 31: TIDAK punya Program Studi, perlu join dengan penyebut
    df31_with_prodi = df31_pembilang.merge(
        df_penyebut[['NIP', 'Program Studi']].drop_duplicates(),
        on='NIP', how='left'
    )
    df31_subset = df31_with_prodi[['NIP', 'Nama', 'Program Studi']].copy()
    df31_subset['Sumber'] = 'Tridharma'

    # IKU 33: SUDAH punya Program Studi, tapi kolom nama dosen adalah 'Dosen Pembimbing'
    df33_pembilang_copy = df33_pembilang.copy()
    df33_pembilang_copy['Program Studi'] = df33_pembilang_copy['Program Studi'].apply(
        lambda x: f'Program Studi {x}' if pd.notna(x) and not str(x).startswith('Program Studi') else x
    )
    df33_subset = df33_pembilang_copy[['NIP', 'Dosen Pembimbing', 'Program Studi']].copy()
    df33_subset.columns = ['NIP', 'Nama', 'Program Studi']
    df33_subset['Sumber'] = 'Bimbingan'

    df_combined = pd.concat([df31_subset, df33_subset], ignore_index=True)
    df_pembilang_combined = df_combined.drop_duplicates(subset=['NIP'], keep='first')

    print(f"    - Gabungan unik: {len(df_pembilang_combined)} dosen")

    total_pembilang = len(df_pembilang_combined)
    total_penyebut = len(df_penyebut)
    persentase_total = (total_pembilang / total_penyebut * 100) if total_penyebut > 0 else 0

    stats = {
        'pembilang': total_pembilang,
        'penyebut': total_penyebut,
        'persentase': round(persentase_total, 2)
    }

    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang_combined.groupby('Program Studi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result, stats, df_pembilang_combined, df_penyebut


# ============================================================================
# IKU 4 PROCESSORS (Dosen DUDI - IKU 2.2 PDF)
# ============================================================================

def process_iku_41(df_pembilang, df_penyebut):
    """
    Proses data IKU 41 - Sertifikat DUDI
    """
    df_pembilang = df_pembilang.copy()
    df_pembilang['Program Studi'] = df_pembilang['Program Studi'].apply(normalize_prodi_name)

    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang.groupby('Program Studi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result


def process_iku_42(df_pembilang, df_penyebut):
    """
    Proses data IKU 42 - Pengajar dari Kalangan Praktisi
    """
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang.groupby('Program Studi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result


def process_iku_4_combined():
    """
    Proses data IKU 4 Gabungan - Kombinasi IKU 41, 42
    (Dosen Sertifikat DUDI + Pengajar dari Praktisi)
    Sesuai IKU 2.2 PDF: Target 20.14%
    """
    print("  → Membaca dan menggabungkan data IKU 41, 42...")

    df41_pembilang = read_excel_iku('41', 'pembilang')
    df42_pembilang = read_excel_iku('42', 'pembilang')
    df_penyebut = read_excel_iku('41', 'penyebut')

    print(f"    - IKU 41 (Sertifikat DUDI): {len(df41_pembilang)} dosen")
    print(f"    - IKU 42 (Praktisi): {len(df42_pembilang)} dosen")
    print(f"    - Total Penyebut: {len(df_penyebut)} dosen")

    # Join dengan penyebut untuk mendapatkan Program Studi jika belum ada
    if 'Program Studi' not in df41_pembilang.columns:
        df41_pembilang = df41_pembilang.merge(
            df_penyebut[['NIP', 'Program Studi']].drop_duplicates(),
            on='NIP', how='left'
        )
    if 'Program Studi' not in df42_pembilang.columns:
        df42_pembilang = df42_pembilang.merge(
            df_penyebut[['NIP', 'Program Studi']].drop_duplicates(),
            on='NIP', how='left'
        )

    df41_subset = df41_pembilang[['NIP', 'Nama', 'Program Studi']].copy()
    df41_subset['Sumber'] = 'Sertifikat DUDI'

    df42_subset = df42_pembilang[['NIP', 'Nama', 'Program Studi']].copy()
    df42_subset['Sumber'] = 'Praktisi'

    df_combined = pd.concat([df41_subset, df42_subset], ignore_index=True)
    df_pembilang_combined = df_combined.drop_duplicates(subset=['NIP'], keep='first')

    print(f"    - Gabungan unik: {len(df_pembilang_combined)} dosen")

    total_pembilang = len(df_pembilang_combined)
    total_penyebut = len(df_penyebut)
    persentase_total = (total_pembilang / total_penyebut * 100) if total_penyebut > 0 else 0

    stats = {
        'pembilang': total_pembilang,
        'penyebut': total_penyebut,
        'persentase': round(persentase_total, 2)
    }

    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang_combined.groupby('Program Studi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result, stats, df_pembilang_combined, df_penyebut


# ============================================================================
# IKU 7 PROCESSORS (Mata Kuliah PJBL/Case Method)
# ============================================================================

def process_iku_71(df_pembilang, df_penyebut):
    """
    Proses data IKU 71 - Mata Kuliah menggunakan PJBL/Case Method
    Entity: Mata Kuliah (bukan dosen/mahasiswa)
    """
    # Group by Program Studi
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')
    pembilang_prodi = df_pembilang.groupby('Program Studi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result


def process_iku_7_combined():
    """
    Proses data IKU 7 Gabungan (hanya IKU 71)
    Mata Kuliah yang menggunakan PJBL/Case Method
    Target: 50%
    """
    print("  → Membaca data IKU 71...")

    df71_pembilang = read_excel_iku('71', 'pembilang')
    df_penyebut = read_excel_iku('71', 'penyebut')

    print(f"    - IKU 71 (PJBL/Case Method): {len(df71_pembilang)} mata kuliah")
    print(f"    - Total Penyebut: {len(df_penyebut)} mata kuliah")

    total_pembilang = len(df71_pembilang)
    total_penyebut = len(df_penyebut)
    persentase_total = (total_pembilang / total_penyebut * 100) if total_penyebut > 0 else 0

    stats = {
        'pembilang': total_pembilang,
        'penyebut': total_penyebut,
        'persentase': round(persentase_total, 2)
    }

    # Process per prodi
    penyebut_prodi = df_penyebut.groupby('Program Studi').size().reset_index(name='Penyebut')
    pembilang_prodi = df71_pembilang.groupby('Program Studi').size().reset_index(name='Pembilang')

    result = penyebut_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Persentase'] = (result['Pembilang'] / result['Penyebut'] * 100).round(2)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result, stats, df71_pembilang, df_penyebut


# ============================================================================
# IKU 8 PROCESSORS (Prodi Akreditasi Internasional)
# ============================================================================

def process_iku_81(df_pembilang, df_penyebut):
    """
    Proses data IKU 81 - Program Studi dengan Akreditasi Internasional
    Entity: Program Studi
    """
    # Get list of prodi with international accreditation
    prodi_akreditasi = set(df_pembilang['Program Studi'].dropna().unique())

    # Create result per prodi (1 if has accreditation, 0 otherwise)
    result_data = []
    for _, row in df_penyebut.iterrows():
        prodi = row['Program Studi']
        has_akreditasi = 1 if prodi in prodi_akreditasi else 0
        result_data.append({
            'Program Studi': prodi,
            'Pembilang': has_akreditasi,
            'Penyebut': 1,
            'Persentase': 100.0 if has_akreditasi else 0.0
        })

    result = pd.DataFrame(result_data)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result


def process_iku_8_combined():
    """
    Proses data IKU 8 Gabungan (hanya IKU 81)
    Program Studi dengan Akreditasi Internasional
    Target: 10%
    """
    print("  → Membaca data IKU 81...")

    df81_pembilang = read_excel_iku('81', 'pembilang')
    df_penyebut = read_excel_iku('81', 'penyebut')

    print(f"    - IKU 81 (Akreditasi Internasional): {len(df81_pembilang)} prodi")
    print(f"    - Total Penyebut: {len(df_penyebut)} prodi")

    total_pembilang = len(df81_pembilang)
    total_penyebut = len(df_penyebut)
    persentase_total = (total_pembilang / total_penyebut * 100) if total_penyebut > 0 else 0

    stats = {
        'pembilang': total_pembilang,
        'penyebut': total_penyebut,
        'persentase': round(persentase_total, 2)
    }

    # Get list of prodi with international accreditation
    prodi_akreditasi = set(df81_pembilang['Program Studi'].dropna().unique())

    # Create result per prodi
    result_data = []
    for _, row in df_penyebut.iterrows():
        prodi = row['Program Studi']
        has_akreditasi = 1 if prodi in prodi_akreditasi else 0
        result_data.append({
            'Program Studi': prodi,
            'Pembilang': has_akreditasi,
            'Penyebut': 1,
            'Persentase': 100.0 if has_akreditasi else 0.0
        })

    result = pd.DataFrame(result_data)
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Persentase', ascending=True)

    return result, stats, df81_pembilang, df_penyebut


# ============================================================================
# IKU 5 PROCESSORS (Luaran Dosen Rekognisi Internasional)
# ============================================================================

def process_iku_51(df_pembilang, df_penyebut):
    """
    Proses data IKU 51 - Luaran Dosen Rekognisi Internasional
    NUMBER-BASED: Target adalah jumlah, bukan persentase
    """
    # Use dosen penyebut for reference (from IKU 31)
    df_dosen = read_excel_iku('31', 'penyebut')

    # Count luaran per prodi
    prodi_col = 'Program Studi' if 'Program Studi' in df_pembilang.columns else 'Prodi'

    # Join with dosen to get prodi
    if 'NIP' in df_pembilang.columns:
        df_merged = df_pembilang.merge(df_dosen[['NIP', 'Program Studi']], on='NIP', how='left')
        pembilang_prodi = df_merged.groupby('Program Studi').size().reset_index(name='Pembilang')
    else:
        pembilang_prodi = df_pembilang.groupby(prodi_col).size().reset_index(name='Pembilang')
        pembilang_prodi = pembilang_prodi.rename(columns={prodi_col: 'Program Studi'})

    # Get all prodi from dosen penyebut
    all_prodi = df_dosen.groupby('Program Studi').size().reset_index(name='Dosen')

    result = all_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Penyebut'] = 1  # Target 1 luaran per prodi as baseline
    result['Persentase'] = result['Pembilang']  # Show count directly
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Pembilang', ascending=True)

    return result


def process_iku_5_combined():
    """
    Proses data IKU 5 Gabungan (IKU 51)
    Luaran Dosen dengan Rekognisi Internasional
    NUMBER-BASED: Target = 5 (jumlah luaran)
    """
    print("  → Membaca data IKU 51...")

    df51_pembilang = read_excel_iku('51', 'pembilang')
    df_dosen = read_excel_iku('31', 'penyebut')  # Use dosen as reference

    total_luaran = len(df51_pembilang)
    dosen_unik = df51_pembilang['NIP'].nunique() if 'NIP' in df51_pembilang.columns else total_luaran

    print(f"    - IKU 51 (Luaran Rekognisi): {total_luaran} luaran")
    print(f"    - Dosen unik dengan luaran: {dosen_unik} dosen")
    print(f"    - Total Dosen (referensi): {len(df_dosen)} dosen")

    # NUMBER-BASED: pembilang = actual, penyebut = target
    target = 5  # Target 5 luaran
    persentase_vs_target = (total_luaran / target * 100) if target > 0 else 0

    stats = {
        'pembilang': total_luaran,
        'penyebut': target,  # target number
        'persentase': round(persentase_vs_target, 2),
        'is_number_based': True
    }

    # Process per prodi
    if 'NIP' in df51_pembilang.columns:
        df_merged = df51_pembilang.merge(df_dosen[['NIP', 'Program Studi']], on='NIP', how='left')
        pembilang_prodi = df_merged.groupby('Program Studi').size().reset_index(name='Pembilang')
    else:
        pembilang_prodi = pd.DataFrame({'Program Studi': [], 'Pembilang': []})

    all_prodi = df_dosen.groupby('Program Studi').size().reset_index(name='Dosen')

    result = all_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Penyebut'] = 1
    result['Persentase'] = result['Pembilang']
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Pembilang', ascending=True)

    return result, stats, df51_pembilang, df_dosen


# ============================================================================
# IKU 6 PROCESSORS (Kerjasama per Program Studi)
# ============================================================================

def process_iku_62(df_pembilang, df_penyebut):
    """
    Proses data IKU 62 - Kerjasama per Program Studi
    NUMBER-BASED: Target adalah jumlah per prodi
    """
    df_prodi = read_excel_iku('81', 'penyebut')  # Use prodi as reference

    prodi_col = 'Program Studi'
    pembilang_prodi = df_pembilang.groupby(prodi_col).size().reset_index(name='Pembilang')

    all_prodi = df_prodi[['Program Studi']].copy()

    result = all_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Penyebut'] = 2  # Target 2 per prodi
    result['Persentase'] = result['Pembilang']  # Show count directly
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Pembilang', ascending=True)

    return result


def process_iku_6_combined():
    """
    Proses data IKU 6 Gabungan (IKU 62)
    Kerjasama per Program Studi
    NUMBER-BASED: Target = 2 per prodi
    """
    print("  → Membaca data IKU 62...")

    df62_pembilang = read_excel_iku('62', 'pembilang')
    df_prodi = read_excel_iku('81', 'penyebut')  # Use prodi as reference

    total_kerjasama = len(df62_pembilang)
    total_prodi = len(df_prodi)
    avg_per_prodi = total_kerjasama / total_prodi if total_prodi > 0 else 0

    print(f"    - IKU 62 (Kerjasama): {total_kerjasama} kerjasama")
    print(f"    - Total Prodi: {total_prodi} prodi")
    print(f"    - Rata-rata per prodi: {avg_per_prodi:.2f}")

    # NUMBER-BASED: compare avg per prodi vs target
    target_per_prodi = 2
    persentase_vs_target = (avg_per_prodi / target_per_prodi * 100) if target_per_prodi > 0 else 0

    stats = {
        'pembilang': round(avg_per_prodi, 2),  # avg per prodi
        'penyebut': target_per_prodi,  # target per prodi
        'persentase': round(persentase_vs_target, 2),
        'is_number_based': True,
        'total_kerjasama': total_kerjasama,
        'total_prodi': total_prodi
    }

    # Process per prodi
    prodi_col = 'Program Studi'
    pembilang_prodi = df62_pembilang.groupby(prodi_col).size().reset_index(name='Pembilang')

    all_prodi = df_prodi[['Program Studi']].copy()

    result = all_prodi.merge(pembilang_prodi, on='Program Studi', how='left')
    result['Pembilang'] = result['Pembilang'].fillna(0).astype(int)
    result['Penyebut'] = target_per_prodi
    result['Persentase'] = result['Pembilang']
    result['Program Studi'] = result['Program Studi'].str.replace('Program Studi ', '')
    result = result.sort_values('Pembilang', ascending=True)

    return result, stats, df62_pembilang, df_prodi


# ============================================================================
# PROCESSOR MAPPING
# ============================================================================

# Mapping IKU number to processor function
IKU_PROCESSORS = {
    '11': process_iku_11,
    '12': process_iku_12,
    '13': process_iku_13,
    '21': process_iku_21,
    '22': process_iku_22,
    '23': process_iku_23,
    '31': process_iku_31,
    '33': process_iku_33,
    '41': process_iku_41,
    '42': process_iku_42,
    '51': process_iku_51,
    '62': process_iku_62,
    '71': process_iku_71,
    '81': process_iku_81,
}

# Mapping combined IKU number to processor function
COMBINED_PROCESSORS = {
    '1': (process_iku_1_combined, 'lulusan', '11, 12, 13'),
    '2': (process_iku_2_combined, 'mahasiswa', '21, 22, 23'),
    '3': (process_iku_3_combined, 'dosen', '31, 33'),
    '4': (process_iku_4_combined, 'dosen', '41, 42'),
    '5': (process_iku_5_combined, 'luaran', '51'),
    '6': (process_iku_6_combined, 'kerjasama', '62'),
    '7': (process_iku_7_combined, 'mata kuliah', '71'),
    '8': (process_iku_8_combined, 'prodi', '81'),
}
