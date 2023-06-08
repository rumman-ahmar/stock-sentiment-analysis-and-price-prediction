import pandas as pd
from google_news import ScrapeGoogleNews
from stocks import get_historical_data
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class StockPriceNewsSentimentAnalyzer:
    """
    A class for analyzing news sentiment and stock data.
    """

    def __init__(self, ticker, start_date=None, end_date=None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def get_news_headline_sentiment(self, headline):
        """
        Retrieves the sentiment score and remark for a given news headline.

        Args:
            headline (str): The news headline to analyze.

        Returns:
            tuple: A tuple containing the sentiment score and remark.
        """
        vader = SentimentIntensityAnalyzer()
        sentiment = vader.polarity_scores(headline)['compound']
        return sentiment, "positive" if sentiment >= 0 else "negative"

    def analyze_news_sentiment_and_stock_data(self):
        """
        Analyzes the sentiment of news headlines and stock data,
        and calculates the number of correct predictions.

        Returns:
            int: The count of correct predictions.
        """
        # Read the news data from Excel
        sgn = ScrapeGoogleNews()
        # news_df = pd.read_excel("AAPL news.xlsx")
        search_term = f"{self.ticker} stock news"
        news_df = sgn.scrape_news(
            search_term, self.start_date, self.end_date
        )

        # Combine news titles by time_stamp
        news_df = news_df.groupby('time_stamp')['news_title'].apply(' '.join).reset_index()  # noqa

        if news_df.empty:
            return False

        # Calculate sentiment scores and remarks for news titles
        news_df[['sentiment_score', 'sentiment_remark']] = news_df['news_title'].apply(  # noqa
            lambda x: pd.Series(self.get_news_headline_sentiment(x)))

        # Read the historical stock data from Excel
        # hist_df = pd.read_excel("AAPL stock data.xlsx")
        hist_df = get_historical_data(
            self.ticker, self.start_date, self.end_date
        )
        hist_df['time_stamp'] = hist_df['time_stamp'].astype(str)

        # Merge news and stock data on time_stamp
        df = pd.merge(news_df, hist_df, on='time_stamp', how='inner')

        # Calculate the count of correct predictions
        correct_count = sum((df['sentiment_score'] >= 0) & (df['Price_Change'] >= 0) |  # noqa
                            (df['sentiment_score'] < 0) & (df['Price_Change'] < 0))  # noqa
        return {
            "data": df,
            "score": format(correct_count/(len(df)-1), ".4f")
        }
