import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt

# Load data from CSV files
df_station_hour = pd.read_csv("station_hour.csv")
stations = pd.read_csv("stations.csv")

# Merge station data with AQI data
df_station_hour = df_station_hour.merge(stations[['StationId']], on="StationId")

# Define AQI calculation formulas
# Simplified version for AQI calculation (average of all pollutants)
def calculate_AQI(row):
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NOx', 'NH3', 'CO', 'O3']
    sub_indices = [get_subindex(row[poll]) for poll in pollutants]
    return sum(sub_indices) / len(sub_indices)

# Define sub-index calculation function
def get_subindex(x):
    if x <= 50:
        return x
    elif x <= 100:
        return 50 + (x - 50) / 50 * 50
    elif x <= 200:
        return 100 + (x - 100) / 100 * 50
    elif x <= 300:
        return 200 + (x - 200) / 100 * 100
    elif x <= 400:
        return 300 + (x - 300) / 100 * 100
    else:
        return 400 + (x - 400) / 500 * 100

# Apply AQI calculation to station hour data
df_station_hour["AQI_calculated"] = df_station_hour.apply(calculate_AQI, axis=1)

# Drop rows with missing values
df_station_hour.dropna(inplace=True)

# Select features and target
X = df_station_hour[['PM2.5', 'PM10', 'SO2', 'NOx', 'NH3', 'CO', 'O3']]
y = df_station_hour['AQI_calculated']

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define and train the Random Forest model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_train_pred = model.predict(X_train)
y_val_pred = model.predict(X_val)

# Evaluate the model
train_mse = mean_squared_error(y_train, y_train_pred)
val_mse = mean_squared_error(y_val, y_val_pred)
train_r2 = r2_score(y_train, y_train_pred)
val_r2 = r2_score(y_val, y_val_pred)
print("Training MSE:", train_mse)
print("Validation MSE:", val_mse)
print("Training R^2:", train_r2)
print("Validation R^2:", val_r2)

# Save the model
joblib.dump(model, 'random_forest_model.pkl')

# Plot residuals
train_residuals = y_train - y_train_pred
val_residuals = y_val - y_val_pred

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.scatter(y_train_pred, train_residuals, color='blue', label='Training Data')
plt.xlabel('Predicted AQI')
plt.ylabel('Residuals')
plt.title('Training Residuals')
plt.axhline(y=0, color='r', linestyle='-')
plt.legend()

plt.subplot(1, 2, 2)
plt.scatter(y_val_pred, val_residuals, color='green', label='Validation Data')
plt.xlabel('Predicted AQI')
plt.ylabel('Residuals')
plt.title('Validation Residuals')
plt.axhline(y=0, color='r', linestyle='-')
plt.legend()

plt.tight_layout()
plt.show()
