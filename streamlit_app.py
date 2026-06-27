import pandas as pd
import streamlit as st
import yfinance as yf
import requests
from typing import Optional

# Function calling local CSS sheet
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.sidebar.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

# Local CSS sheet
local_css("style.css")

# Custom session to avoid some rate limiting issues
@st.cache_resource
def get_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    })
    return session

# Helper function to display data or handle empty data
def display_data(data: Optional[pd.DataFrame]):
    if data is None or data.empty:
        st.write("No data available at the moment")
    else:
        st.write(data)

# Main function
def main():
    session = get_session()

    st.subheader("""Daily **closing price** for """ + selected_stock)
    # Get data on searched ticker
    stock_data = yf.Ticker(selected_stock, session=session)

    try:
        # Get historical data for searched ticker
        stock_df = stock_data.history(start='2020-01-01')

        if stock_df.empty:
            st.write(f"No historical data found for {selected_stock}. Possibly delisted or incorrect ticker.")
        else:
            # Print line chart with daily closing prices for searched ticker
            if 'Close' in stock_df.columns:
                st.line_chart(stock_df.Close)
            else:
                st.write("Closing price data not available.")

            st.subheader("""Last **closing price** for """ + selected_stock)
            # Get current date data for searched ticker
            stock_lastprice = stock_data.history(period='1d')
            # Get current date closing price for searched ticker
            if not stock_lastprice.empty and 'Close' in stock_lastprice.columns:
                last_price = stock_lastprice.Close
                st.write(last_price)
            else:
                st.write("No data available at the moment")

            # Get daily volume for searched ticker
            st.subheader("""Daily **volume** for """ + selected_stock)
            if 'Volume' in stock_df.columns:
                st.line_chart(stock_df.Volume)
            else:
                st.write("Volume data not available.")

            # Additional information feature in sidebar
            st.sidebar.subheader("""Display Additional Information""")
            # Checkbox to display stock actions for the searched ticker
            actions = st.sidebar.checkbox("Stock Actions")
            if actions:
                st.subheader("""Stock **actions** for """ + selected_stock)
                display_data(stock_data.actions)

            # Checkbox to display quarterly financials for the searched ticker
            financials = st.sidebar.checkbox("Quarterly Financials")
            if financials:
                st.subheader("""**Quarterly financials** for """ + selected_stock)
                display_data(stock_data.quarterly_financials)

            # Checkbox to display list of institutional shareholders for searched ticker
            major_shareholders = st.sidebar.checkbox("Institutional Shareholders")
            if major_shareholders:
                st.subheader("""**Institutional investors** for """ + selected_stock)
                display_data(stock_data.institutional_holders)

            # Checkbox to display quarterly balance sheet for searched ticker
            balance_sheet = st.sidebar.checkbox("Quarterly Balance Sheet")
            if balance_sheet:
                st.subheader("""**Quarterly balance sheet** for """ + selected_stock)
                display_data(stock_data.quarterly_balance_sheet)

            # Checkbox to display quarterly cashflow for searched ticker
            cashflow = st.sidebar.checkbox("Quarterly Cashflow")
            if cashflow:
                st.subheader("""**Quarterly cashflow** for """ + selected_stock)
                display_data(stock_data.quarterly_cashflow)

            # Checkbox to display quarterly earnings for searched ticker
            earnings = st.sidebar.checkbox("Quarterly Earnings")
            if earnings:
                st.subheader("""**Quarterly earnings** for """ + selected_stock)
                display_data(stock_data.quarterly_earnings)

            # Checkbox to display list of analysts recommendation for searched ticker
            analyst_recommendation = st.sidebar.checkbox("Analysts Recommendation")
            if analyst_recommendation:
                st.subheader("""**Analysts recommendation** for """ + selected_stock)
                display_data(stock_data.recommendations)

    except Exception as e:
        if "Too Many Requests" in str(e) or "Rate limited" in str(e):
            st.error("Rate limit reached for Yahoo Finance. Please try again later.")
        else:
            st.error(f"An error occurred: {e}")

# Ticker search feature in sidebar
st.sidebar.subheader("""Stock Search Web App""")
selected_stock = st.sidebar.text_input("Enter a valid stock ticker...", "GOOG")
button_clicked = st.sidebar.button("GO")

if __name__ == "__main__":
    main()
