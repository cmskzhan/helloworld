# from time import sleep
from time import sleep
import miniEnc as enc
import ast
import requests

def chunks(l, n):
    ll = list(l)
    for i in range(0, len(ll), n):
        yield ll[i:i+n]

def less_than_32_symbols(symbols_in_8s, k) -> dict:
    url = "https://api.twelvedata.com/eod"
    count = 0
    close_price = {}
    for each_8_symbols in symbols_in_8s:
        params = {"symbol": ",".join(each_8_symbols), "apikey": k[count]}
        count += 1
        response = requests.get(url, params=params)
        r = response.json()
        for ticker in each_8_symbols:
            close_price[ticker] = r[ticker]["close"]
    return close_price


def getEODprice(L) -> dict:
    g = b'z4zZpKqmm9jAubi2gLF8d3ja2Kqgz56eyJhpxarIo6msqIyeen6NhYOBf3ikr6nY0aGenZtsmZqtx6uspabGo4qNtomEgW9xYqDarKOmm56XanGTpJunqainnaOTvbiHfoR6qnneqKXU05GThF1pw6rKqtasp5umjIqItrB_gad1qaylpNDNn8iaa8OolZrR'
    k = ast.literal_eval(enc.decode(enc.cccccccz, g))
    
    symbols_in_8s = list(chunks(set(L), 8)) # 8 symbols per request (12data free tier)
    all_close_price = {}

    for i in range(0, int(len(symbols_in_8s)/(len(k)))+1):
        all_close_price.update(less_than_32_symbols(symbols_in_8s[i*len(k): (i+1)*len(k)], k))
        if i>1:
            print(i, "sleeping for 60 seconds")
            sleep(60)
    return all_close_price

            

        
def main():
    L1 = [
    'MMM',
    'ANSS',
    'ABT',
    'ATVI',
    'AKAM',
    'GOLD',
    'BL',
    'BB',
    'BX',
    'ET',
    'FDS',
    'GILD',
    'IEA',
    'INSW',
    'ISRG',
    'IVZ',
    'KOPN',
    'LRCX',
    'LITE',
    'MP',
    'MSCI',
    'MS',
    'MOS',
    'OKTA',
    'QDEL',
    'RTX',
    'SWIR',
    'SKLZ',
    'SDC',
    'LUV',
    'TSLA',
    'TROX',
    'TWLO',
    'ME',
    'VEEV',
    'XLNX',
    'ZM',
    'ZS']


    print(getEODprice(L1))

if __name__ == "__main__":
    main()