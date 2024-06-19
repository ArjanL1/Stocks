from flask import Flask, render_template, request, jsonify
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import os

app = Flask(__name__)


API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'Enter alpha key') 

def get_intraday_stock_data(symbol):
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval='60min', outputsize='compact')
    return data

@app.route('/')
def index():
    top_stocks = get_top_stocks()
    return render_template('index.html', top_stocks=top_stocks, stock_chart_data=[], time_labels=[])

@app.route('/search', methods=['POST'])
def search():
    stock_symbol = request.form['stock_symbol']
    stock_info = get_stock_info(stock_symbol)
    intraday_data = get_intraday_stock_data(stock_symbol)
    stock_chart_data = intraday_data['4. close'].tolist()
    time_labels = intraday_data.index.format()

    top_stocks = get_top_stocks()
    return render_template('index.html', stock_info=stock_info, top_stocks=top_stocks, stock_chart_data=stock_chart_data, time_labels=time_labels)

def get_top_stocks():
    stock_symbols = ['AAPL', 'NVDA', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NFLX', 'BABA', 'V']
    stocks_data = []

    for symbol in stock_symbols:
        stock_info = get_stock_info(symbol)
        if 'error' not in stock_info:
            stocks_data.append(stock_info)

    return stocks_data

def get_stock_info(stock_symbol):
    try:
        ticker = yf.Ticker(stock_symbol)
        stock_info = ticker.info

        previous_close = stock_info.get("regularMarketPreviousClose", "N/A")
        current_price = stock_info.get("currentPrice", "N/A")
        open_price = stock_info.get("regularMarketOpen", "N/A")
        day_low = stock_info.get("regularMarketDayLow", "N/A")
        day_high = stock_info.get("regularMarketDayHigh", "N/A")
        market_cap = stock_info.get("marketCap", "N/A")
        pe_ratio = stock_info.get("trailingPE", "N/A")
        div_yield = stock_info.get("dividendYield", "N/A")
        year_low = stock_info.get("fiftyTwoWeekLow", "N/A")
        year_high = stock_info.get("fiftyTwoWeekHigh", "N/A")
        volume = stock_info.get("regularMarketVolume", "N/A")
        avg_volume = stock_info.get("averageVolume", "N/A")
        eps = stock_info.get("trailingEps", "N/A")
        beta = stock_info.get("beta", "N/A")
        target_high_price = stock_info.get("targetHighPrice", "N/A")
        target_low_price = stock_info.get("targetLowPrice", "N/A")
        target_mean_price = stock_info.get("targetMeanPrice", "N/A")
        recommendation_mean = stock_info.get("recommendationMean", "N/A")
        
        cdp_score = "N/A"
        sustainability_data = stock_info.get("sustainability", {})
        if isinstance(sustainability_data, dict):
            cdp_data = sustainability_data.get('CDP', {})
            cdp_score = cdp_data.get('score', 'N/A')

        return {
            'stock_symbol': stock_symbol,
            'previous_close': previous_close,
            'current_price': current_price,
            'open_price': open_price,
            'day_low': day_low,
            'day_high': day_high,
            'market_cap': market_cap,
            'pe_ratio': pe_ratio,
            'div_yield': div_yield,
            'year_low': year_low,
            'year_high': year_high,
            'volume': volume,
            'avg_volume': avg_volume,
            'eps': eps,
            'beta': beta,
            'target_high_price': target_high_price,
            'target_low_price': target_low_price,
            'target_mean_price': target_mean_price,
            'recommendation_mean': recommendation_mean,
        }
    except Exception as e:
        return {'error': f"An error occurred: {e}"}

if __name__ == '__main__':
    app.run(debug=True)
