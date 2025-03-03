import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style
sns.set(style='dark')

@st.cache_data
def load_data(file_path):
    """Load dataset with optimized memory usage."""
    df = pd.read_csv(file_path, sep=';', low_memory=False)
    numeric_cols = ['year', 'month', 'day', 'hour', 'PM2.5', 'PM10', 'SO2', 'CO']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df.dropna(subset=['year', 'month', 'day', 'hour'], inplace=True)
    df['station'] = df['station'].astype(str)
    return df

@st.cache_data
def preprocess_data(df):
    """Preprocess DataFrame to ensure a clean datetime index."""
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']], errors='coerce')
    df.dropna(subset=['datetime'], inplace=True)
    df.set_index('datetime', inplace=True)
    df = df[~df.index.duplicated(keep='first')]
    df.sort_index(inplace=True)
    return df

def plot_monthly_pm25(df):
    """Plot the monthly average of PM2.5 concentration."""
    monthly_pm25 = df['PM2.5'].resample('M').mean()
    fig, ax = plt.subplots(figsize=(15, 6))
    monthly_pm25.plot(ax=ax, color='b', marker='o')
    ax.set_title('Rata-rata Bulanan PM2.5')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Konsentrasi PM2.5 (µg/m³)')
    ax.axhline(y=75, color='r', linestyle='--', label='Ambang Batas (75 µg/m³)')
    ax.legend()
    st.pyplot(fig)

def plot_so2_distribution(df):
    """Plot the distribution of SO2 concentration."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['SO2'].dropna(), bins=30, kde=True, color='skyblue', ax=ax)
    ax.set_title('Distribusi Konsentrasi SO2')
    ax.set_xlabel('Konsentrasi SO2 (µg/m³)')
    ax.set_ylabel('Frekuensi')
    ax.grid(axis='y')
    st.pyplot(fig)

def plot_co_pm10_relationship(df):
    """Plot the relationship between CO and PM10 concentrations."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=df['CO'], y=df['PM10'], alpha=0.5, color='green', ax=ax)
    ax.set_title('Hubungan antara Konsentrasi CO dan PM10')
    ax.set_xlabel('Konsentrasi CO (µg/m³)')
    ax.set_ylabel('Konsentrasi PM10 (µg/m³)')
    ax.grid()
    st.pyplot(fig)
    
    correlation = df['CO'].corr(df['PM10'])
    st.write(f"Koefisien Korelasi antara CO dan PM10: {correlation:.2f}")

def count_exceeding_pm25(df, cities, start_date, end_date):
    """Count days with PM2.5 exceeding threshold within user-selected dates."""
    df_filtered = df[df['station'].isin(cities)].loc[start_date:end_date]
    exceeding_days = df_filtered[df_filtered['PM2.5'] > 75].resample('D').size().count()
    st.write(f"Total hari PM2.5 di atas ambang batas di {', '.join(cities)} dari {start_date.date()} hingga {end_date.date()}: **{exceeding_days} hari**")

def main():
    st.title("🌍 Dashboard Analisis Kualitas Udara")
    
    all_df = load_data("merged_data.csv")
    all_df = preprocess_data(all_df)
    
    st.write("### Statistik Data")
    st.dataframe(all_df.describe())
    
    st.header("1️⃣ Tren Bulanan Rata-rata Konsentrasi PM2.5")
    plot_monthly_pm25(all_df)
    
    st.header("2️⃣ Distribusi Konsentrasi SO2 dan Nilai Ekstrim")
    plot_so2_distribution(all_df)
    
    st.header("3️⃣ Hubungan antara Konsentrasi CO dan PM10")
    plot_co_pm10_relationship(all_df)
    
    st.header("4️⃣ Hitung Hari PM2.5 Melebihi Ambang Batas")
    
    city_options = sorted(all_df['station'].unique().tolist())
    
    # Pastikan Dingling selalu ada dalam daftar opsi
    if 'Dingling' not in city_options:
        city_options.append('Dingling')
    
    default_options = [city for city in ['Dingling', 'Changping'] if city in city_options]
    
    selected_cities = st.multiselect(
        label="Pilih kota:", 
        options=city_options,
        default=default_options
    )
    
    start_date = st.date_input("Pilih tanggal mulai:", value=pd.to_datetime("2016-01-01").date())
    end_date = st.date_input("Pilih tanggal akhir:", value=pd.to_datetime("2017-12-31").date())
    
    if start_date > end_date:
        st.error("Tanggal mulai harus lebih awal dari tanggal akhir!")
    elif selected_cities:
        count_exceeding_pm25(all_df, selected_cities, pd.to_datetime(start_date), pd.to_datetime(end_date))

if __name__ == "__main__":
    main()
