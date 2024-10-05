import streamlit as st
from datetime import datetime
import yfinance as yf
import pandas as pd

st.set_page_config(page_title='Conservative Investor Stocks', page_icon='📉', layout='wide')

# Set the title for the conservative page
st.title('Conservative Investor Stocks')

# Fetch today's date
Date = datetime.today().strftime(r'%d-%m-%Y')

# Conservative stock symbols
conservative = ('BRK.B', 'PG', 'T', 'PFE', 'VZ', 'CAT', 'CVX')

# Cache the function to load data for better performance
@st.cache_data
def load_current_data(ticker):
    data = yf.download(ticker, period="1d")  # Download only the current day's data
    return data

# Initialize data for Conservative category
conservative_data = []

# Process Conservative stock data
for stock in conservative:
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

        # Append the data for each stock
        conservative_data.append([date, stock, avg_cost, ltp, pnl, net_change])

# Display data for Conservative category
if conservative_data:
    df = pd.DataFrame(conservative_data, columns=['Date', 'Stock', 'Avg Cost', 'LTP', 'P&L', 'Net Change'])
    st.subheader("Conservative (Low-risk Investor) Stocks")
    
    # Display stock data with color gradients for P&L
    st.dataframe(df.style.format({
        'Avg Cost': "{:.2f}",
        'LTP': "{:.2f}",
        'P&L': "{:.2f}",
        'Net Change': "{:.2f}"
    }).background_gradient(subset=['P&L'], cmap='RdYlGn'))  # Color gradient for P&L
else:
    st.write("No data available for Conservative stocks.")
