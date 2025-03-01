import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='dark')

def load_data(file_path):
    return pd.read_csv(file_path, sep=';')

def preprocess_data(df):
    df[['year', 'month', 'day', 'hour']] = df[['year', 'month', 'day', 'hour']].apply(pd.to_numeric, errors='coerce')
    df.dropna(subset=['year', 'month', 'day', 'hour'], inplace=True)
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df.set_index('datetime', inplace=True)
    return df

def filter_data(df, start_date, end_date, stations):
    df_filtered = df[(df.index >= start_date) & (df.index <= end_date)]
    if stations:
        df_filtered = df_filtered[df_filtered['station'].isin(stations)]
    return df_filtered

def plot_monthly_pm25(df):
    df['PM2.5'] = pd.to_numeric(df['PM2.5'], errors='coerce')
    df.dropna(subset=['PM2.5'], inplace=True)
    monthly_pm25 = df['PM2.5'].resample('ME').mean()
    fig, ax = plt.subplots(figsize=(15, 6))
    monthly_pm25.plot(title='Rata-rata Bulanan PM2.5', xlabel='Tanggal', ylabel='Konsentrasi PM2.5', ax=ax)
    ax.axhline(y=75, color='r', linestyle='--', label='Ambang Batas (75 µg/m³)')
    ax.legend()
    st.pyplot(fig)

def main():
    st.header("# Dashboard Analisis Air Quality")
    all_df = load_data("merged_data.csv")
    all_df = preprocess_data(all_df)
    
    # Sidebar untuk interaktif
    st.sidebar.header("Filter Data")
    start_date = st.sidebar.date_input("Mulai Tanggal", value=all_df.index.min().date())
    end_date = st.sidebar.date_input("Akhir Tanggal", value=all_df.index.max().date())
    stations = st.sidebar.multiselect("Pilih Stasiun", options=all_df['station'].unique())
    
    filtered_df = filter_data(all_df, pd.to_datetime(start_date), pd.to_datetime(end_date), stations)
    st.dataframe(filtered_df.describe())
    
    st.header("Tren Bulanan PM2.5")
    plot_monthly_pm25(filtered_df)

if __name__ == "__main__":
    main()