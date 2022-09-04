import streamlit as st
from .streamlit_portfolio_dashboard import threeTabs as dashboard

login_details = {
  "credentials": {
    "usernames": {
      "jsmith": {
        "email": "kaizhang@yahoo.com",
        "name": "John Smith",
        "password": 123
      },
      "rbriggs": {
        "email": "rbriggs@gmail.com",
        "name": "Rebecca Briggs",
        "password": 456
      }
    }
  },
  "cookie": {
    "expiry_days": 1,
    "key": "some_signature_key",
    "name": "cookie_name_streamlit_authenticator"
  },
  "preauthorized": {
    "emails": [
      "abc@gmail.com"
    ]
  }
}

st.title("login")
with st.form(key='login'):
    username = st.text_input(label='username')
    password = st.text_input(label='password', type='password')
    submit_button = st.form_submit_button(label='Login')
    if submit_button:
        if username in login_details["credentials"]["usernames"]:
            if password == login_details["credentials"]["usernames"][username]["password"]:
                st.success("Login successful")
                dashboard()
            else:
                st.error("Login failed")