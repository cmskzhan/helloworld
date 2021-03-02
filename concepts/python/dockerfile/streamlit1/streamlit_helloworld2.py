  
import yfinance as yf
import streamlit as st


st.title("Quick display of a stock, default is MSFT")
# stockNotWorking = st.sidebar.text_input('Yahoo Symbol:')
stock = st.sidebar.text_input('Yahoo Symbol:')

# stock = st.sidebar.selectbox('Yahoo Symbol:',('MSFT','AAPL', 'FDS', 'NDAQ', 'T'))

if not stock:
  st.warning("no stock detected, use default symbol")
  stock = "MSFT"


p = st.sidebar.radio('period:',['1mo','2mo','3mo'])

df=yf.Ticker(stock)
tickerDf = df.history(period=p, interval='1h')


st.write("""
## SideBars etc
yfinance package with more refined intervals
""")


st.line_chart(tickerDf[['Open','Close']])

st.write("""
Volumes 
""")

st.line_chart(tickerDf.Volume)

st.write(tickerDf)