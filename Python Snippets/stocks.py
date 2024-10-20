import yfinance as yf
from datetime import datetime, timedelta

def get_stock_data(symbols, start_date=None, end_date=None):
    """
    Fetch important stock data for given symbols.

    Parameters:
    - symbols: List of stock symbols (e.g., ['AAPL', 'MSFT'])
    - start_date: Start date for data retrieval in 'YYYY-MM-DD' format (default: 30 days ago)
    - end_date: End date for data retrieval in 'YYYY-MM-DD' format (default: today)

    Returns:
    - A dictionary containing stock data for each symbol
    """
    # Set default dates if not provided
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    stock_data = {}
    
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)

        if not data.empty:
            stock_data[symbol] = {
                'Closing Price': data['Close'].iloc[-1],
                'Volume': data['Volume'].iloc[-1],
                'Market Cap': stock.info.get('marketCap', 'N/A')
            }
        else:
            stock_data[symbol] = 'No data available for this period'

    return stock_data



if __name__ == "__main__":
    stocks = ["AAPL", "GOOGL"]
    print(get_stock_data(stocks))