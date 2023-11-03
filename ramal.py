import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error


# Load historical data
@st.cache_data
def load_data():
    data = pd.read_csv("harga_real.csv")
    return data

data = load_data()

# User selects a commodity to forecast
commodity_choice = st.selectbox("Select Commodity", data.columns[1:])  # Assuming the first column is "Date"

# Split data into training and testing sets
X = data.drop(columns=["Tanggal", commodity_choice])
y = data[commodity_choice]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# User selects forecasting model
model_choice = st.selectbox("Select Forecasting Model", ["Random Forest", "ARIMA", "Exponential Smoothing", "Moving Average"])

# User specifies the number of periods to forecast
forecast_periods = st.text_input("Enter the number of periods to forecast:", 1)  # Default to 1 period

if model_choice == "Random Forest":
    # Train a Random Forest model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    # Make predictions
    predictions = model.predict(X_test)

elif model_choice == "ARIMA":
    # Train an ARIMA model
    model = ARIMA(y_train, order=(5, 1, 0))
    model = model.fit(disp=0)
    # Make predictions
    predictions = model.forecast(steps=int(forecast_periods), alpha=0.05)

elif model_choice == "Exponential Smoothing":
    # Train an Exponential Smoothing model
    model = ExponentialSmoothing(y_train, trend='add', seasonal='add', seasonal_periods=12)
    model = model.fit()
    # Make predictions
    predictions = model.forecast(int(forecast_periods))

else:
    # Use Moving Average for forecasting
    predictions = y_train.rolling(window=12).mean().iloc[-1]  # Use a simple 12-month moving average for forecasting

# Model evaluation
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)

st.title("Market Prices Forecasting")

st.write("## Historical Data")
st.write(data)

st.write(f"## Forecasting for {commodity_choice}")
st.write(f"### Model: {model_choice}")
st.write(f"### Forecasting Periods: {forecast_periods} periods")
st.write(f"#### Model Evaluation")
st.write(f"Mean Absolute Error (MAE): {mae}")
st.write(f"Mean Squared Error (MSE): {mse}")
st.write(f"Root Mean Squared Error (RMSE): {rmse}")

st.write("#### Model Predictions")
st.write(predictions)

st.write("#### Actual vs. Predicted Data")
comparison_data = pd.DataFrame({'Actual': y_test, 'Predicted': predictions})
st.write(comparison_data)

st.line_chart(predictions)

# Optionally, you can plot historical vs. predicted data
plt.figure(figsize=(10, 6))
plt.plot(y_test, label='Historical Data')
plt.plot(predictions, label='Predictions')
plt.legend()
st.pyplot(plt)
