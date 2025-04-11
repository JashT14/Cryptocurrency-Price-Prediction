# import pandas as pd
# import numpy as np
# from xgboost import XGBRegressor
# from sklearn.metrics import mean_absolute_percentage_error
# import matplotlib.pyplot as plt
# from datetime import timedelta

# # 1. Load Data
# df = pd.read_csv('bitcoin_last_5_year.csv')
# df['Date'] = pd.to_datetime(df['Date'])

# # 2. Feature Engineering
# df['Return'] = df['Close'].pct_change()
# df['Lag_1'] = df['Close'].shift(1)
# df['Lag_2'] = df['Close'].shift(2)
# df['Lag_3'] = df['Close'].shift(3)
# df['SMA_diff'] = df['SMA_20'] - df['SMA_50']
# df.dropna(inplace=True)

# # 3. Prepare Data
# features = ['SMA_20', 'SMA_50', 'RSI', 'MACD', 'EMA_12', 'EMA_26',
#             'Return', 'Lag_1', 'Lag_2', 'Lag_3', 'SMA_diff']
# X = df[features]
# y = df['Close']

# # 4. Train Model
# model = XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=5)
# model.fit(X, y)

# # 5. Forecast Future Date
# def forecast_future_date(df, model, target_date):
#     last_known = df.copy()
#     current_date = last_known['Date'].max()
#     target_date = pd.to_datetime(target_date)

#     if target_date <= current_date:
#         return f"❌ Date {target_date.date()} is already in dataset. Please enter a future date."

#     while current_date < target_date:
#         last_row = last_known.iloc[-1]

#         # Prepare next date
#         next_date = current_date + timedelta(days=1)

#         # Create next row for prediction
#         row = {}
#         row['SMA_20'] = last_known['Close'].rolling(window=20).mean().iloc[-1]
#         row['SMA_50'] = last_known['Close'].rolling(window=50).mean().iloc[-1]
#         row['RSI'] = last_known['RSI'].iloc[-1]  # Assume RSI, MACD, etc. as constant (or retrain to remove)
#         row['MACD'] = last_known['MACD'].iloc[-1]
#         row['EMA_12'] = last_known['Close'].ewm(span=12, adjust=False).mean().iloc[-1]
#         row['EMA_26'] = last_known['Close'].ewm(span=26, adjust=False).mean().iloc[-1]
#         row['Return'] = (last_row['Close'] - last_known.iloc[-2]['Close']) / last_known.iloc[-2]['Close']
#         row['Lag_1'] = last_row['Close']
#         row['Lag_2'] = last_row['Lag_1']
#         row['Lag_3'] = last_row['Lag_2']
#         row['SMA_diff'] = row['SMA_20'] - row['SMA_50']

#         X_future = pd.DataFrame([row])
#         pred_close = model.predict(X_future)[0]

#         # Append predicted row
#         row['Date'] = next_date
#         row['Close'] = pred_close
#         last_known = pd.concat([last_known, pd.DataFrame([row])], ignore_index=True)

#         current_date = next_date

#     final_price = last_known[last_known['Date'] == target_date]['Close'].values[0]
#     return f"\n🔮 Predicted Bitcoin Price on {target_date.date()}: ${final_price:.2f}"

# # 6. Ask User for Future Date (Manual or Widget)
# user_date = input("📅 Enter a future date (YYYY-MM-DD): ").strip()
# print(forecast_future_date(df, model, user_date))

from flask import Flask, render_template, request
import pandas as pd
from xgboost import XGBRegressor
from datetime import timedelta

app = Flask(__name__)

# Load and preprocess data
df = pd.read_csv('bitcoin_last_5_year.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Return'] = df['Close'].pct_change()
df['Lag_1'] = df['Close'].shift(1)
df['Lag_2'] = df['Close'].shift(2)
df['Lag_3'] = df['Close'].shift(3)
df['SMA_diff'] = df['SMA_20'] - df['SMA_50']
df.dropna(inplace=True)

features = ['SMA_20', 'SMA_50', 'RSI', 'MACD', 'EMA_12', 'EMA_26',
            'Return', 'Lag_1', 'Lag_2', 'Lag_3', 'SMA_diff']
X = df[features]
y = df['Close']

# Train model
model = XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=5)
model.fit(X, y)

# Forecast function
def forecast_future_date(df, model, target_date):
    last_known = df.copy()
    current_date = last_known['Date'].max()
    target_date = pd.to_datetime(target_date)

    if target_date <= current_date:
        return f"❌ Date {target_date.date()} is already in dataset. Please enter a future date."

    while current_date < target_date:
        last_row = last_known.iloc[-1]

        next_date = current_date + timedelta(days=1)
        row = {
            'SMA_20': last_known['Close'].rolling(window=20).mean().iloc[-1],
            'SMA_50': last_known['Close'].rolling(window=50).mean().iloc[-1],
            'RSI': last_known['RSI'].iloc[-1],
            'MACD': last_known['MACD'].iloc[-1],
            'EMA_12': last_known['Close'].ewm(span=12, adjust=False).mean().iloc[-1],
            'EMA_26': last_known['Close'].ewm(span=26, adjust=False).mean().iloc[-1],
            'Return': (last_row['Close'] - last_known.iloc[-2]['Close']) / last_known.iloc[-2]['Close'],
            'Lag_1': last_row['Close'],
            'Lag_2': last_row['Lag_1'],
            'Lag_3': last_row['Lag_2'],
            'SMA_diff': last_known['Close'].rolling(window=20).mean().iloc[-1] - last_known['Close'].rolling(window=50).mean().iloc[-1]
        }

        X_future = pd.DataFrame([row])
        pred_close = model.predict(X_future)[0]

        row['Date'] = next_date
        row['Close'] = pred_close
        last_known = pd.concat([last_known, pd.DataFrame([row])], ignore_index=True)
        current_date = next_date

    final_price = last_known[last_known['Date'] == target_date]['Close'].values[0]
    return f"🔮 Predicted Bitcoin Price on {target_date.date()}: ${final_price:.2f}"

# Web Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        user_date = request.form['future_date']
        try:
            result = forecast_future_date(df, model, user_date)
        except Exception as e:
            result = f"⚠️ Error: {str(e)}"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
