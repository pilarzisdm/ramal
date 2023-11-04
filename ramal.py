import pandas as pd

# Assuming your data is in a DataFrame called 'data' and the date column is 'Tanggal'
# First, make sure 'Tanggal' is in datetime format
data['Tanggal'] = pd.to_datetime(data['Tanggal'])

# Find the last date in the data series
last_date = data['Tanggal'].max()

# Calculate the next day
next_day = last_date + pd.DateOffset(1)

# Print the next day
print("Next day after the last date:", next_day)