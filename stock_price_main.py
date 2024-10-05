import streamlit as st
from datetime import date
import yfinance as yf
import pandas as pd
from datetime import datetime

st.title('Stock Today')

# Fetch today's date
Date = datetime.today().strftime(r'%d-%m-%Y')

# Define stock symbols based on categories
aggressive = ('NVDA', 'TSLA', 'SNOW', 'ROKU', 'SHOP', 'CRWD', 'PLTR')
moderate = ('KO', 'JNJ', 'PEP', 'CSCO', 'ABBV', 'PLD', 'TGT')
conservative = ('BRK.B', 'PG', 'T', 'PFE', 'VZ', 'CAT', 'CVX')

# Cache the function to load data for better performance
@st.cache_data
def load_current_data(ticker):
    data = yf.download(ticker, period="1d")  # Download only the current day's data
    return data

# Initialize dictionaries to store data for each category
category_data = {
    'Aggressive (High-risk Investors)': [],
    'Moderate (Medium-risk Investors)': [],
    'Conservative (Low-risk Investors)': []
}

# Helper function to process stock data and append to the right category
def process_stock_data(stock, category):
    data = load_current_data(stock)
    
    if not data.empty:
        open_price = data['Open'][0]
        close_price = data['Close'][0]
        high_price = data['High'][0]
        low_price = data['Low'][0]
        date = Date
        ltp = close_price  # LTP is typically the last traded price (close price for the current day)
        avg_cost = (open_price + high_price + low_price) / 3  # Example calculation for average cost
        pnl = ltp - avg_cost  # Profit & Loss
        net_change = close_price - open_price  # Net change for the day

        # Append the data to the correct category
        category_data[category].append([date, stock, avg_cost, ltp, pnl, net_change])

# Get query parameters to determine the risk profile
query_params = st.experimental_get_query_params()
risk_profile = query_params.get('risk_profile', [''])[0].lower()

# Define a function to display stocks based on the risk profile
def display_stock_data():
    if risk_profile == 'aggressive':
        for stock in aggressive:
            process_stock_data(stock, 'Aggressive (High-risk Investors)')
        category_to_display = 'Aggressive (High-risk Investors)'
    elif risk_profile == 'moderate':
        for stock in moderate:
            process_stock_data(stock, 'Moderate (Medium-risk Investors)')
        category_to_display = 'Moderate (Medium-risk Investors)'
    elif risk_profile == 'conservative':
        for stock in conservative:
            process_stock_data(stock, 'Conservative (Low-risk Investors)')
        category_to_display = 'Conservative (Low-risk Investors)'
    else:
        st.write("Invalid or no risk profile provided.")
        return
    
    # Display the filtered data
    if category_data[category_to_display]:
        df = pd.DataFrame(category_data[category_to_display], columns=['Date', 'Stock', 'Avg Cost', 'LTP', 'P&L', 'Net Change'])
        st.subheader(f"{category_to_display} Stocks")
        st.write(df)
    else:
        st.subheader(f"{category_to_display} Stocks")
        st.write("No data available for this category.")

# Call the function to display stock data
display_stock_data()