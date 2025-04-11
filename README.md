# 🚀 Cryptocurrency Price Prediction

![Crypto Prediction](https://img.shields.io/badge/Crypto-Prediction-orange?style=for-the-badge)
![ML Model](https://img.shields.io/badge/ML-XGBoost-green?style=for-the-badge)
![Frontend](https://img.shields.io/badge/Frontend-Vite-blue?style=for-the-badge)
![Backend](https://img.shields.io/badge/Backend-Flask-red?style=for-the-badge)

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=36BCF7&center=true&vCenter=true&width=435&lines=Predict+Crypto+Prices+with+ML;XGBoost+Regressor;Real-time+Analysis;Data-driven+Decisions" alt="Typing SVG" />
</div>

## 📋 Overview

This project uses machine learning to predict cryptocurrency prices using historical data. It leverages the XGBoost Regressor model for predictions, a Flask backend API for serving the model, and a modern Vite-powered frontend for user interactions.

## ✨ Features

- 📈 Real-time cryptocurrency price predictions
- 📊 Interactive data visualization
- 🔄 Support for multiple cryptocurrencies (BTC, ETH, XRP, etc.)
- 📱 Responsive design for all devices
- 🧠 Advanced XGBoost regression model
- 📆 Historical price analysis and trends

## 🔧 Technologies Used

- **Backend**: Python, Flask, XGBoost
- **Frontend**: JavaScript, React, Vite
- **Data Processing**: Pandas, NumPy
- **Visualization**: Chart.js

## 📁 Project Structure

```
project-root/
├── api/                                
├── node_modules/                       
├── public/                             
├── src/                                
├── .gitignore                          
├── bnb_5years.csv                      
├── bnb_model.pkl                       
├── eslint.config.js                    
├── index.html                          
├── package.json                        
├── package-lock.json                   
├── README.md                           
├── shiba_5years.csv                    
├── shiba_model.pkl                     
├── ssssss.csv                          
└── vite.config.js                      
```

## 🛠️ Installation and Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Clone the Repository

```bash
git clone https://github.com/JashT14/Cryptocurrency-price-prediction.git
cd Cryptocurrency-price-prediction
```

### Backend Setup

1. Create and activate a virtual environment:

```bash
cd api
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Flask server - For each <coin_name>.py file:

```bash
python <coin_name>.py
```


### Frontend Setup

1. Install dependencies:

```bash
npm install
# or
yarn
```

2. Start the development server:

```bash
npm run dev
# or
yarn dev
```


## 📝 Usage

1. Open the application in your browser
2. Select the cryptocurrency you want to analyze
3. Choose the prediction timeframe (1 day, 7 days, 30 days)
4. View the visualized prediction results
5. Explore historical data and trends

## 🤖 ML Model Details

The XGBoost Regressor model is trained on historical cryptocurrency data with the following features:
- Opening price
- Closing price
- Volume
- Market cap
- Technical indicators (RSI, MACD, etc.)

## 🔄 Training the Model

To retrain the model with updated data:

```bash
cd backend
python models/xgboost_model.py --train --data_path data/crypto_data.csv
```

## 🚧 Future Improvements

- [ ] Add support for more cryptocurrencies
- [ ] Implement advanced feature engineering
- [ ] Add portfolio optimization suggestions
- [ ] Develop mobile application
- [ ] Integrate sentiment analysis from social media

## 🤝 Contributors

<table>
  <tr>
    <td align="center"><a href="https://github.com/JashT14"><img src="https://github.com/JashT14.png" width="100px;" alt="JashT14"/><br /><sub><b>JashT14</b></sub></a></td>
    <td align="center"><a href="https://github.com/ManasShah1810"><img src="https://github.com/ManasShah1810.png" width="100px;" alt=""/><br /><sub><b>ManasShah1810</b></sub></a></td>
    <td align="center"><a href="https://github.com/123456789165789"><img src="https://github.com/123456789165789.png" width="100px;" alt=""/><br /><sub><b>Aryan Khandare</b></sub></a></td>
    </td>
  <td align="center"><a href="https://github.com/SmitsPatil"><img src="https://github.com/SmitsPatil.png" width="100px;" alt=""/><br /><sub><b>SmitsPatil</b></sub></a></td>
    </td>
  </tr>
</table>


Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the GNU GENERAL PUBLIC LICENSE v3.0 - see the [LICENSE](LICENSE) file for details.

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" width="100%" />
</div>
