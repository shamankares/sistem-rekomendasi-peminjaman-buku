import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def create_collection_types_per_month_df(df):
  pinjaman_bulanan_by_tipe_koleksi = df.groupby([pd.Grouper(key='Tgl Pinjam', freq='M'), 'Tipe Koleksi'],)['Nomor Buku'].nunique().unstack(fill_value=0)
  pinjaman_bulanan_by_tipe_koleksi.index = pinjaman_bulanan_by_tipe_koleksi.index.month_name()
  return pinjaman_bulanan_by_tipe_koleksi.reset_index().melt(id_vars='Tgl Pinjam', var_name='Tipe Koleksi', value_name='Banyak Pinjaman')

def create_borrow_duration_df(df):
  lama_peminjaman = (df['Tgl Kembali'] - df['Tgl Pinjam']).dt.days
  return lama_peminjaman

def create_borrower_by_faculty_per_month_df(df):
  pinjaman_bulanan_by_fakultas = df.groupby([pd.Grouper(key='Tgl Pinjam', freq='M'), 'Fakultas Pemustaka'])['Nomor Buku'].count().unstack(fill_value=0)
  pinjaman_bulanan_by_fakultas.index = pinjaman_bulanan_by_fakultas.index.month_name()
  return pinjaman_bulanan_by_fakultas.reset_index().melt(id_vars='Tgl Pinjam', var_name='Fakultas', value_name='Banyak Pinjaman')

def create_transactions_df(df):
  return df.groupby(by=['Nama Pemustaka', 'Tgl Pinjam', 'Judul Buku'])['Jumlah'].count().unstack(2).reset_index(['Nama Pemustaka', 'Tgl Pinjam'], drop=True).fillna(0).map(lambda x: bool(x))

def create_support_df(df, support):
  if support == 0.0:
    support = 0

  freq = apriori(df, min_support=support, use_colnames=True)
  return freq

def create_association_by_lift_df(df_freq, lift_threshold):
  assoc = association_rules(df_freq, metric='lift', min_threshold=lift_threshold)
  return assoc

def create_recommendations(assoc_df, book):
  return assoc_df[assoc_df['antecedents'] == frozenset({book})]['consequents'].explode().unique()

### MAIN PROGRAM
df_pinjaman = pd.read_csv('daftar-peminjaman-2022.csv')

# Ubah tipe data kolom Tgl Pinjam dan Tgl Kembali menjadi datetime untuk visualisasi
kolom_tgl = ['Tgl Pinjam', 'Tgl Kembali']

for kolom in kolom_tgl:
    df_pinjaman[kolom] = pd.to_datetime(df_pinjaman[kolom], format='%Y-%m-%d', errors='coerce')

st.header('Sistem Rekomendasi Peminjaman Buku :book:')

# Visualisasi jumlah pinjaman berdasarkan tipe koleksi per bulan
df_borrow_by_tipe_koleksi_per_month = create_collection_types_per_month_df(df_pinjaman)

fig = plt.figure(figsize=(12, 5))
sns.barplot(data=df_borrow_by_tipe_koleksi_per_month, x='Tgl Pinjam', y='Banyak Pinjaman', hue='Tipe Koleksi', palette='bright')
plt.title('Banyak Pinjaman Berdasarkan Tipe Koleksi')
plt.xlabel('Bulan Peminjaman')
plt.xticks(rotation=0)

st.subheader('Jumlah Pinjaman Berdasarkan Tipe Koleksi per Bulan')
st.pyplot(fig)

# Visualisasi durasi pinjaman
df_borrow_duration = create_borrow_duration_df(df_pinjaman)

fig = plt.figure(figsize=(12, 20))
sns.boxplot(y=df_borrow_duration)
plt.title('Lama Peminjaman')

st.subheader('Durasi Peminjaman')
st.pyplot(fig)

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
st.subheader('Analisis Asosiasi')

daftar_fakultas = df_pinjaman['Fakultas Pemustaka'].unique()
daftar_fakultas = np.insert(daftar_fakultas, 0, 'Semua')
fakultas = st.selectbox('Pilih fakultas:', daftar_fakultas)
df_pinjaman_fakultas = df_pinjaman if fakultas == 'Semua' else df_pinjaman[df_pinjaman['Fakultas Pemustaka'] == fakultas]

support = st.slider(
  label='Support',
  min_value=0.001,
  max_value=0.050,
  step=0.0001,
  format="%4f"
)
df_transaksi = create_transactions_df(df_pinjaman_fakultas)
df_freq = create_support_df(df_transaksi, support)
st.dataframe(df_freq, use_container_width=True)

lift_threshold = st.slider(
  label='Lift Threshold',
  min_value=1.0,
  max_value=5.0,
  step=0.1,
)
assc_by_lift_df = create_association_by_lift_df(df_freq, lift_threshold)
st.dataframe(assc_by_lift_df, use_container_width=True)

# Rekomendasi Peminjaman
st.subheader('Rekomendasi Peminjaman')

buku = st.selectbox('Judul buku:', df_transaksi.columns)
st.write('Rekomendasi buku:')
st.dataframe(create_recommendations(assc_by_lift_df, buku), use_container_width=True)
