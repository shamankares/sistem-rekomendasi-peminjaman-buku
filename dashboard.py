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
  pass

def create_transactions_df(df):
  pass

### MAIN PROGRAM
df_pinjaman = pd.read_csv('daftar-peminjaman-2022.csv')

# Visualisasi jumlah pinjaman berdasarkan tipe koleksi per bulan

# Visualisasi durasi pinjaman

# Visualisasi jumlah pinjaman berdasarkan fakultas peminjam per bulan

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
