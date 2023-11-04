import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA

# Load the CSV data
@st.cache_data
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
    st.sidebar.subheader("Peramalan Harga Komoditas untuk Hari Mendatang")
    forecasting_days = st.sidebar.number_input("Masukkan jumlah hari untuk peramalan:", min_value=1, step=1)

    if st.sidebar.button("Forecast"):
        if len(commodities) > 0:
            forecast_data = selected_data.copy()

            for commodity in commodities:
                # Prepare data for ARIMA
                df = forecast_data[['Tanggal', commodity]].copy()
                df.set_index('Tanggal', inplace=True)

                # Fit ARIMA model
                model = ARIMA(df, order=(5, 1, 0))  # You can adjust the order based on your data and requirements
                model_fit = model.fit()

                # Make future forecasts
                forecast_values = model_fit.forecast(steps=forecasting_days)

                # Create date range for forecasting period
                last_date = df.index.max()
                forecast_dates = pd.date_range(start=last_date + pd.DateOffset(1), periods=forecasting_days)

                # Create a DataFrame for the forecasted data
                forecast_df = pd.DataFrame({commodity: forecast_values}, index=forecast_dates)

                # Concatenate the forecasted data to the original data
                forecast_data = pd.concat([forecast_data, forecast_df])

            # Display the forecasted data in the main content area
            st.subheader("Hasil Peramalan")
            st.write(forecast_data.tail(forecasting_days)[commodities])
