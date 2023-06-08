import yfinance as yf
from datetime import datetime, timedelta


def get_historical_data(ticker, start_date=None, end_date=None):
    """
    Retrieves historical data for a given ticker symbol and date range.

    Args:
        ticker (str): The ticker symbol to retrieve data for
        start_date (str): The start date for the historical data
        end_date (str): The end date for the historical data

    Returns:
        dataframe: Historical data for the ticker symbol and date range
    """

    # set defualt start and end dates
    if not start_date:
        start_date = (datetime.today() - timedelta(days=30)).date()
    if not end_date:
        end_date = datetime.today().date()

    hist_data = yf.download(tickers=ticker, start=start_date, end=end_date)
    if hist_data.empty:
        print("Failed to download ticker data")
        return False
    hist_data = hist_data.reset_index()
    hist_data['Date'] = hist_data['Date'].dt.date
    hist_data.rename(columns={"Date": "time_stamp"}, inplace=True)
    hist_data['Price_Change'] = hist_data['Close'].pct_change() * 100
    hist_data.drop(columns=["Adj Close", "Volume"], inplace=True)
    return hist_data
