import numpy as numpy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_collection_types_per_month_df(df):
  pass

def create_borrow_duration_df(df):
  pass

def create_borrower_by_faculty_per_month_df(df):
  pinjaman_bulanan_by_fakultas = df.groupby([pd.Grouper(key='Tgl Pinjam', freq='M'), 'Fakultas Pemustaka'])['Nomor Buku'].count().unstack(fill_value=0)
  pinjaman_bulanan_by_fakultas.index = pinjaman_bulanan_by_fakultas.index.month_name()
  return pinjaman_bulanan_by_fakultas.reset_index().melt(id_vars='Tgl Pinjam', var_name='Fakultas', value_name='Banyak Pinjaman')

def create_transactions_df(df):
  pass

### MAIN PROGRAM
df_pinjaman = pd.read_csv('daftar-peminjaman-2022.csv')

# Ubah tipe data kolom Tgl Pinjam dan Tgl Kembali menjadi datetime untuk visualisasi
kolom_tgl = ['Tgl Pinjam', 'Tgl Kembali']

for kolom in kolom_tgl:
    df_pinjaman[kolom] = pd.to_datetime(df_pinjaman[kolom], format='%Y-%m-%d', errors='coerce')

# Visualisasi jumlah pinjaman berdasarkan tipe koleksi per bulan

# Visualisasi durasi pinjaman

# Visualisasi jumlah pinjaman berdasarkan fakultas peminjam per bulan
df_borrower_by_faculty_per_month = create_borrower_by_faculty_per_month_df(df_pinjaman)

fig = plt.figure(figsize=(12, 5))
sns.barplot(data=df_borrower_by_faculty_per_month, x='Tgl Pinjam', y='Banyak Pinjaman', hue='Fakultas', palette='bright')
plt.title('Banyak Pinjaman Berdasarkan Fakultas')
plt.xlabel('Bulan Peminjaman')
plt.xticks(rotation=0)

st.subheader('Jumlah Peminjaman Berdasarkan Fakultas Peminjam per Bulan')
st.pyplot(fig)

# Analisis Asosiasi
support = st.slider(
  label='Support',
  min_value=0.0,
  max_value=0.05,
  step=0.0001
)
st.write("Support:", support)

lift_threshold = st.slider(
  label='Lift Threshold',
  min_value=0,
  max_value=10,
)
st.write("Lift Threshold:", lift_threshold)
