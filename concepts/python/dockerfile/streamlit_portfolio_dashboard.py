import streamlit as st
import pandas as pd


def threeTabs():
    st.title("My Portfolio")


    tab1, tab2, tab3 = st.tabs(["Positions", "Cash", "P&L"])

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
                    st.dataframe(df_trade_history.head(9))
                elif f.name.startswith("Transaction") and f.name.endswith(".csv"):
                    df_transaction_history = pd.read_csv(f)
                    st.subheader("latest transaction history")
                    st.write(df_transaction_history.head(9))
                else:
                    st.write("filename must begin with 'Trades' or 'Transaction' and format must be a csv")
            
        else:
            st.error("no file uploaded")
        



    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


# def main():
#     pass

if __name__ == "__main__":
    threeTabs()