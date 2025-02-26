import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency

# Set Seaborn style
sns.set(style='dark')

def load_data(file_path):
    """Load the dataset from a CSV file."""
    return pd.read_csv(file_path, sep=';')

def preprocess_data(df):
    """Preprocess the DataFrame to convert columns to numeric and handle missing values."""
    # Convert necessary columns to numeric
    df[['year', 'month', 'day', 'hour']] = df[['year', 'month', 'day', 'hour']].apply(pd.to_numeric, errors='coerce')
    df.dropna(subset=['year', 'month', 'day', 'hour'], inplace=True)
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df.set_index('datetime', inplace=True)
    return df

def plot_monthly_pm25(df):
    """Plot the monthly average of PM2.5 concentration."""
    df['PM2.5'] = pd.to_numeric(df['PM2.5'], errors='coerce')
    df.dropna(subset=['PM2.5'], inplace=True)
    monthly_pm25 = df['PM2.5'].resample('ME').mean()

    fig, ax = plt.subplots(figsize=(15, 6))
    monthly_pm25.plot(title='Rata-rata Bulanan PM2.5', xlabel='Tanggal', ylabel='Konsentrasi PM2.5', ax=ax)
    ax.axhline(y=75, color='r', linestyle='--', label='Ambang Batas (75 µg/m³)')
    ax.legend()
    st.pyplot(fig)

def plot_so2_distribution(df):
    """Plot the distribution of SO2 concentration."""
    df['SO2'] = pd.to_numeric(df['SO2'], errors='coerce')
    df.dropna(subset=['SO2'], inplace=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    df['SO2'].hist(bins=30, color='skyblue', edgecolor='black', ax=ax)
    ax.set_title('Distribusi Konsentrasi SO2')
    ax.set_xlabel('Konsentrasi SO2 (µg/m³)')
    ax.set_ylabel('Frekuensi')
    ax.grid(axis='y')
    st.pyplot(fig)

    extreme_so2 = df[df['SO2'] > df['SO2'].quantile(0.95)][['SO2']].reset_index()
    if not extreme_so2.empty:
        st.write("### Nilai Ekstrim SO2 (di atas 95th percentile):")
        st.dataframe(extreme_so2)
    else:
        st.write("Tidak ada nilai ekstrim SO2 yang ditemukan.")

def plot_co_pm10_relationship(df):
    """Plot the relationship between CO and PM10 concentrations."""
    df['CO'] = pd.to_numeric(df['CO'], errors='coerce')
    df['PM10'] = pd.to_numeric(df['PM10'], errors='coerce')
    df.dropna(subset=['CO', 'PM10'], inplace=True)

    plt.figure(figsize=(10, 6))
    plt.scatter(df['CO'], df['PM10'], alpha=0.5, color='green')
    plt.title('Hubungan antara Konsentrasi CO dan PM10')
    plt.xlabel('Konsentrasi CO (µg/m³)')
    plt.ylabel('Konsentrasi PM10 (µg/m³)')
    plt.grid()
    st.pyplot(plt)

    correlation = df['CO'].corr(df['PM10'])
    st.write(f"Koefisien Korelasi antara CO dan PM10: {correlation:.2f}")

def count_exceeding_pm25(df, cities, years):
    """Count days with PM2.5 exceeding the threshold for specified cities and years."""
    filtered_df = df[(df.index.year.isin(years)) & (df['station'].isin(cities))]
    exceeding_days = filtered_df[filtered_df['PM2.5'] > 75]
    total_exceeding_days = exceeding_days.groupby(exceeding_days.index.date).size().count()
    st.write(f"Total hari PM2.5 di atas ambang batas (75 µg/m³) di {', '.join(cities)} selama {years[0]} - {years[-1]}: {total_exceeding_days}")

def main():
    st.header("# Dashboard Analisis Air Quality")

    all_df = load_data("merged_data.csv")
    st.dataframe(all_df.describe())

    all_df = preprocess_data(all_df)

    st.header("Pertanyaan 1: Bagaimana tren bulanan rata-rata konsentrasi PM2.5 selama periode pengamatan?")
    plot_monthly_pm25(all_df)

    st.header("Pertanyaan 2: Apa distribusi konsentrasi SO2 dan bagaimana nilai-nilai ekstrimnya?")
    plot_so2_distribution(all_df)

    st.header("Pertanyaan 3: Apakah ada hubungan antara konsentrasi CO dan PM10?")
    plot_co_pm10_relationship(all_df)

    st.header("Pertanyaan 4: Di kota Changping dan Dingling selama satu tahun terakhir, berapa PM2.5 di atas ambang batas?")
    count_exceeding_pm25(all_df, cities=['Changping', 'Dingling'], years=[2016, 2017])

if __name__ == "__main__":
    main()
