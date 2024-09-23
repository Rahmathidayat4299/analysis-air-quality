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