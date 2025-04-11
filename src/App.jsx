import React, { useState, useEffect, useRef } from 'react';
import { Line } from 'react-chartjs-2';
import zoomPlugin from 'chartjs-plugin-zoom';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import './App.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  zoomPlugin
);

const App = () => {
  const [selectedCrypto, setSelectedCrypto] = useState('bitcoin');
  const [timeframe, setTimeframe] = useState('7d');
  const [isLoading, setIsLoading] = useState(false);
  const [predictionData, setPredictionData] = useState(null);
  const [error, setError] = useState(null);
  const [typedTitle, setTypedTitle] = useState('');
  const [showHeadline, setShowHeadline] = useState(false);
  const [showControls, setShowControls] = useState(false);
  const [showBackground, setShowBackground] = useState(false);
  const chartRef = useRef(null);

  const cryptos = [
    { id: 'bitcoin', name: 'Bitcoin (BTC)', symbol: 'BTC', port: 5474 },
    { id: 'ethereum', name: 'Ethereum (ETH)', symbol: 'ETH', port: 5475 },
    { id: 'solana', name: 'Solana (SOL)', symbol: 'SOL', port: 5472 },
    { id: 'doge', name: 'Dogecoin (DOGE)', symbol: 'DOGE', port: 5470 },
    { id: 'shiba', name: 'Shiba Inu (SHIB)', symbol: 'SHIB', port: 5471 },
    { id: 'tone', name: 'Tone (TON)', symbol: 'TON', port: 5473 },
    { id: 'usdt', name: 'Tether (USDT)', symbol: 'USDT', port: 5476 },
    { id: 'xrp', name: 'XRP (XRP)', symbol: 'XRP', port: 5477 }

  ];

  const timeframes = [
    { id: '1d', name: '1 Day' },
    { id: '7d', name: '7 Days' },
    { id: '30d', name: '30 Days' },
    { id: '90d', name: '90 Days' },
  ];

  // Background animation effect
  useEffect(() => {
    setTimeout(() => setShowBackground(true), 300);
  }, []);

  // Typewriter effect for title
  useEffect(() => {
    const title = "Crypto Price Prediction";
    let i = 0;
    const typing = setInterval(() => {
      if (i < title.length) {
        setTypedTitle(prev => prev + title.charAt(i));
        i++;
      } else {
        clearInterval(typing);
        setShowHeadline(true);
        setTimeout(() => setShowControls(true), 500);
      }
    }, 100);
    return () => clearInterval(typing);
  }, []);

  const handlePredict = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Find the selected crypto to get the correct port
      const selectedCryptoData = cryptos.find(c => c.id === selectedCrypto);
      if (!selectedCryptoData) {
        throw new Error('Selected cryptocurrency not found');
      }

      const response = await fetch(`http://localhost:${selectedCryptoData.port}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          crypto: selectedCryptoData.id,
          timeframe: timeframe
        }),
      });

      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Prediction failed');
      }

      setPredictionData(data);
    } catch (err) {
      setError(err.message);
      console.error('Prediction error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const getChartData = () => {
    if (!predictionData) return null;
    
    const { historical, predictions } = predictionData.result.chart_data;
    const allDates = [...historical.dates, ...predictions.dates];
    const allPrices = [...historical.prices, ...predictions.prices];
    
    // Determine if the prediction is up or down
    const lastHistoricalPrice = historical.prices[historical.prices.length - 1];
    const lastPredictedPrice = predictions.prices[predictions.prices.length - 1];
    const isPriceUp = lastPredictedPrice >= lastHistoricalPrice;
    
    // Set colors based on price direction
    const predictionColor = isPriceUp ? 'rgba(75, 192, 112, 1)' : 'rgba(255, 99, 132, 1)';
    const predictionBgColor = isPriceUp ? 'rgba(75, 192, 112, 0.2)' : 'rgba(255, 99, 132, 0.2)';
    
    return {
      labels: allDates,
      datasets: [
        {
          label: 'Historical Price',
          data: historical.prices,
          borderColor: 'rgba(54, 162, 235, 1)',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          tension: 0.4,
          fill: true,
          pointRadius: 0,
          borderWidth: 2
        },
        {
          label: 'Predicted Price',
          data: [...Array(historical.prices.length).fill(null), ...predictions.prices],
          borderColor: predictionColor,
          backgroundColor: predictionBgColor,
          borderDash: [5, 5],
          tension: 0.4,
          fill: false,
          pointRadius: 3,
          borderWidth: 2
        }
      ]
    };
  };
  
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 1200,
      easing: 'easeOutQuart'
    },
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: 'rgba(255, 255, 255, 0.8)',
          font: {
            size: 12,
            family: "'Inter', sans-serif",
            weight: 500
          },
          padding: 20,
          usePointStyle: true,
          pointStyle: 'rectRounded',
          boxWidth: 10,
          boxHeight: 10
        },
        title: {
          display: true,
          text: 'Price Data',
          color: 'rgba(255, 255, 255, 0.9)',
          font: {
            size: 14,
            weight: 'bold'
          }
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(22, 22, 40, 0.95)',
        titleColor: '#88d3ce',
        bodyColor: '#ffffff',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1,
        cornerRadius: 8,
        padding: 12,
        bodySpacing: 8,
        titleFont: {
          size: 14,
          weight: 'bold'
        },
        bodyFont: {
          size: 13
        },
        usePointStyle: true,
        boxPadding: 6,
        caretSize: 6,
        caretPadding: 8,
        callbacks: {
          title: (tooltipItems) => {
            return new Date(tooltipItems[0].label).toLocaleDateString('en-US', {
              day: 'numeric',
              month: 'short',
              year: 'numeric'
            });
          },
          label: (context) => {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 2,
                maximumFractionDigits: context.parsed.y < 1 ? 6 : 2
              }).format(context.parsed.y);
            }
            return label;
          },
          labelTextColor: (context) => {
            return context.dataset.label === 'Predicted Price' 
              ? (getPriceChangeIndicator()?.isPositive ? 'rgba(75, 192, 112, 1)' : 'rgba(255, 99, 132, 1)')
              : 'rgba(54, 162, 235, 1)';
          }
        }
      },
      zoom: {
        pan: {
          enabled: true,
          mode: 'x'
        },
        zoom: {
          wheel: {
            enabled: true
          },
          pinch: {
            enabled: true
          },
          mode: 'x'
        }
      }
    },
    scales: {
      x: {
        grid: {
          display: false,
          drawBorder: false
        },
        ticks: {
          color: 'rgba(255, 255, 255, 0.6)',
          maxRotation: 45,
          minRotation: 45,
          font: {
            size: 11
          },
          callback: function(value, index, values) {
            const date = new Date(this.getLabelForValue(value));
            return date.toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric'
            });
          }
        },
        border: {
          display: false
        }
      },
      y: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
          drawBorder: false,
          lineWidth: 0.5
        },
        ticks: {
          color: 'rgba(255, 255, 255, 0.6)',
          font: {
            size: 11
          },
          callback: (value) => {
            if (value >= 1000) {
              return `$${(value / 1000).toLocaleString()}k`;
            }
            return `$${value.toLocaleString()}`;
          },
          padding: 10
        },
        border: {
          display: false
        },
        beginAtZero: false
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    },
    elements: {
      line: {
        tension: 0.4
      },
      point: {
        hoverRadius: 7,
        hoverBorderWidth: 2,
        hitRadius: 10
      }
    },
    layout: {
      padding: {
        left: 10,
        right: 10,
        top: 20,
        bottom: 10
      }
    },
    transitions: {
      zoom: {
        animation: {
          duration: 800,
          easing: 'easeOutQuad'
        }
      }
    }
  };

  const getCurrentCrypto = () => {
    return cryptos.find(c => c.id === selectedCrypto);
  };

  const getPriceChangeIndicator = () => {
    if (!predictionData) return null;
    
    const currentPrice = predictionData.result.chart_data.historical.prices[predictionData.result.chart_data.historical.prices.length - 1];
    const predictedPrice = predictionData.result.prediction.price;
    const percentChange = ((predictedPrice - currentPrice) / currentPrice) * 100;
    
    return {
      value: percentChange.toFixed(2),
      isPositive: percentChange >= 0
    };
  };

  return (
    <div className={`app ${showBackground ? 'show-background' : ''}`}>
      <div className="background-gradient"></div>
      <div className="background-grid"></div>
      
      <header className="app-header">
        <div className="logo">
          <div className="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#88d3ce" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M12 16V8M12 8L16 12M12 8L8 12" stroke="#ff7e5f" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
        </div>
        <h1 className="typewriter">{typedTitle}<span className="cursor">|</span></h1>
        {showHeadline && (
          <h2 className="headline fade-in">
            AI-powered cryptocurrency price predictions with interactive charts
          </h2>
        )}
      </header>

      <main className="work-area">
        {showControls && (
          <div className="controls-container fade-in-up">
            <div className="controls">
              <div className="control-group">
                <label htmlFor="crypto-select">Select Cryptocurrency:</label>
                <select 
                  id="crypto-select" 
                  value={selectedCrypto}
                  onChange={(e) => setSelectedCrypto(e.target.value)}
                  className="styled-select"
                >
                  {cryptos.map(crypto => (
                    <option key={crypto.id} value={crypto.id}>{crypto.name}</option>
                  ))}
                </select>
              </div>

              <div className="control-group">
                <label htmlFor="timeframe-select">Prediction Timeframe:</label>
                <select 
                  id="timeframe-select" 
                  value={timeframe}
                  onChange={(e) => setTimeframe(e.target.value)}
                  className="styled-select"
                >
                  {timeframes.map(tf => (
                    <option key={tf.id} value={tf.id}>{tf.name}</option>
                  ))}
                </select>
              </div>

              <button 
                className="predict-button" 
                onClick={handlePredict}
                disabled={isLoading}
              >
                {isLoading ? (
                  <span className="loading">
                    <span className="loading-dot">.</span>
                    <span className="loading-dot">.</span>
                    <span className="loading-dot">.</span>
                  </span>
                ) : (
                  <>
                    <span className="predict-icon">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M2 12C2 7.28595 2 4.92893 3.46447 3.46447C4.92893 2 7.28595 2 12 2C16.714 2 19.0711 2 20.5355 3.46447C22 4.92893 22 7.28595 22 12C22 16.714 22 19.0711 20.5355 20.5355C19.0711 22 16.714 22 12 22C7.28595 22 4.92893 22 3.46447 20.5355C2 19.0711 2 16.714 2 12Z" stroke="white" strokeWidth="1.5"/>
                        <path d="M17 12L14 9M17 12L14 15M17 12H7" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    </span>
                    Predict Price
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {error && (
          <div className="error-message slide-in">
            <svg className="error-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#f44336" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M12 8V12" stroke="#f44336" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M12 16.01L12.01 15.9989" stroke="#f44336" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <p>{error}</p>
          </div>
        )}

        {predictionData && (
          <div className="results-container">
            <div className="prediction-result slide-in">
              <div className="prediction-header">
                <h3>Predicted Price for {getCurrentCrypto().name}</h3>
                <p className="timeframe">{timeframes.find(t => t.id === timeframe).name} forecast</p>
              </div>
              <div className="prediction-value">
                ${predictionData.result.prediction.price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}
              </div>
              
              {getPriceChangeIndicator() && (
                <div className={`price-change ${getPriceChangeIndicator().isPositive ? 'positive' : 'negative'}`}>
                  <span className="change-icon">
                    {getPriceChangeIndicator().isPositive ? (
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 20V4M12 4L18 10M12 4L6 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    ) : (
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 4V20M12 20L18 14M12 20L6 14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    )}
                  </span>
                  <span className="change-value">{getPriceChangeIndicator().value}%</span>
                </div>
              )}
              
              <p className="prediction-date">
                Expected on {new Date(predictionData.result.prediction.date).toLocaleDateString()}
              </p>
            </div>

            <div className="chart-container slide-in delayed">
  <h3>Price Trend & Prediction</h3>
  <div className="chart-wrapper">
    {getChartData() && (
      <Line 
        ref={chartRef}
        data={getChartData()} 
        options={chartOptions}
        datasetIdKey="id"
        updateMode="resize"
      />
    )}
  </div>
  <div className="chart-legend">
  <div className="legend-item">
    <span className="legend-color historical" style={{ backgroundColor: 'rgba(54, 162, 235, 1)' }}></span>
    <span>Historical Data</span>
  </div>
  <div className="legend-item">
    <span className="legend-color prediction" style={{ 
      backgroundColor: getPriceChangeIndicator()?.isPositive ? 'rgba(75, 192, 112, 1)' : 'rgba(255, 99, 132, 1)' 
    }}></span>
    <span>Predicted Trend ({getPriceChangeIndicator()?.isPositive ? 'Up' : 'Down'})</span>
  </div>
</div>
</div>
          </div>
        )}
      </main>

      <footer className="app-footer fade-in">
        <p>Crypto Price Prediction &copy; {new Date().getFullYear()}</p>
        <p className="disclaimer">Disclaimer: Predictions are for educational purposes only. Not financial advice.</p>
      </footer>
    </div>
  );
};

export default App;