import streamlit as st
import mysql.connector
from streamlit_extras.switch_page_button import switch_page
from cryptography.fernet import Fernet

st.set_page_config(page_title='Admin Registration', page_icon="random")


def db_cnx():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Akshay123@",
        database="ecommerce_management"
    )
    return mydb


def click_home():
    switch_page("Home")


def add_admin():  # added this function to register admins
    col3, col4 = st.columns(2)
    with col3:
        st.text_input("username:", key="admin_new_user_name", placeholder="xyz123")
        st.text_input("Password:", key="admin_new_password", type="password", placeholder="Password")
        st.text_input("Confirm Password:", key="admin_confirm_password", type="password", placeholder="Confirm Password")

    with col4:
        if st.session_state.admin_new_user_name != '':
            mydb = db_cnx()
            cnx = mydb.cursor()
            cnx.execute(f"select * from account where User_Name = '{st.session_state.admin_new_user_name}'")
            data = cnx.fetchall()
            cnx.close()

            if data:
                st.error('Username already taken', icon="❌")
            else:
                st.success('Username available', icon="✔")
        else:
            st.info('Choose Username', icon="ℹ")

    col5, col6 = st.columns(2)
    with col5:
        st.text_input("Mobile Number:", key="admin_mob_number", max_chars=10, placeholder="XXXXXXXXX")
        st.text_input("Email:", key="admin_email", placeholder="XXXXXXX@admin.com")
        add_btn = st.button("Create Admin Account")
    with col6:
        if st.session_state.admin_mob_number != '':
            mydb = db_cnx()
            cnx = mydb.cursor()
            cnx.execute(f"select * from customers where Customer_Number = '{st.session_state.admin_mob_number}'")
            admin_mob_number_msg = cnx.fetchall()
            cnx.close()
            if admin_mob_number_msg:
                st.error('Mobile number already used', icon="❌")
        if st.session_state.admin_email != '':
            mydb = db_cnx()
            cnx = mydb.cursor()
            cnx.execute(f"select * from customers where Customer_Email = '{st.session_state.admin_email}'")
            admin_email_msg = cnx.fetchall()
            cnx.close()
            if admin_email_msg:
                st.error('Email already used', icon="❌")

        if st.session_state.admin_new_password != st.session_state.admin_confirm_password:
            st.error('Password and confirm password not matched', icon="ℹ")

    if add_btn:
        add_user_name = st.session_state.admin_new_user_name
        add_password = st.session_state.admin_new_password
        add_confirm_password = st.session_state.admin_confirm_password
        add_mob_number = st.session_state.admin_mob_number
        add_email = st.session_state.admin_email

        if add_password == add_confirm_password:
            passwd = add_password
            passwd = passwd.encode()
            key = b'j8rS20etwOw1qH8XeznLLz_tpmwEUuXhKUs_oS8XgOY='
            cipher = Fernet(key)
            passwd = (cipher.encrypt(passwd)).decode()
            mydb = db_cnx()
            cnx = mydb.cursor()
            sql = f"Select * from account where user_name = '{add_user_name}'"
            cnx.execute(sql)
            acc_data = cnx.fetchall()
            sql2 = f"Select * from admin where mail_id = '{add_email}'"
            cnx.execute(sql2)
            acc_data_email = cnx.fetchall()
            sql2 = f"Select * from admin where phone_number = '{add_mob_number}'"
            cnx.execute(sql2)
            acc_mob_number = cnx.fetchall()  # changed acc_data_email to acc_mob_number
            if acc_data and acc_data_email and acc_mob_number:
                st.error("User name already exist try another user name")
            else:
                sql = """INSERT INTO account (User_Name, Password, Old_Password, Role)
                    VALUES
                    (%s, %s, %s, %s);"""
                sql2 = """
                    INSERT INTO admin (User_Id, admin_username, phone_number, mail_id)
                    VALUES
                    ((SELECT User_id FROM account WHERE User_Name = %s), %s, %s, %s);"""

                data1 = (str(add_user_name), str(passwd), str(passwd), 'Admin')
                data2 = (str(add_user_name), str(add_user_name), int(add_mob_number), str(add_email))
                cnx.execute(sql, data1)
                cnx.execute(sql2, data2)
                mydb.commit()
                mydb.close()
                st.success("Account Created please Login")
                st.button("Click here to go to home", on_click=click_home)

        else:
            st.error("Passwords do not match.")


registration_key = '1234'


def admin_auth():
    if 'Logged_Username' not in st.session_state:
        add_admin()
    else:
        st.success("You are already logged in")
        st.button("Click here to go to home", on_click=click_home)


st.title("Welcome to Admin Registration")
st.image("banner_4.jpg")
admin_auth()
if ('Logged_Username' in st.session_state) and ('User_Role' in st.session_state):
    switch_page('Home')
