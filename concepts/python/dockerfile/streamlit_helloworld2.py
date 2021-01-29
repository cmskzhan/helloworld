  
import yfinance as yf
import streamlit as st
abt=yf.Ticker("FDS")
tickerDf = abt.history(period='1mo', interval='1h')



for fieldname, vlu in abt_info.items():
  print(fieldname, vlu)

st.write("""
# Simple Stock Price App
FDS closing price 
""")

st.line_chart(df.Close)

st.write("""
FDS volumes 
""")

st.line_chart(df.Volume)