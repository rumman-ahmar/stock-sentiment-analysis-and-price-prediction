# Stock Price with News Article Headline Sentiment Analysis


This project aims to analyze the change in stock prices based on sentiment analysis of news article headlines with an 80% accuracy score during testing. The project consists of several Python files that work together to gather news articles, scrape historical stock prices, perform sentiment analysis, and present the results using Streamlit.

## Files
- google_news.py: This file utilizes the requests and bs4 libraries to scrape news articles from Google News. It collects the article headlines and other relevant information, and creates a dataframe for further processing.

- stock.py: The stock.py file is responsible for scraping historical stock prices using the yfinance library. It retrieves the stock price data for a given time period and stores it for analysis.

- sentiment.py: This file performs sentiment analysis on the news article headlines using the Natural Language Toolkit (NLTK) library. It utilizes the sentiment analysis algorithm to determine the sentiment polarity (positive, negative, or neutral) of each headline. Additionally, it calls the google_news.py and stock.py files to gather the necessary data.

- main.py: The main.py file serves as the main entry point for the project. It calls the sentiment.py file to perform sentiment analysis and retrieve the stock and news data. Finally, it utilizes the Streamlit library to display the output in an interactive and visually appealing manner.

![demo](https://github.com/rumman-ahmar/stock-sentiment-analysis-and-price-prediction/assets/72764336/9e3a288b-0139-4c21-a3be-639286e7d40b)

## Usage
To run the project, follow these steps:

- Make sure you have Python 3.x installed on your system.

- Install the required libraries by running the following command in your terminal:


```
pip install requests bs4 yfinance nltk streamlit
```

Download the NLTK sentiment analysis package by opening a Python shell and running the following commands:

```
import nltk
nltk.download('vader_lexicon')
```

Place all the project files (google_news.py, stock.py, sentiment.py, and main.py) in the same directory.


```
streamlit run main.py
```

The Streamlit application will start running, and you can access it by opening the provided URL in your web browser.

Interact with the Streamlit application to view the analyzed stock prices based on the sentiment analysis of news article headlines.

## Future Work
Build a ML model around it and predict the future stock prices based on the sentiment analysis (news title) and other features
