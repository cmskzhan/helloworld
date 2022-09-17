import streamlit as st
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import json
import re

def position_calculation(df_in: pd.DataFrame) -> dict:
    """Calculate the position and cost basis of a stock"""
    position = df_in['Quantity'].sum()
    DollarCost = (df_in['Quantity'] * df_in['Price']).sum() + df_in['Charges'].sum()
    # DollarCost_per_share = DollarCost / position
    GBPCost = ((df_in['Quantity'] * df_in['Price'] + df_in['Charges']) * df_in['Conversion rate'] - df_in['Commission']).sum()
    # GBPCost_per_share = GBPCost / position
    return {'position': position, 'DollarCost': DollarCost, 'GBPCost': GBPCost}

def add_ticker(df_in: pd.DataFrame) -> pd.DataFrame:
    ''' find ticker through 
    1. json file
    2. sec site
    3. ig pdf
    4. close match
    5. if not found, return empty string and throw up err
    6. for new ticker found through 2,3,4, add to json file'''
    
    df_in['Ticker'] = np.nan #create a new column for ticker

    # load known ticker to column
    with open('ticker.json') as f:  # TODO: replace json file with correct path
        ticker_dict = json.load(f)
    for k, v in ticker_dict.items():
        df_in.loc[df_in['Market'] == k, 'Ticker'] = v
    
    # find unknown ticker through sec site
    # get ticker is nan
    df_unkonw_symbol = df_in[df_in['Ticker'].isna()]
    if len(df_unkonw_symbol) > 0:
        # search on sec site
        sec_site_mapping = pd.read_json(r'https://www.sec.gov/files/company_tickers.json', orient='index')
        sec_site_mapping['Company Name'] = sec_site_mapping['title'].str.lower()
        sec_site_mapping['Company Name'] = sec_site_mapping['Company Name'].str.replace('\.', '')
        sec_site_mapping['Company Name'] = sec_site_mapping['Company Name'].str.replace('\,', '')
        no_tikcer_company_list = df_unkonw_symbol['Market'].str.lower().unique()
        company_name_to_ticker = {}
        for i in list(map(lambda x: re.sub(r"\s\(.*\)","",x), no_tikcer_company_list)): # remove (*) from company name
            if i in sec_site_mapping['Company Name'].values: # if no_ticker_list matchs lower case company name matches 
                company_name_to_ticker[i] = sec_site_mapping[sec_site_mapping['Company Name'] == i]['ticker'].values[0]
        # add ticker to df
        for k, v in company_name_to_ticker.items():
            df_in.loc[df_in['Market'] == k, 'Ticker'] = v
        # add ticker to json file
        with open('ticker.json', 'a') as f: # TODO: replace json file with correct path
            json.dump(company_name_to_ticker, f)
    # TODO: unit test this function
    return df_in



def threeTabs():
    st.title("My Portfolio")


    tab1, tab2, tab3 = st.tabs(["Positions", "Fire", "P&L"])

    with tab1:
        st.header("Upload Trade/Transaction History")
        uploaded_file = st.file_uploader('''\
        Upload your trade/transaction history in CSV format. Filename must be in the format of: \n
        1. trade file must have filename start with Trade*.csv \n
        2. transaction file must have filename start with Transaction*.csv''', type=["csv"], accept_multiple_files=True)
        if uploaded_file is not None:
            for f in uploaded_file:
                if f.name.startswith("Trade") and f.name.endswith(".csv"):
                    df_trade_history = pd.read_csv(f)
                    st.subheader("latest trade history")
                    st.dataframe(df_trade_history.head(3))

                    market_list = df_trade_history['Market'].unique()
                    all_positions = pd.DataFrame()
                    for stock in market_list:
                        stock_position = position_calculation(df_trade_history[df_trade_history['Market'] == stock])
                        stock_position['Stock'] = stock                        
                        #all_positions = all_positions.append(stock_position, ignore_index=True)
                        all_positions = pd.concat([all_positions, pd.DataFrame.from_dict(stock_position, orient='index').T], ignore_index=True)
                        
                    all_positions.set_index('Stock', inplace=True)
                    all_positions.sort_values(by='position', ascending=False, inplace=True)
                    st.write(all_positions)

                    #create a dropdown list of unique market
                    market = st.selectbox("Select Stock", market_list)
                    st.subheader("Trade history for {}".format(market))
                    st.dataframe(df_trade_history[df_trade_history['Market'] == market])


                elif f.name.startswith("Transaction") and f.name.endswith(".csv"):
                    df_transactions = pd.read_csv(f)
                    st.subheader("latest transaction history")
                    st.write(df_transactions.head())

                    df_transactions['PL Amount'] = df_transactions['PL Amount'].str.replace(',','')
                    type_dict = {'Date': 'datetime64', 'PL Amount': 'float', 'Summary': 'category', 'Transaction type': 'category', 'Cash transaction': 'boolean', 'MarketName': 'string'}
                    df_transactions = df_transactions.astype(type_dict)
                    df_transactions['Date'] = pd.to_datetime(df_transactions['Date'], format='%Y-%m-%d')
                    df_transactions.set_index('Date', inplace=True)
                    df_cashIn = df_transactions[(df_transactions['Summary']=='Cash In') | (df_transactions['MarketName'] == 'Bank Deposit')]
                    df_cashIn.rename(columns={'ProfitAndLoss': 'Deposits'}, inplace=True)
                    st.metric(label="Total Cash Deposit in GBP", value=df_cashIn['PL Amount'].sum())
                    with st.expander("Cash In Details"):
                        st.table(df_cashIn['Deposits'])
                    
                    
                else:
                    st.write("filename must begin with 'Trades' or 'Transaction' and format must be a csv")
            
        else:
            st.error("no file uploaded")
        



    with tab2:
        st.header("Financial Independence and Retire Early")
        # isa_annual_contrib = 20000
        # current_ttl = 86700
        # if df_transactions exists
        if 'df_transactions' in locals():
            st.write("df_transactions exists in local")
            st.metric(label="Current available cash in GBP", value=df_transactions['PL Amount'].sum())

        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


# def main():
#     pass

if __name__ == "__main__":
    threeTabs()