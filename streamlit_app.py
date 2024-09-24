import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='dark')
st.header(
    """#Dashboard Analisis Air Quality"""
)

all_df = pd.read_csv("merged_data.csv",sep=';')
print(all_df.describe())
# Display the data as a table in Streamlit
st.dataframe(all_df)
st.header("Pertanyaan 1:Bagaimana tren bulanan rata-rata konsentrasi PM2.5 selama periode pengamatan?")
# Ensure all required columns are numeric
all_df[['year', 'month', 'day', 'hour']] = all_df[['year', 'month', 'day', 'hour']].apply(pd.to_numeric, errors='coerce')

# Drop rows with NaN in the required columns
all_df.dropna(subset=['year', 'month', 'day', 'hour'], inplace=True)

# Create datetime column
all_df['datetime'] = pd.to_datetime(all_df[['year', 'month', 'day', 'hour']])

# Set datetime as index
all_df.set_index('datetime', inplace=True)

# Convert PM2.5 column to numeric, forcing errors to NaN
all_df['PM2.5'] = pd.to_numeric(all_df['PM2.5'], errors='coerce')

# Drop rows where PM2.5 is NaN
all_df.dropna(subset=['PM2.5'], inplace=True)

# Calculate monthly average of PM2.5
monthly_pm25 = all_df['PM2.5'].resample('ME').mean()

# Display the title in Streamlit
st.write("# Rata-rata Bulanan PM2.5")

# Create the plot
fig, ax = plt.subplots(figsize=(15, 6))
monthly_pm25.plot(title='Rata-rata Bulanan PM2.5', xlabel='Tanggal', ylabel='Konsentrasi PM2.5', ax=ax)
ax.axhline(y=75, color='r', linestyle='--', label='Ambang Batas (75 µg/m³)')
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)
# Ensure SO2 is numeric
st.header("Pertanyaan 2: Apa distribusi konsentrasi SO2 dan bagaimana nilai-nilai ekstrimnya?")
all_df['SO2'] = pd.to_numeric(all_df['SO2'], errors='coerce')

# Drop rows where SO2 is NaN
all_df.dropna(subset=['SO2'], inplace=True)

# Check if year, month, day, hour columns exist for datetime creation
required_columns = ['year', 'month', 'day', 'hour']
if all(col in all_df.columns for col in required_columns):
    try:
        # Create datetime column
        all_df['datetime'] = pd.to_datetime(all_df[['year', 'month', 'day', 'hour']], errors='coerce')
        all_df.dropna(subset=['datetime'], inplace=True)  # Drop rows with NaT
    except Exception as e:
        st.error(f"Error creating datetime: {e}")
else:
    st.error("Year, month, day, and hour columns are required for datetime creation.")

# Set datetime as index if available
if 'datetime' in all_df.columns:
    all_df.set_index('datetime', inplace=True)

# Create a histogram for SO2 distribution
st.write("# Distribusi Konsentrasi SO2")
fig, ax = plt.subplots(figsize=(10, 6))
all_df['SO2'].hist(bins=30, color='skyblue', edgecolor='black', ax=ax)
ax.set_title('Distribusi Konsentrasi SO2')
ax.set_xlabel('Konsentrasi SO2 (µg/m³)')
ax.set_ylabel('Frekuensi')
ax.grid(axis='y')

# Display the histogram in Streamlit
st.pyplot(fig)

# Identify extreme values of SO2
extreme_so2 = all_df[all_df['SO2'] > all_df['SO2'].quantile(0.95)][['SO2']].reset_index()

# Display extreme SO2 values
if not extreme_so2.empty:
    st.write("### Nilai Ekstrim SO2 (di atas 95th percentile):")
    st.dataframe(extreme_so2)
else:
    st.write("Tidak ada nilai ekstrim SO2 yang ditemukan.")

######
##pertanyaan 3
st.header("Pertanyaan3:Apakah ada hubungan antara konsentrasi CO dan PM10?")
# Ensure CO and PM10 columns are numeric
all_df['CO'] = pd.to_numeric(all_df['CO'], errors='coerce')
all_df['PM10'] = pd.to_numeric(all_df['PM10'], errors='coerce')

# Drop NaN values
all_df.dropna(subset=['CO', 'PM10'], inplace=True)

# Create scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(all_df['CO'], all_df['PM10'], alpha=0.5, color='green')
plt.title('Hubungan antara Konsentrasi CO dan PM10')
plt.xlabel('Konsentrasi CO (µg/m³)')
plt.ylabel('Konsentrasi PM10 (µg/m³)')
plt.grid()

# Display the plot in Streamlit
st.pyplot(plt)

