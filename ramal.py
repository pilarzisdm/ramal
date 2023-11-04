import streamlit as st
import pandas as pd

# Load the CSV data
@st.cache_data
def load_data():
    data = pd.read_csv("harga_real.csv")
    data['Tanggal'] = pd.to_datetime(data['Tanggal'])  # Parse the date column as datetime
    return data

# Main content
st.title("Next Day Forecast")

# Load data
data = load_data()

# Get the last date in the dataset
last_date = data['Tanggal'].max()

# Calculate the next day
next_day = last_date + pd.DateOffset(days=1)

st.write("Last Date:", last_date.date())
st.write("Next Day:", next_day.date())
