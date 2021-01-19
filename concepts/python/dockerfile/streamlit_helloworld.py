  
from pandas_datareader import data as web
df = web.DataReader("FDS", data_source='yahoo', start='01-01-2020')
#import yfinance as yf
import streamlit as st

st.write("""
# Simple Stock Price App
FDS closing price 
""")

st.line_chart(df.Close)

st.write("""
FDS volumes 
""")

st.line_chart(df.Volume)