  
from datetime import date
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
\int_0^\infty x^2 dx = \frac{d^2y}{dx^2} \\
\int_0^\infty 2x dx = \frac{d^3y}{dx^3} \\
""")
st.latex(r"\lim\limits_{n\rightarrow\infty}{\left(1+\frac{1}{n}\right)^n}")
st.latex(r"H(D_2) = -\left(\frac{2}{4}\log_2 \frac{2}{4} + \frac{2}{4}\log_2 \frac{2}{4}\right) = 1")
st.latex(r"\begin{cases} s = V_光 * (t1 - t0)\\ s = V_声 * (t2 - t0) \end{cases}")
#  st.latex(r"\ce{Hg^2+ ->[I-] HgI2 ->[I-] [Hg^{II}I4]^2-}") 
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
st.button("can't click me", key="disabled", disabled=True, help="I can't be clicked")

radioed_item = st.radio("Select an item", ["A", "B", "C"])
st.write("You selected ", radioed_item)
selected_item = st.selectbox("Select an item", ["E", "F", "G"])
st.write("You selected ", selected_item)
#multi select columns of df
selected_items = st.multiselect("Select items", ["High", "Low", "Open", "Close", "Volume"], default=["High", "Low"])
st.write(df[selected_items])
value1 = st.slider("Select a value", 0.0, 100.0, (25.0, 75.0))
st.write("You selected ", value1)
value2 = st.slider("select a date", date(2000, 1, 1), date(2020, 1, 1), date(2015, 1, 1))
st.write("You selected ", value2)
value3 = st.select_slider("select a step", [1,2,3,4,5,6,7,8,9,10], 2) #none continuous
st.write("You selected ", value3)
username = st.text_input("Enter your name", "John Doe", help="This is a help text")
st.write("Hello ", username)
password = st.text_input("Enter your password", "", help="password help", type="password")
st.write("Your password is ", password)
st.write(st.text_area("Enter something", "Hello world with examples"))
n_girls = st.number_input("how many ex girlfriends?", min_value=0, max_value=10, value=2, step=2)
st.write(n_girls)
reserved = st.date_input("reservation date")
st.write(reserved)
alarm = st.time_input("What'the time Mr. Wolf?")
st.write("time is ", alarm)
f = st.file_uploader("upload csv file only", type=["csv"])
if f is not None:
  df = pd.read_csv(f)
f2 = st.file_uploader("upload multi csv files", type=["csv"], accept_multiple_files=True)
for f in f2:
  df = pd.read_csv(f)

st.write(st.session_state)
st.header("cache")
@st.cache()
def get_more_data(symbol: str) -> pd.DataFrame:
  cache_df  = web.DataReader(symbol, data_source='stooq', start='01-01-2021')
  return cache_df
sym = "MSCI"
st.write("max price from 2021 for ", sym, max(get_more_data(sym)['High']))

