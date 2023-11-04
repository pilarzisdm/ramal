import pandas as pd

# Load your data from the CSV file
data = pd.read_csv("ramal.csv")

# Assuming the date column in your CSV is named 'Tanggal'
# First, make sure 'Tanggal' is in datetime format
data['Tanggal'] = pd.to_datetime(data['Tanggal'])

# Find the last date in the data series
last_date = data['Tanggal'].max()

# Calculate the next day
next_day = last_date + pd.DateOffset(1)

# Print the next day
print("Next day after the last date:", next_day)
