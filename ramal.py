import streamlit as st
import pandas as pd
import numpy as np

# Load the CSV data
@st.cache
def load_data():
    data = pd.read_csv("harga_real.csv")
    data['Tanggal'] = pd.to_datetime(data['Tanggal'])  # Parse the date column as datetime
    return data

# Sidebar: Select commodities
st.sidebar.title("Pilih Komoditas")
commodities = st.sidebar.multiselect("Pilih satu atau lebih komoditas", ["Beras", "Daging Ayam", "Telur Ayam", "Cabai Merah", "Cabai Rawit"])

# Main content area
st.title("Peramalan Harga Komoditas Harian")

if len(commodities) > 0:
    # Load data when commodities are selected
    data = load_data()

    # Filter data based on selected commodities
    selected_data = data[['Tanggal'] + commodities]
    selected_data = selected_data.sort_values(by='Tanggal', ascending=False)

    # Display the data table for selected commodities
    st.subheader("Harga Komoditas")
    selected_data['Tanggal'] = selected_data['Tanggal'].dt.date  # Extract date portion
    st.write(selected_data.set_index('Tanggal'))

    # Sidebar: Input for forecasting
    st.sidebar.subheader("Peramalan Harga Komoditas")
    forecasting_days = st.sidebar.number_input("Masukkan jumlah hari untuk peramalan:", min_value=1, step=1)

    if st.sidebar.button("Forecast"):
        if len(commodities) > 0:
            forecast_data = selected_data.copy()

            for commodity in commodities:
                # Calculate the Simple Moving Average (SMA) for the commodity
                forecast_data[commodity + '_SMA'] = forecast_data[commodity].rolling(window=7).mean()

                # Use the SMA to forecast future values for each selected commodity
                last_date = forecast_data['Tanggal'].max()

                # Create forecast values as an array
                forecast_values = np.array([forecast_data[commodity + '_SMA'].iloc[-1]] * forecasting_days)

                # Create date range starting from the next day after the last date in the data
                forecast_dates = pd.date_range(start=last_date + pd.DateOffset(1), periods=forecasting_days)

                # Create a DataFrame for the forecasted commodity values
                forecast_df = pd.DataFrame({commodity: forecast_values}, index=forecast_dates)

                # Update the forecasted values for the selected commodity in the main DataFrame
                forecast_data[commodity].iloc[-forecasting_days:] = forecast_values

                # Remove the duplicate columns (commodity + '_SMA')
                forecast_data = forecast_data.drop(columns=[commodity + '_SMA'])

            # Display the forecasted data in the main content area
            st.subheader("Hasil Peramalan")
            st.write(forecast_data.tail(forecasting_days))
