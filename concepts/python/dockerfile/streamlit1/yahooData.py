import json
import pandas as pd
from datetime import datetime
import requests

def json2dfConversion(jsonText, intervals):
    p = json.loads(jsonText)
    ohlc_json = p['chart']['result'][0]['indicators']['quote'][0]
    dates = p['chart']['result'][0]['timestamp']
    ohlc_df = pd.DataFrame.from_dict(ohlc_json)

    if intervals == "1d":
        ohlc_df['Date'] = [datetime.fromtimestamp(x).date() for x in dates] 
    else:
        ohlc_df['Date'] = [datetime.fromtimestamp(x) for x in dates] 
    
    ohlc_df.index = ohlc_df['Date']
    return ohlc_df

def yahooDataV8(sym, start, end=datetime.today().strftime('%Y-%m-%d'), interval="1d"): # interval=1m, 2m, 5m, 15m, 30m, 1h, 5d, 1w, 1mo
    
    if interval not in ["1m", "2m", "5m", "15m", "30m", "1h", "1d","5d", "1wk", "1mo"]:
        raise ValueError("Invalid Parameter: interval!")
        
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    baseurl = "https://query1.finance.yahoo.com/v8/finance/chart/" + sym
    x = int(datetime.strptime(start, '%Y-%m-%d').strftime("%s")) #convert %Y-%m-%d to epoch
    y = int(datetime.strptime(end, '%Y-%m-%d').strftime("%s"))
    url = baseurl + "?period1=" + str(x) + "&period2=" + str(y) + "&interval=" + interval +"&events=history" 
    print(url)
    jsonOutput = requests.get(url, headers=header)
    return json2dfConversion(jsonOutput.text, interval)