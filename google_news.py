import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


class ScrapeGoogleNews:
    """
    A class for scraping news data from Google News based on a search term.
    """

    def make_request_and_soup(self, search_term, page, proxies=None):
        """function to make a request to Google News
            and scrape the news data
        """

        articles_per_page = 100
        google_news_url = "https://news.google.com/search?q="

        start = page * articles_per_page
        url = f"{google_news_url}{search_term}&start={start}"
        response = requests.get(url, proxies=proxies)
        if response.status_code != 200:
            print("Hmm... Seems like Google blocked the IP, please try again later or use proxies")  # noqa
            return False

        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.find_all(
            'div', 'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc'
        )
        return articles

    def make_news_df(self, news_providers, news_titles, time_stamps):
        """make news articles dataframe

        Args:
            news_providers (list): list of news_providers
            news_titles (list): list of news_titles
            time_stamps (list): list of time_stamps

        Returns:
            dataframe: DataFrame containing news data
        """
        news = {
            "news_provider": news_providers,
            "news_title": news_titles,
            "time_stamp": time_stamps
        }
        print("Done! Making dataframe...")
        news_df = pd.DataFrame(news)
        news_df.drop_duplicates(inplace=True)
        print("Done!")
        return news_df

    def scrape_news(self, search_term, start_date=None,
                    end_date=None, proxies=None):
        """
        Scrapes news from Google News based on the search term and date range.

        Args:
            search_term (str): The term to search for in Google News
            start_date (str): The start date for filtering news articles
            end_date (str): The end date for filtering news articles
            proxies (dict): Dictionary of proxy URLs.

        Returns:
            dataframe: DataFrame containing news data
        """
        if not search_term:
            print("Search term is required")
            return False

        # set defualt start and end dates
        if not start_date:
            start_date = (datetime.today() - timedelta(days=30)).date()
        if not end_date:
            end_date = datetime.today().date()

        page = 0
        stop = False
        news_providers, news_titles, time_stamps = [], [], []

        print(f"Scraping google news for {search_term}...")
        while True:
            articles = self.make_request_and_soup(search_term, page, proxies)
            # break the loop if no articles or articles are not in date range
            if not articles or stop:
                break

            # itretae article div tag and extract data
            for article in articles:
                news_provider = article.find(
                    'img', 'tvs3Id tvs3Id lqNvvd lITmO WfKKme'
                ).get('alt')
                news_title = article.find('h3', 'ipQwMb ekueJc RD0gLb').text
                time_stamp = article.find('time')['datetime'].split('T')[0]

                if str(start_date) <= time_stamp <= str(end_date):
                    news_providers.append(news_provider)
                    news_titles.append(news_title)
                    time_stamps.append(time_stamp)
                else:
                    stop = True

            page += 1

        return self.make_news_df(news_providers, news_titles, time_stamps)
