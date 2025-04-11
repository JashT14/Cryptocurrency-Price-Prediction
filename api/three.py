from flask import Flask, render_template, request
import pandas as pd
from xgboost import XGBRegressor
from datetime import timedelta

app = Flask(__name__)

# Load and preprocess historical data
df = pd.read_csv('ethereum_last_1_year.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Feature Engineering
df['Return'] = df['Close'].pct_change()
df['Lag_1'] = df['Close'].shift(1)
df['Lag_2'] = df['Close'].shift(2)
df['Lag_3'] = df['Close'].shift(3)
df['SMA_20'] = df['Close'].rolling(window=20).mean()
df['SMA_50'] = df['Close'].rolling(window=50).mean()
df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
df['SMA_diff'] = df['SMA_20'] - df['SMA_50']

# Assume RSI and MACD are already present, otherwise forward-fill or mock
df['RSI'] = df['RSI'].ffill()
df['MACD'] = df['MACD'].ffill()

df.dropna(inplace=True)

# Prepare model inputs
features = ['SMA_20', 'SMA_50', 'RSI', 'MACD', 'EMA_12', 'EMA_26',
            'Return', 'Lag_1', 'Lag_2', 'Lag_3', 'SMA_diff']
X = df[features]
y = df['Close']

# Train XGBoost model
model = XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=5)
model.fit(X, y)

# Forecast function
def forecast_future_date(df, model, target_date):
    target_date = pd.to_datetime(target_date)
    last_known = df.copy()
    current_date = last_known['Date'].max()

    if target_date <= current_date:
        return f"❌ Date {target_date.date()} is already in the dataset."

    while current_date < target_date:
        # Recalculate indicators
        last_known['Return'] = last_known['Close'].pct_change()
        last_known['Lag_1'] = last_known['Close'].shift(1)
        last_known['Lag_2'] = last_known['Close'].shift(2)
        last_known['Lag_3'] = last_known['Close'].shift(3)
        last_known['SMA_20'] = last_known['Close'].rolling(window=20).mean()
        last_known['SMA_50'] = last_known['Close'].rolling(window=50).mean()
        last_known['SMA_diff'] = last_known['SMA_20'] - last_known['SMA_50']
        last_known['EMA_12'] = last_known['Close'].ewm(span=12, adjust=False).mean()
        last_known['EMA_26'] = last_known['Close'].ewm(span=26, adjust=False).mean()
        last_known['RSI'] = 50  # placeholder
        last_known['MACD'] = 0  # placeholder

        last_row = last_known.iloc[-1]
        row = {
            'SMA_20': last_row['SMA_20'],
            'SMA_50': last_row['SMA_50'],
            'RSI': last_row['RSI'],
            'MACD': last_row['MACD'],
            'EMA_12': last_row['EMA_12'],
            'EMA_26': last_row['EMA_26'],
            'Return': last_row['Return'],
            'Lag_1': last_row['Lag_1'],
            'Lag_2': last_row['Lag_2'],
            'Lag_3': last_row['Lag_3'],
            'SMA_diff': last_row['SMA_diff']
        }

        X_future = pd.DataFrame([row])
        pred_close = model.predict(X_future)[0]

        new_row = {
            'Date': current_date + timedelta(days=1),
            'Close': pred_close
        }

        last_known = pd.concat([last_known, pd.DataFrame([new_row])], ignore_index=True)
        current_date += timedelta(days=1)

    predicted_price = last_known[last_known['Date'] == target_date]['Close'].values[0]
    return f"🔮 Predicted Bitcoin Price on {target_date.date()}: ${predicted_price:.2f}"

# Flask Route
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
