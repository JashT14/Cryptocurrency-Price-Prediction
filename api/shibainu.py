from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
from datetime import datetime, timedelta
import numpy as np

app = Flask(__name__)
CORS(app)

def load_model():
    print("Loading pre-trained SHIB model...")
    try:
        with open('./api/shiba_model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("SHIB model loaded successfully")
        return model
    except FileNotFoundError:
        print("Error: Model file 'shib_model.pkl' not found")
        return None

def load_data():
    try:
        df = pd.read_csv('./api/shiba_usd_2020_2025.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        
        # Match EXACT feature names from training (including spaces)
        df['Day '] = df['Date'].dt.day  # Note the space
        df['Month '] = df['Date'].dt.month  # Note the space
        df['Year '] = df['Date'].dt.year  # Note the space
        
        # Technical indicators
        df['Return'] = df['Close'].pct_change()
        df['Lag_1'] = df['Close'].shift(1)
        df['Lag_2'] = df['Close'].shift(2)
        df['Lag_3'] = df['Close'].shift(3)
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df.dropna(inplace=True)
        return df
    except Exception as e:
        print(f"Error loading SHIB data: {str(e)}")
        return None

def forecast_future(df, model, days_to_predict):
    last_known = df.copy()
    current_date = last_known['Date'].max()
    
    predictions = []
    historical_dates = last_known['Date'].tolist()
    historical_prices = last_known['Close'].tolist()
    
    for day in range(1, days_to_predict+1):
        next_date = current_date + timedelta(days=1)
        
        # Match EXACT feature names from training
        X_future = pd.DataFrame([{
            'Day ': next_date.day,      # Note the space
            'Month ': next_date.month,  # Note the space
            'Year ': next_date.year    # Note the space
        }])
        
        pred_close = model.predict(X_future)[0]
        
        predictions.append({
            'date': next_date.strftime('%Y-%m-%d'),
            'price': float(pred_close)
        })
        current_date = next_date

    chart_data = {
        'historical': {
            'dates': [d.strftime('%Y-%m-%d') for d in historical_dates[-30:]],
            'prices': [float(p) for p in historical_prices[-30:]]
        },
        'predictions': {
            'dates': [p['date'] for p in predictions],
            'prices': [p['price'] for p in predictions]
        }
    }
    
    return {
        'prediction': predictions[-1],
        'chart_data': chart_data,
        'timeframe': f"{days_to_predict} days"
    }

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        crypto = data.get('crypto', 'SHIB-USD')
        timeframe = data.get('timeframe', '7d')
        
        timeframe_map = {
            '1d': 1,
            '7d': 7,
            '30d': 30,
            '90d': 90
        }
        days_to_predict = timeframe_map.get(timeframe, 7)
        
        if 'date' in data:
            date_str = data.get('date')
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Match EXACT feature names from training
            input_df = pd.DataFrame([{
                "Day ": date_obj.day,      # Note the space
                "Month ": date_obj.month,  # Note the space
                "Year ": date_obj.year    # Note the space
            }])
            
            prediction = model.predict(input_df)[0]
            return jsonify({
                "date": date_str,
                "predicted_price": float(f"{prediction:.10f}"),
                "predicted_price_scientific": f"{prediction:.4e}",
                "success": True
            })
        else:
            result = forecast_future(df, model, days_to_predict)
            return jsonify({
                'success': True,
                'crypto': crypto,
                'timeframe': timeframe,
                'result': result
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Initialize
model = load_model()
df = load_data()

if __name__ == '__main__':
    if model is not None and df is not None:
        print("Starting SHIB-USD Prediction API...")
        app.run(host='0.0.0.0', port=5471, debug=True)
    else:
        print("Failed to start server due to missing model or data file")