import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.write("Random number to prove that the app has run: " + str(random.randint(1, 1000)))

@st.cache
def skipCompute():
    # ---- Creating Dictionary ----
    _dic = { 'Name': ['Mango', 'Apple', 'Banana'],
            'Quantity': [45, 38, 90]}
    
    _df = pd.DataFrame(_dic)
    st.info('Dataframe created, see 1 time')
    return _df

#load = st.button('Load Data')
load = st.checkbox('Load Data')
if load:
    df = skipCompute()

st.write(df)
# Initialize session state
if "load_state" not in st.session_state:
    st.session_state.load_state = False

if load or st.session_state.load_state:
   st.session_state.load_state = True
   
   
   # ---- Plot types -------
   opt = st.radio('Plot type :',['Bar', 'Pie'])
   if opt == 'Bar':
      fig = px.bar(df, x= 'Name',
                   y = 'Quantity',title ='Bar Chart')
      st.plotly_chart(fig)
   
   else:     
      fig = px.pie(df,names = 'Name',
                   values = 'Quantity',title ='Pie Chart')
      st.plotly_chart(fig)