# Calculate and display correlation coefficient
correlation = all_df['CO'].corr(all_df['PM10'])
st.write(f"Koefisien Korelasi antara CO dan PM10: {correlation:.2f}")
#####
st.header("Pertanyaan 4 : di kota Changping dan Dingling selama satu tahun terakhir berapa PM 2.5 diatas ambang batas ?")
# Ensure all required columns are numeric
all_df[['year', 'month', 'day', 'hour']] = all_df[['year', 'month', 'day', 'hour']].apply(pd.to_numeric, errors='coerce')

# Drop rows with NaN in the required columns
all_df.dropna(subset=['year', 'month', 'day', 'hour'], inplace=True)

# Create datetime column
all_df['datetime'] = pd.to_datetime(all_df[['year', 'month', 'day', 'hour']])

# Set datetime as index
all_df.set_index('datetime', inplace=True)

# Filter data for the years 2016 and 2017 and the desired cities
filtered_df = all_df[(all_df.index.year.isin([2016, 2017])) & (all_df['station'].isin(['Changping', 'Dingling']))]

# Count the number of days where PM2.5 exceeds the threshold
exceeding_days = filtered_df[filtered_df['PM2.5'] > 75]

# Group by date and count the number of days
result = exceeding_days.groupby(exceeding_days.index.date).size()

# Total number of days exceeding the threshold
total_exceeding_days = result.count()

# Display the result in Streamlit
st.write(f"Total hari PM2.5 di atas ambang batas (75 µg/m³) di Changping dan Dingling selama 2016 - 2017: {total_exceeding_days}")

# Plotting PM2.5 levels
plt.figure(figsize=(15, 6))
plt.plot(filtered_df.index, filtered_df['PM2.5'], label='PM2.5 Levels', color='blue')
plt.axhline(y=75, color='r', linestyle='--', label='Ambang Batas (75 µg/m³)')
plt.title('PM2.5 Levels in Changping and Dingling (2016-2017)')
plt.xlabel('Tanggal')
plt.ylabel('Konsentrasi PM2.5 (µg/m³)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.legend()

# Display the plot in Streamlit
st.pyplot(plt)
#####
# Display the title in Streamlit
st.write("# Rata-rata Bulanan PM2.5")

# Create the plot
fig, ax = plt.subplots(figsize=(15, 6))
monthly_pm25.plot(title='Rata-rata Bulanan PM2.5', xlabel='Tanggal', ylabel='Konsentrasi PM2.5', ax=ax)
ax.axhline(y=75, color='r', linestyle='--', label='Ambang Batas (75 µg/m³)')
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)


# Optionally, if you want to display summary statistics in Streamlit:
st.write("## Descriptive Statistics")
st.table(all_df.describe())


# Ensure that selected columns are numeric by forcing non-numeric values to NaN
columns_to_plot = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

# Clean and convert columns to numeric, replacing non-numeric entries with NaN
for column in columns_to_plot:
    if column in all_df.columns:
        all_df[column] = pd.to_numeric(all_df[column], errors='coerce')  # Convert to numeric
    else:
        st.warning(f"Column {column} not found in the dataset.")

# Display title
st.write("# Dashboard Analisis Air Quality")

# Create histograms for each column in the list
st.write("## Histograms of Air Quality Parameters")
for column in columns_to_plot:
    if column in all_df.columns:
        clean_data = all_df[column].dropna()  # Drop NaN values before plotting

        if not clean_data.empty:
            fig, ax = plt.subplots()
            sns.histplot(clean_data, bins=30, kde=True, ax=ax)  # Plot the histogram
            ax.set_title(f"Histogram of {column}")
            st.pyplot(fig)  # Display the plot in Streamlit
        else:
            st.write(f"No valid data available to plot for {column}")
    else:
        st.write(f"{column} is not present in the data.")

# Optionally, display the cleaned DataFrame
st.write("## Cleaned Data Sample")
st.dataframe(all_df.head())

# Ensure the columns are numeric where necessary
all_df[['year', 'month', 'day', 'hour']] = all_df[['year', 'month', 'day', 'hour']].apply(pd.to_numeric, errors='coerce')

# Drop rows with NaN in the required columns
all_df.dropna(subset=['year', 'month', 'day', 'hour'], inplace=True)

# Create a 'datetime' column by combining year, month, day, and hour
all_df['datetime'] = pd.to_datetime(all_df[['year', 'month', 'day', 'hour']])

# Set 'datetime' as the index
all_df.set_index('datetime', inplace=True)

# Resample the data to monthly averages and plot
monthly_avg = all_df[['PM2.5', 'PM10', 'SO2', 'NO2']].resample('M').mean()

# Streamlit app: Displaying the plot
st.write("# Monthly Average of Air Quality Indicators")

# Create the figure and axis
fig, ax = plt.subplots(figsize=(15, 6))
monthly_avg.plot(ax=ax)

# Customize the plot
ax.set_title('Monthly Average of Air Quality Indicators')
ax.set_xlabel('Date')
ax.set_ylabel('Concentration')
ax.legend(title='Pollutants')

# Display the plot in Streamlit
st.pyplot(fig)