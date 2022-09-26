import pandas as pd
import numpy as np
import json
import re
import sys
import PyPDF2
from datetime import datetime
from difflib import get_close_matches

def load_ticker_from_json(json_file: str, df_in: pd.DataFrame) -> pd.DataFrame:
    try: 
        with open(json_file) as f: 
            ticker_dict = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file} not found")
        return df_in
    for k, v in ticker_dict.items():
        df_in.loc[df_in['Market'] == k, 'Ticker'] = v
    return df_in

def get_sec_tickers() -> dict:
    # get json from sec site and convert to dict    
    try:
        sec_site_mapping = pd.read_json(r'https://www.sec.gov/files/company_tickers.json', orient='index')
    except:
        print("Error: can not get to sec tickers from https://www.sec.gov/files/company_tickers.json")
        return {}
    sec_site_mapping['title'] = sec_site_mapping['title'].str.replace('\.', '', regex=True)
    sec_site_mapping['title'] = sec_site_mapping['title'].str.replace('\,', '', regex=True)
    return dict(zip(sec_site_mapping['title'], sec_site_mapping['ticker']))   

def pdf_to_dict(pdf_path: str) ->dict:
    start = datetime.now()
    alltext = ""
    try:
        with open(pdf_path, 'rb') as f:
            pdfReader = PyPDF2.PdfFileReader(f)
            for i in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(i)
                alltext += pageObj.extractText()
    except:
        print("Error: can not open pdf")
        return {}
    
    print(f"total time to read pdf: {datetime.now() - start}")

    mapping_lines = []
    for i in re.split(r'\n', alltext):    
        # if string ends with Y or N
        if i.endswith('Y') or i.endswith('N'):
            mapping_lines.append(i)
    print(f"Total usable lines found  in IG pdf: {len(mapping_lines)} and time taken: {datetime.now() - start}")
    
    pattern = r"(?P<name>^.*)\s(?P<ticker>\w+.\w+)\s\/\s(?P<symbol>\w+)\s(?P<region>\w+).*\s(?P<ISA>\w)\s(?P<SIPP>\w)$"
    all_pdf_tickers2 = pd.DataFrame()
    for i in mapping_lines:
        m = re.search(pattern, i)
        if m:
            # all_pdf_tickers = all_pdf_tickers.append(m.groupdict(), ignore_index=True) also works but futureWarning
            all_pdf_tickers2 = pd.concat([all_pdf_tickers2, pd.DataFrame.from_dict(m.groupdict(), orient='index').T], ignore_index=True)
    print(f"Total extracted records found in IG pdf: {len(all_pdf_tickers2)} and time taken: {datetime.now() - start}")
    # filter to US stocks only
    all_USA_tickers = all_pdf_tickers2[all_pdf_tickers2['region'] == 'US']
    us_tickers = dict(zip(all_USA_tickers['name'], all_USA_tickers['symbol']))
    non_USA_tickers = all_pdf_tickers2[all_pdf_tickers2['region'] != 'US']
    non_us_tickers = dict(zip(non_USA_tickers['name'], non_USA_tickers['ticker']))

    return {**non_us_tickers, **us_tickers}

def close_matched_tickers(unknown_ticker_list: list, tickers_dict: dict, cutoff_ratio = 0.801) -> dict:
    """
    compare company name without tickers against a ticker dictionary find close word match ratio above 0.8 by default
    """
    possible_resolute = {}
    ticker_keys = list(tickers_dict.keys())
    for i in unknown_ticker_list:
        closely_matched_name = get_close_matches(i, ticker_keys, cutoff=cutoff_ratio)
        if len(closely_matched_name) > 0:
            possible_resolute[i] = tickers_dict[closely_matched_name[0]]
    return possible_resolute


def match_tickers_dict(ticker_dict: dict, df_in: pd.DataFrame) -> pd.DataFrame:
    ''' match ticker from dict to df_in and return df_in with ticker column'''
    df_in['TPname'] = df_in['Market'].str.replace(r'\(.*\)', '', regex=True).str.strip()
    df_in['Ticker'] = df_in['TPname'].map(ticker_dict).fillna(df_in['Ticker'])
    return df_in

