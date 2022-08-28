  
from pandas_datareader import data as web
df = web.DataReader("FDS", data_source='stooq', start='01-01-2022')
#import yfinance as yf
import streamlit as st


st.title("""
# Simple Stock Price App
FDS closing price :tada:
""", anchor="title") # anchor="title" creates a link to this section

st.caption("created by Kai, last updated on 2022-08-28")
st.header("Header 1: FDS closing price", anchor="header1")
st.subheader("Subheader 1: closing price", anchor="subheader1")
st.write("Normal text: from stooq")

st.line_chart(df.Close)

st.header("""
Header 2:
FDS volumes 
""", anchor="header2")

st.line_chart(df.Volume, use_container_width=False)
st.code("""
st.title()
st.caption("created by Kai, last updated on 2022-08-28")
st.header("Header 1: FDS closing price", anchor="header1")
st.subheader("Subheader 1: closing price", anchor="subheader1")
st.write("Normal text: from stooq")
st.line_chart(df.Close)
st.bar_chart(df.Close)
st.area_chart(df.Close)
""")
st.latex(r"""
\int_0^\infty x^2 dx = \frac{d^2y}{dx^2}
""")
"table"
mytable = st.table(df.tail())
import time
time.sleep(3)
mytable.add_rows(df.head()) #dynamically add row, can also add to charts, but it will hold up below outputs
"bar chart"
bar1 = st.bar_chart(df[['High', 'Low']].head(20))
time.sleep(3)
bar1.add_rows(df[['High', 'Low']].tail(20))
"dataframe"
st.dataframe(df.tail(20))
"area chart :sunglasses:"
st.area_chart(df[['High', 'Low']])
"metric"
st.metric(label = "last close price", value = df.Close.iloc[-1], delta="10%")


login_details = {
  "credentials": {
    "usernames": {
      "jsmith": {
        "email": "kaizhang@yahoo.com",
        "name": "John Smith",
        "password": 123
      },
      "rbriggs": {
        "email": "rbriggs@gmail.com",
        "name": "Rebecca Briggs",
        "password": 456
      }
    }
  },
  "cookie": {
    "expiry_days": 1,
    "key": "some_signature_key",
    "name": "cookie_name_streamlit_authenticator"
  },
  "preauthorized": {
    "emails": [
      "abc@gmail.com"
    ]
  }
}
st.json(login_details)

import numpy as np
import pandas as pd
def random_lat_lon(n=1, lat_min=-90., lat_max=90., lon_min=-180., lon_max=180.):
    """
    this code produces an array with pairs lat, lon
    """
    lat = np.random.uniform(lat_min, lat_max, n)
    lon = np.random.uniform(lon_min, lon_max, n)

    return pd.DataFrame({"lat": lat, "lon": lon})
"st.map"
st.map(random_lat_lon(n=100))
"st.video"
st.video("basic_animation.mp4")

clicked = st.button("Click me")
st.write("You clicked me ", clicked)
clickedagain = st.button("Click me again")
st.write("You clicked me again", clickedagain)
