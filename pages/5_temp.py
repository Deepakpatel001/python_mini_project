import streamlit as st

def button_one():
    st.text_input("1",key="hey")
    st.text_input("2")
    if st.button("submit"):
        st.write(st.session_state.hey)

pages = {
    0 : button_one,
}

A = st.button("A")
if "current" not in st.session_state:

    st.session_state.current = None
# Now you can set the button click to a number and call the linked function
if A:
    st.session_state.current = 0
if st.session_state.current != None:
    pages[st.session_state.current]()