def add_ticker_to_json(new_dict: dict, output_json_file: str):
    ''' open existing json, read to dict, add new dict, write to json'''
    with open(output_json_file, 'r+') as f:
        existing_dict = json.load(f)
        existing_dict.update(new_dict)
        f.seek(0)
        json.dump(existing_dict, f, indent=4)

def ticker_by_keyword(unresolved_tpname: list, tickers_dict: dict) -> dict:
    """
    find keyword in company name and search for relevant ticker in ticker dictionary
    """
    not_keyword = ["the", "inc", "corp", "ltd", "limited", "co", "corporation", "company", "plc", "group", "lp", "holdings", "trust", "laboratories"]
    possible_resolute = {}
    for i in unresolved_tpname:
        for j in i.split():
            if j.lower() not in not_keyword:
                for k in tickers_dict.keys():
                    if j in k:
                        possible_resolute[i] = tickers_dict[k]
                        break
            break # only search for first keyword    
    return possible_resolute

# in main
with open('/mnt/f/Downloads/TradeHistory.csv', 'r') as f:
    df_in = pd.read_csv(f)


total_instruments = len(df_in['Market'].unique())

# def add_ticker(df_in: pd.DataFrame) -> pd.DataFrame:
reference_data_json_file = sys.path[0] + '/company_name_to_ticker.json'

if 'Ticker' not in df_in.columns:
    df_in['Ticker'] = np.nan 
    
# else:
#     print("csv already has ticker in it, no need to add ticker")
#     return df_in

# add ticker from json file
df_in = load_ticker_from_json(reference_data_json_file, df_in)

ttl_resolved_instrument = len(df_in[df_in['Ticker'].notna()]['Market'].unique())
print(f"Total instruments resolved from json file: {ttl_resolved_instrument} out of {total_instruments}")



# add ticker from sec site
sec_tickers = get_sec_tickers()
df_in = match_tickers_dict(sec_tickers, df_in)
ttl_resolved_instrument = len(df_in[df_in['Ticker'].notna()]['Market'].unique())
print(f"Total instruments resolved from sec site: {ttl_resolved_instrument} out of {total_instruments}")
df_resolved = df_in[df_in['Ticker'].notna()]
print(df_resolved.drop_duplicates(subset=['Market', 'Ticker']))
add_ticker_to_json(dict(zip(df_resolved['Market'], df_resolved['Ticker'])), reference_data_json_file)

# add ticker from IG pdf
pdf_tickers = pdf_to_dict('/mnt/f/Downloads/Stockbroking Share List.pdf')
df_in = match_tickers_dict(pdf_tickers, df_in)
ttl_resolved_instrument = len(df_in[df_in['Ticker'].notna()]['Market'].unique())
print(f"Total instruments resolved from json file: {ttl_resolved_instrument} out of {total_instruments}")
df_resolved = df_in[df_in['Ticker'].notna()]
print(df_resolved.drop_duplicates(subset=['Market', 'Ticker']))
add_ticker_to_json(dict(zip(df_resolved['Market'], df_resolved['Ticker'])), reference_data_json_file)


# close match tickers from sec site
close_matched_result = close_matched_tickers(df_in[df_in['Ticker'].isna()]['Market'], sec_tickers)
print(f"{close_matched_result} to be added to dataframe and json file")
df_in['Ticker'] = df_in['Market'].map(close_matched_result).fillna(df_in['Ticker'])
add_ticker_to_json(close_matched_result, reference_data_json_file)

# close match tickers from IG pdf
close_matched_result = close_matched_tickers(df_in[df_in['Ticker'].isna()]['Market'], pdf_tickers, cutoff_ratio=0.66)
print(f"{close_matched_result} to be added to dataframe and json file")
df_in['Ticker'] = df_in['Market'].map(close_matched_result).fillna(df_in['Ticker'])
add_ticker_to_json(close_matched_result, reference_data_json_file)


# resolve by keyword
unresolved_company_name = df_in[df_in['Ticker'].isna()]['Market'].unique()
keyword_resolution = ticker_by_keyword(unresolved_company_name, sec_tickers)
df_in['Ticker'] = df_in['Market'].map(keyword_resolution).fillna(df_in['Ticker'])
add_ticker_to_json(keyword_resolution, reference_data_json_file)


# check if there is any unresolved company name
unresolved_company_name = df_in[df_in['Ticker'].isna()]['Market'].unique()
print(f"Unresolved company name: {unresolved_company_name}")
