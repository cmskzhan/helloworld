# https://polygon.io/docs/get_v2_aggs_ticker__stocksTicker__range__multiplier___timespan___from___to__anchor
import requests
import datetime
import json
import pandas as pd
import encStrings
import pickle

'''
Getting polygon ohlc, vwap and volume requires symbol, date range, etc
'''
AK = encStrings.decode(encStrings.cccccccz, pickle.loads(requests.get("https://github.com/cmskzhan/helloworld/raw/master/pgon.pik").content))
# BASE_URL = "https://api.polygon.io/v2/aggs/ticker/"
url=r"https://api.polygon.io/v2/aggs"
symbol="ANSS"
multiplier=1
timespan="day"
from_date="2020-01-01"
to_date=datetime.date.today()
vw_url = f"/ticker/{symbol}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
data = { "apikey": AK, "sort": "asc", "limit": 50000 }
full_url = url + vw_url

column_names = { 
"v": "Volume",
"vw": "VWAP",
"o": "Open",
"c": "Adj Close",
"h": "High",
"l": "Low",
"n": "transactions"
  }

response = requests.get(full_url, data)
parsed = json.loads(response.text)

df_polygon = pd.DataFrame.from_dict(parsed['results'])
df_polygon["Date"] = pd.to_datetime(df_polygon['t']/1000, unit='s').dt.date
df_polygon = df_polygon.rename(columns=column_names)
df_polygon.set_index('Date', inplace=True)
df_polygon.index=pd.to_datetime(df_polygon.index)
print(df_polygon)
