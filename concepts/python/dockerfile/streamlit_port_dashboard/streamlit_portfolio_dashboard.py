import streamlit as st
import pandas as pd
import ticker_resolution as tr
import sys
import os

def replace_duplicated_ticker(df_in: pd.DataFrame) -> pd.DataFrame:
    """Due to corp events such as SPAC conversion, ticker may change. 
    This function will call the add_ticker function and update company name that has the same ticker to the latest company name
    The dataframe then would be ready for the position calculation"""
    
    df = tr.add_ticker(df_in).sort_values('Settlement date', ascending=False)
    df_find_dup_ticker = df[['Ticker','Market', 'Settlement date']].drop_duplicates(subset=['Ticker','Market'], keep='first')

    df_find_dup_ticker = df_find_dup_ticker[df_find_dup_ticker.duplicated(subset=['Ticker'], keep=False)].sort_values('Settlement date', ascending=False)
    df_find_dup_ticker = df_find_dup_ticker.reset_index(drop=True)
    for i in df_find_dup_ticker['Market'][1:len(df_find_dup_ticker)]:
        print(f"{df_find_dup_ticker['Market'][0]} to replace {i}")
        df.loc[df['Market'] == i, 'Market'] = df_find_dup_ticker['Market'][0]
    return df

def openPositions(df_in: pd.DataFrame) -> pd.DataFrame:
    """Calculate open position for each ticker"""
    df = replace_duplicated_ticker(df_in)
    df['Open Position $'] = df['Quantity'] * df['Price'] /100
    df_op = df.groupby(['Ticker','Market']).sum().sort_values('Open Position $', ascending=False)
    return df_op


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
                    df_trade_history['Settlement date'] = pd.to_datetime(df_trade_history['Settlement date'], format='%d-%m-%Y')
                    st.subheader("latest trade history")
                    st.dataframe(df_trade_history.head(3))

                    st.subheader("Open Positions")
                    st.write(openPositions(df_trade_history))
                    # market_list = df_trade_history['Market'].unique()
                    # all_positions = pd.DataFrame()
                    # for stock in market_list:
                    #     stock_position = position_calculation(df_trade_history[df_trade_history['Market'] == stock])
                    #     stock_position['Stock'] = stock                        
                    #     #all_positions = all_positions.append(stock_position, ignore_index=True)
                    #     all_positions = pd.concat([all_positions, pd.DataFrame.from_dict(stock_position, orient='index').T], ignore_index=True)
                        
                    # all_positions.set_index('Stock', inplace=True)
                    # all_positions.sort_values(by='position', ascending=False, inplace=True)
                    # st.write(all_positions)

                    #create a dropdown list of unique market
                    market_list = df_trade_history['Market'].unique()
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