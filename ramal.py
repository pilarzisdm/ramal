import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
@st.cache_data
def load_data():
    data = pd.read_csv("harga_real.csv")
    data['Tanggal'] = pd.to_datetime(data['Tanggal'])  # Parse the date column as datetime
    return data

# Sidebar: Select commodities
st.sidebar.title("Pilih Komoditas")
commodities = st.sidebar.multiselect("Pilih satu atau lebih komoditas", ["Beras", "Daging Ayam", "Telur Ayam", "Cabai Merah", "Cabai Rawit"])

# Main content
st.title("Peramalan Harga Komoditas Harian")

# Load data
data = load_data()

# Filter data based on selected commodities
if len(commodities) > 0:
    selected_data = data[['Tanggal'] + commodities]
    selected_data = selected_data.sort_values(by='Tanggal', ascending=False)

    st.subheader("Harga Komoditas")
    selected_data['Tanggal'] = selected_data['Tanggal'].dt.date  # Extract date portion
    st.write(selected_data.set_index('Tanggal'))

    # Add select box for granularity just for the plot
    granularity = st.selectbox("Pilih Granularitas Tanggal untuk Grafik", ["Harian", "Mingguan", "Bulanan"])

    # Determine granularity interval
    if granularity == "Mingguan":
        granularity_interval = 'W'
    elif granularity == "Bulanan":
        granularity_interval = 'M'
    else:
        granularity_interval = 'D'

    # Convert the index to DatetimeIndex
    selected_data['Tanggal'] = pd.to_datetime(selected_data['Tanggal'])
    selected_data.set_index('Tanggal', inplace=True)

    # Resample data for the selected granularity
    resampled_data = selected_data.resample(granularity_interval).last()

    # Plot selected commodities with the selected granularity
    st.subheader("Grafik Harga Komoditas")
    fig, ax = plt.subplots(figsize=(10, 5))

    for commodity in commodities:
        ax.plot(resampled_data.index, resampled_data[commodity], label=commodity)

    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Harga")
    ax.set_title("Harga Komoditas Antar Waktu")
    ax.legend()

    st.pyplot(fig)

    # Perform multi-day-ahead forecasting for selected commodities
    st.subheader("Peramalan Harga Komoditas untuk Hari Berikutnya")

    forecasting_period = st.number_input("Masukkan jumlah hari untuk peramalan:", min_value=1, step=1)

    if st.button("Forecast"):
        forecast_data = resampled_data.copy()

        for commodity in commodities:
            # Calculate the multi-day-ahead forecast using a rolling mean
            forecast_data[commodity + ' (Forecast)'] = forecast_data[commodity].rolling(window=forecasting_period).mean()

        # Display the forecasted data
        st.write(forecast_data.tail(forecasting_period))

else:
    st.warning("Silakan pilih satu atau lebih komoditas.")
