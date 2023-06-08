import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sentiment import StockPriceNewsSentimentAnalyzer


def plot_stock_price_with_sentiment(text_input, start_date, end_date):
    """function to plot stock price with sentiment analysis

    Args:
        text_input (str): ticker for stock historical data and search term for news
        start_date (str): from where data and news is needed
        end_date (str): up to which data and news is needed
    """

    # add loader until we get data
    with st.spinner("Loading data..."):
        spns = StockPriceNewsSentimentAnalyzer(
            text_input, start_date, end_date
        )
        res = spns.analyze_news_sentiment_and_stock_data()

    if not res:
        st.error("Something went wrong")
        return

    # Load the data
    df = res['data']
    score = res['score']
    print(df)

    # Convert time_stamp to datetime format
    df['time_stamp'] = pd.to_datetime(df['time_stamp'])

    # Create the line graph trace
    line_trace = go.Scatter(
        x=df['time_stamp'],
        y=df['Close'],
        mode='markers+lines',
        name='Close Price',
        line=dict(width=3)
    )

    # Create the sentiment remark symbols trace
    sentiment_positive = df[df['sentiment_remark'] == 'positive']
    sentiment_negative = df[df['sentiment_remark'] == 'negative']
    symbol_trace_positive = go.Scatter(
        x=sentiment_positive['time_stamp'],
        y=sentiment_positive['Close'],
        mode='markers',
        name='Positive',
        marker=dict(symbol='triangle-up', color='green')
    )
    symbol_trace_negative = go.Scatter(
        x=sentiment_negative['time_stamp'],
        y=sentiment_negative['Close'],
        mode='markers',
        name='Negative',
        marker=dict(symbol='triangle-down', color='red')
    )

    # Create the figure
    fig = go.Figure(data=[
        line_trace,
        symbol_trace_positive,
        symbol_trace_negative]
    )

    # Update the layout
    fig.update_layout(
        title='Time Stamp vs Close Price',
        xaxis=dict(title='Time Stamp'),
        yaxis=dict(title='Close Price'),
        xaxis_tickangle=-45
    )

    # Display the score
    st.subheader("Sentiment Accuracy Score")
    st.write(score)

    # Display the plot using Streamlit
    st.plotly_chart(fig)

    # Display the plot using Streamlit
    st.subheader("Stock Price Data")
    st.dataframe(df)


# Input fields
text_input = st.text_input("Enter ticker:", "TSLA")
two_weeks_ago_date = (datetime.now() - timedelta(weeks=2)).date()
start_date = st.date_input("Start Date:", two_weeks_ago_date)
end_date = st.date_input("End Date:")

# Generate plot based on input
if st.button("Generate Plot"):
    plot_stock_price_with_sentiment(text_input, start_date, end_date)
