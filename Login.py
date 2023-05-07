import streamlit as st
import mysql.connector
from streamlit_extras.switch_page_button import switch_page

def db_cnx():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Night@123",
        database="ecommerce_management"
    )
    return mydb

def login():
    st.image("banner.jpg")
    st.title("Login")
    st.text_input("userId",key="user_id")
    st.text_input("Password",key="password",type="password")
    login_btn = st.button("Login")

    if login_btn:
        userId = st.session_state.user_id
        password = st.session_state.password
        mydb = db_cnx()
        cnx = mydb.cursor()
        cnx.execute(f"select * from Admin where User_Id = '{userId}' and Password = '{password}'")
        data = cnx.fetchall()
        if data:
            st.success("Logged In")
            if 'Logged_Username' not in st.session_state:
                st.session_state['Logged_Username'] = data[0][1]
                st.session_state['User_Role'] = data[0][4]
            switch_page("Product")
        else:
            st.error("Incorrect User name or Password")

def login_auth():
    if 'Login' not in st.session_state:
        login()
    else:
        switch_page("view_products")
        st.success("You already logged in")

login_auth()

