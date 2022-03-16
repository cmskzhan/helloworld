import streamlit as st
import pandas as pd
import numpy as np
from pandas_datareader import data as web
from datetime import datetime

benchmarks = {'NASDAQ Composit':'^NDQ', 'S&P 500':'^SPX', 'NASDAQ 100':'^NDX', 'HengShen':'^HSI', 'DAX':'^DAX' }


st.write("""
## Simple Streamlit web app example 
""")

st.sidebar.header("User inputs")

def get_user_input(bm):
    start_date=st.sidebar.date_input("Start Date", datetime(2019,9,15))
    end_date=st.sidebar.date_input("End Date")
    benchmark=st.sidebar.selectbox("Select Benchmark", list(bm.keys()))
    return start_date, end_date, benchmark


startdate, enddate, benchmark = get_user_input(benchmarks)
df = web.DataReader(benchmarks[benchmark], data_source='stooq', start=startdate, end=enddate)
# company_name = get_company_name(symbol.upper())

st.header(benchmark + " Closing Price from stooq\n")
st.line_chart(df['Close'])

st.header(benchmark + " Volume \n")
st.line_chart(df['Volume'])

st.header('Data statistics')
st.write(df.describe())
