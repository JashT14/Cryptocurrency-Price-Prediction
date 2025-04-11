import yfinance as yf
import pandas as pd
import xgboost as xgb
import pickle
import numpy as np
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime

# Step 1: Download Binance Coin data
def download_data():
    print("Downloading BNB-USD data...")
    data = yf.download('BNB-USD', period='5y', interval='1d')
    data.to_csv('bnb_5years.csv')
    print("Saved to bnb_5years.csv")
    return data

# Step 2: Train model with XGBoost
def train_model(data):
    print("Training model...")
    df = data.reset_index()
    df['Day'] = df['Date'].dt.day
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year

    X = df[['Day', 'Month', 'Year']]
    y = df['Close']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    print(f"Model trained. RMSE: {rmse:.2f}")

    with open('bnb_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model saved as bnb_model.pkl")

# Step 3: Flask API to make predictions
def create_app():
    with open('bnb_model.pkl', 'rb') as f:
        model = pickle.load(f)

    app = Flask(__name__)

    @app.route("/predict", methods=["POST"])
    def predict():
        try:
            data = request.get_json()
            date_str = data.get("date")  # Expected format: YYYY-MM-DD
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            input_df = pd.DataFrame([{
                "Day": date_obj.day,
                "Month": date_obj.month,
                "Year": date_obj.year
            }])
            prediction = model.predict(input_df)[0]
            return jsonify({
                "date": date_str,
                "predicted_price": round(prediction, 2)
            })
        except Exception as e:
            return jsonify({"error": str(e)})

    return app

# Main execution
if __name__ == "__main__":
    bnb_data = download_data()
    train_model(bnb_data)
    app = create_app()
    app.run(debug=True)
