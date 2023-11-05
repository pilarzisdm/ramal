import streamlit as st
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Load the CSV data
@st.cache
def load_data():
    data = pd.read_csv("ramal.csv")
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

    # Button to trigger forecasting
    if st.button("Forecast for November 1st"):
        if len(commodities) > 0:
            forecast_data = selected_data.copy()

            for commodity in commodities:
                # Use Exponential Smoothing to forecast prices for November 1st for each selected commodity
                last_date = forecast_data['Tanggal'].max()
                forecast_date = last_date + pd.DateOffset(1)  # Change this line to forecast for November 1st

                # Check if the forecast_date exists in the DataFrame
                if forecast_date in forecast_data['Tanggal'].values:
                    # Fit the Exponential Smoothing model and make a single-step forecast
                    model = ExponentialSmoothing(forecast_data[commodity], trend='add', seasonal='add', seasonal_periods=7)
                    model_fit = model.fit()
                    forecast_value = model_fit.forecast(steps=1)[0]

                    # Update the forecasted value for the selected commodity in the main DataFrame
                    forecast_data.loc[forecast_data['Tanggal'] == forecast_date, commodity] = forecast_value

            # Format the forecasted data to remove decimal places
            forecast_data = forecast_data.round(0)

            # Set the index and remove the index column
            forecast_data.set_index('Tanggal', inplace=True)

            # Display the forecasted data in the main content area
            st.subheader("Hasil Peramalan")
            st.dataframe(forecast_data.loc[forecast_date:forecast_date])
