# https://github.com/mkhorasani/Streamlit-Authenticator
import streamlit as st
import streamlit_authenticator as stauth

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

# update login details with hashed password
for i in login_details["credentials"]["usernames"]:
    login_details["credentials"]["usernames"][i]["password"] = stauth.Hasher([str(login_details["credentials"]["usernames"][i]["password"])]).generate()[0]
# pprint.pprint(login_details["credentials"])


authenticator = stauth.Authenticate(credentials=login_details['credentials'], cookie_name="streamlit_authenticator", key="streamlit_authenticator" ,cookie_expiry_days=1)
# create a login widget in main screen
name, authentication_status, username = authenticator.login('Login', 'main')

# forgot username/password widget
# def forgot_username_password_button(user_pass: str):
#     try:
#         if user_pass == "username":
#             username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
#             if username_forgot_username:
#                 st.success("Username sent to email")
#                 st.write(username_forgot_username, email_forgot_username)
#             elif username_forgot_username is False:
#                 st.error("Email not found")
#             st.write(f"username_forgot_username : ", {username_forgot_username}, "email_forgot_username",  {email_forgot_username})
#             st.write(username_forgot_username, email_forgot_username)

#         else:
#             username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
#             #print(f"username_forgot_pw : ", {username_forgot_pw}, "email_forgot_password:",  {email_forgot_password}, "random_password:", {random_password})
#             if username_forgot_pw:
#                 st.success("Password sent to email")
#             elif username_forgot_pw is False:
#                 st.error("Username not found")
#     except Exception as e:
#         st.error(e)

def forgot_username_button(auth):
    try:
        username_forgot_username, email_forgot_username = auth.forgot_username('Find my username')

        if username_forgot_username:
            return st.success('Username sent securely')
            # Username to be transferred to user securely
        elif username_forgot_username == False:
            return st.error('Email not found')
        print(username_forgot_username, email_forgot_username)
    except Exception as e:
        return st.error(e)
    

if not authentication_status:
    if st.button("forgot username"):
        forgot_username_button(authenticator)
    # if st.button("forgot password"):
    #     forgot_username_password_button("password")



# # if the user is logged in, create a logout button, else...
# if authentication_status:
#     authenticator.logout('Logout', 'main')
#     st.write(f"Hello {username}")
#     st.title("Streamlit Authenticator landing page")
# elif authentication_status is False:
#     st.error("incorrect username or password")
# elif authentication_status is None:
#     st.warning("Enter username and password")

# retrieve session state through st.session_state["name"], st.session_state["authentication_status"], and st.session_state["username"]
if st.session_state["authentication_status"]:
    st.write(f"Hello session user {st.session_state['username']}")
    st.title("Streamlit Authenticator session landing page")
    authenticator.logout('Logout', 'main')
elif st.session_state["authentication_status"] is False:
    st.error("incorrect session username or password")
elif st.session_state["authentication_status"] is None:
    st.warning("Enter your session username and password")


# password reset widget
def reset_password_button():
        try:
            if authenticator.reset_password(username, 'Reset Password', 'sidebar'):
                st.success("Password reset successful")
        except Exception as e:
            st.error(e)

# place a st button and call reset_password_button()
if authentication_status:
    if st.button("Reset Password"):
        reset_password_button()

