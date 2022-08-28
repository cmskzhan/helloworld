import streamlit as st

st.title("session state simple examples")

"current session state values changes", st.session_state

# def lbs_to_kg2():
#     lbs = st.text_input("Enter weight in lbs")
#     kg = float(lbs) * 0.453592
#     st.write(f"{lbs} lbs is {kg} kg")

# def kg_to_lbs2():
#     kg = st.text_input("Enter weight in kg")
#     lbs = float(kg) * 2.20462
#     st.write(f"{kg} kg is {lbs} lbs")

def lbs_to_kg():
    st.session_state.kg = st.session_state.lbs/2.20462

def kg_to_lbs():
    st.session_state.lbs = st.session_state.kg * 2.20462


col1, buff, col2 = st.columns(3)
with col1:
    pounds = st.number_input("pounds", key="lbs", on_change=lbs_to_kg)

with col2:
    kilogram = st.number_input("kilogram", key="kg", on_change=kg_to_lbs)


# def form_callback():
#     st.write(st.session_state.my_slider)
#     st.write(st.session_state.my_checkbox)

if st.button("show form"):

    with st.form(key='my_form'):
        slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
        checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
        # submit_button = st.form_submit_button(label='Submit', on_click=form_callback)
        submit_button = st.form_submit_button(label='Submit')