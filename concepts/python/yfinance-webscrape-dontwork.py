# pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org beautifulsoup4
# pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org lxml
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as ur

tker= 'MSFT'
# URL link 
url_is = 'https://finance.yahoo.com/quote/' + tker + '/financials?p=' + tker
url_bs = 'https://finance.yahoo.com/quote/' + tker +'/balance-sheet?p=' + tker
url_cf = 'https://finance.yahoo.com/quote/' + tker + '/cash-flow?p='+ tker

print(url_is, "\n", url_bs, "\n", url_cf)

read_data = ur.urlopen(url_is).read() 
soup_is= BeautifulSoup(read_data, 'lxml')
ls=list(soup_is.find_all('div'))
ls = [e for e in ls if e not in ('Operating Expenses','Non-recurring Events')]
new_ls = list(filter(None,ls))
print(new_ls[12:])