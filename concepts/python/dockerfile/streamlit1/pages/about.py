import streamlit as st

import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
import yahooData
# import plotly.graph_objects as go
# import plotly.express as px
# from PIL import Image

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter, # STDOUT trace
)

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)


st.write("""
# Crypto Dashboard Application
Visually show data on crypto (BTC, Eth, Dodge Coins) from **2019-01-01 to today**
""")

# st.sidebar.header("User Input")
def double_ends_slides():
    cols1,_ = st.columns((4,4)) # To make it narrower
    format = 'MMM DD, YYYY'  # format output
    start_date = dt.date(year=2021,month=1,day=1)-relativedelta(years=2)  #  I need some range in the past
    end_date = dt.datetime.now().date()
    max_days = end_date-start_date

    slider = cols1.slider('Select start and end dates', start_date, end_date, (start_date, end_date), format=format)
    return slider

dates = double_ends_slides()
with tracer.start_as_current_span("foo"):
    df = yahooData.yahooDataV8("ETH-USD",  start=str(dates[0]), end=str(dates[1]))
    with tracer.start_as_current_span("bar"):
        st.write(df)

st.header("Data Statistics")
st.write(df.describe())
