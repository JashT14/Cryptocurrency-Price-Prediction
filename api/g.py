import yfinance as yf
import pandas as pd
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator
from datetime import datetime, timedelta

# Step 1: Auto set last 1 year dates
def get_date_range():
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

# Step 2: Download ETH historical data
def fetch_eth_data(start_date, end_date, interval='1d'):
    print("📥 Fetching Ethereum data...")
    eth = yf.download("ETH-USD", start=start_date, end=end_date, interval=interval, auto_adjust=True)
    eth.reset_index(inplace=True)
    eth.columns = [col[0] if isinstance(col, tuple) else col for col in eth.columns]  # Flatten MultiIndex
    eth.dropna(inplace=True)
    return eth

# Step 3: Add technical indicators
def add_technical_indicators(df):
    print("📊 Adding technical indicators...")

    close_series = df['Close']
    df['SMA_20'] = SMAIndicator(close=close_series, window=20).sma_indicator()
    df['SMA_50'] = SMAIndicator(close=close_series, window=50).sma_indicator()
    df['RSI'] = RSIIndicator(close=close_series, window=14).rsi()
    df['MACD'] = MACD(close=close_series).macd_diff()
    df['EMA_12'] = EMAIndicator(close=close_series, window=12).ema_indicator()
    df['EMA_26'] = EMAIndicator(close=close_series, window=26).ema_indicator()

    df.dropna(inplace=True)
    return df

# Step 4: Save to CSV
def save_dataset(df, filename='ethereum_last_1_year.csv'):
    print(f"💾 Saving dataset to {filename}...")
    df.to_csv(filename, index=False)
    print("✅ Done!")

# Main
if __name__ == "__main__":
    start, end = get_date_range()
    eth_df = fetch_eth_data(start, end)
    eth_df = add_technical_indicators(eth_df)
    save_dataset(eth_df)

    print("\n📄 Preview of final dataset:")
    print(eth_df.tail())
