# import yfinance as yf
# import plotly.graph_objs as go
# import tkinter as tk
# from tkinter import ttk
# from plotly.offline import plot
# import webbrowser
# import os

# # Map selection to Yahoo Finance time intervals
# timeframes = {
#     "1 Day": ("1d", "5m"),
#     "5 Days": ("5d", "15m"),
#     "1 Week": ("7d", "30m"),
#     "1 Month": ("1mo", "1h"),
#     "5 Months": ("5mo", "1d")
# }

# # Function to fetch and plot data
# def show_chart(period, interval):
#     btc = yf.Ticker("BTC-USD")
#     data = btc.history(period=period, interval=interval)
#     data.reset_index(inplace=True)

#     fig = go.Figure()
#     fig.add_trace(go.Scatter(
#         x=data['Datetime'] if 'Datetime' in data else data['Date'],
#         y=data['Close'],
#         mode='lines+markers',
#         name='Close Price',
#         line=dict(color='orange')
#     ))

#     fig.update_layout(
#         title=f"📈 Bitcoin Price - {period} / {interval}",
#         xaxis_title="Time",
#         yaxis_title="Price (USD)",
#         xaxis_rangeslider_visible=True,
#         template="plotly_dark"
#     )

#     # Save and open HTML
#     file_path = "bitcoin_chart.html"
#     plot(fig, filename=file_path, auto_open=False)
#     webbrowser.open('file://' + os.path.realpath(file_path))

# # Create Tkinter GUI
# root = tk.Tk()
# root.title("Bitcoin Chart Viewer")
# root.geometry("400x300")
# root.configure(bg="#111")

# title_label = tk.Label(root, text="🪙 Bitcoin Price Chart", font=("Arial", 16, "bold"), fg="white", bg="#111")
# title_label.pack(pady=20)

# # Add buttons for each timeframe
# for label, (period, interval) in timeframes.items():
#     button = ttk.Button(root, text=label, command=lambda p=period, i=interval: show_chart(p, i))
#     button.pack(pady=5)

# root.mainloop()

from flask import Flask, render_template, request
import yfinance as yf
import plotly.graph_objs as go
from plotly.offline import plot
import os

app = Flask(__name__)

# Timeframes for the dropdown
timeframes = {
    "1 Day": ("1d", "5m"),
    "5 Days": ("5d", "15m"),
    "1 Week": ("7d", "30m"),
    "1 Month": ("1mo", "1h"),
    "5 Months": ("5mo", "1d")
}

# Chart Generation Function
def generate_chart(period, interval):
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period=period, interval=interval)
    data.reset_index(inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Datetime'] if 'Datetime' in data else data['Date'],
        y=data['Close'],
        mode='lines+markers',
        name='Close Price',
        line=dict(color='orange')
    ))

    fig.update_layout(
        title=f"📈 Bitcoin Price - {period} / {interval}",
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=True,
        template="plotly_dark"
    )

    # Save chart as HTML snippet
    chart_html = plot(fig, output_type='div', include_plotlyjs=True)
    return chart_html

# Home Route
@app.route('/', methods=['GET', 'POST'])
def index():
    chart_html = ""
    selected_option = ""
    if request.method == 'POST':
        selected_option = request.form['timeframe']
        period, interval = timeframes[selected_option]
        chart_html = generate_chart(period, interval)
    return render_template('chart.html', chart=chart_html, options=list(timeframes.keys()), selected=selected_option)

if __name__ == '__main__':
    app.run(debug=True)
