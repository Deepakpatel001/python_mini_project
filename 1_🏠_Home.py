import streamlit as st
import mysql.connector
from streamlit_extras.switch_page_button import switch_page
from cryptography.fernet import Fernet

# database connection started here

def db_cnx():
    mydb = mysql.connector.connect(
        host="localhost",
        user="ecommerce",
        password="Strom@123",
        database="ecommerce_management_1"
    )
    return mydb

# login session started here
def login():
    st.text_input("User Name:", key="user_name", placeholder="John_Doe")
    st.text_input("Password:", key="password", type="password", placeholder="Password")
    login_btn = st.button("Login")

    if login_btn:
        user_name = st.session_state.user_name
        password = st.session_state.password
        mydb = db_cnx()
        cnx = mydb.cursor()
        cnx.execute(f"select * from account where User_Name = '{user_name}' and Status = 'Active'")
        data = cnx.fetchall()
        cnx.close()
        if data:
            passwd = data[0][2]
            passwd = passwd.encode() # password encoded
            key = b'j8rS20etwOw1qH8XeznLLz_tpmwEUuXhKUs_oS8XgOY='
            cipher = Fernet(key)
            passwd = (cipher.decrypt(passwd)).decode()
            st.success(passwd)
            if passwd == password:
                if 'Logged_Username' not in st.session_state:
                    st.session_state['Logged_Username'] = data[0][1]
                    st.session_state['User_Role'] = data[0][4]
                    st.session_state['User_id'] = data[0][0]
                switch_page("Product")
            else:
                st.error("Incorrect User name or Password")
        else:
            st.error("Incorrect User name or Password")


def add_customer():
    col3, col4 = st.columns(2)
    with col3:
        st.text_input("First Name:", key="add_first_name",placeholder="John")
        st.text_input("Mobile Number:", key="add_mob_number", max_chars=10, placeholder="XXXXXXXXX")

    with col4:
        st.text_input("Last Name:", key="add_last_name",placeholder="Doe")
        st.text_input("Email:", key="add_email", placeholder="XXXXXXX@gmail.com")




    col5, col6 = st.columns(2)
    with col5:
        st.text_input("username:", key="add_user_name",placeholder="John_Doe")
        st.text_input("Password:", key="add_password",type="password",placeholder="Password")
        st.text_input("Confirm Password:", key="add_confirm_password",type="password",placeholder="Password")
        add_btn = st.button("Create an Account")
    with col6:
        if st.session_state.add_mob_number != '':
            mydb = db_cnx()
            cnx = mydb.cursor()
            cnx.execute(f"select * from customers where Customer_Number = '{st.session_state.add_mob_number}'")
            add_mob_number_msg = cnx.fetchall()
            cnx.close()
            if add_mob_number_msg:
                st.error('Mobile number already used', icon="❌")
        if st.session_state.add_email != '':
            mydb = db_cnx()
            cnx = mydb.cursor()
            cnx.execute(f"select * from customers where Customer_Email = '{st.session_state.add_email}'")
            add_email_msg = cnx.fetchall()
            cnx.close()
            if add_email_msg:
                st.error('Email already used', icon="❌")
        if st.session_state.add_user_name != '':
            mydb = db_cnx()
            cnx = mydb.cursor()
            cnx.execute(f"select * from account where User_Name = '{st.session_state.add_user_name}'")
            data = cnx.fetchall()
            cnx.close()

            if data:
                st.error('Username already taken', icon="❌")
            else:
                st.success('Username available', icon="✔")
        else:
            st.info('Choose Username', icon="ℹ")

        if st.session_state.add_password != st.session_state.add_confirm_password:
            st.error('Password and confirm password not matched', icon="ℹ")

    if add_btn:
        add_user_name = st.session_state.add_user_name
        add_password = st.session_state.add_password
        add_confirm_password = st.session_state.add_confirm_password
        add_first_name = st.session_state.add_user_name
        add_last_name = st.session_state.add_last_name
        add_mob_number = st.session_state.add_mob_number
        add_email = st.session_state.add_email


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
                sql2 = f"Select * from customers where Customer_Email = '{add_email}'"
                cnx.execute(sql2)
                acc_data_email = cnx.fetchall()
                sql2 = f"Select * from customers where Customer_Number = '{add_mob_number}'"
                cnx.execute(sql2)
                acc_data_email = cnx.fetchall()
                if acc_data and acc_data_email and add_mob_number:
                    st.error("User name already exist try another user name")
                else:
                    sql = """INSERT INTO account (User_Name, Password, Old_Password, Role)
                    VALUES
                    (%s, %s, %s, %s);"""
                    sql2 = """
                    INSERT INTO customers (User_Id, Customer_First_Name, Customer_Last_Name, Customer_Number, Customer_Email)
                    VALUES
                    ((SELECT User_id FROM account WHERE user_name = %s), %s, %s, %s, %s)"""
                    data1 = (str(add_user_name), str(passwd),str(passwd), 'Customer')
                    data2 = (str(add_user_name),str(add_first_name),str(add_last_name), int(add_mob_number), str(add_email))
                    cnx.execute(sql, data1)
                    cnx.execute(sql2, data2)
                    mydb.commit()
                    mydb.close()
                    st.success("Account Created please Login")
        else:
            st.error("Passwords do not match.")


def login_auth():
    if 'Logged_Username' not in st.session_state:
        st.subheader("Login")
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            login()

        with tab2:
            add_customer()
    else:
        st.success("You already logged in")


if ('Logged_Username' in st.session_state) and ('User_Role' in st.session_state):
    col1, col2 = st.columns(2)
    with col1:
        st.write("Hello", st.session_state.Logged_Username, "(", st.session_state.User_Role, ")")
    with col2:
        logout = st.button("Logout")
        if logout:
            del st.session_state.Logged_Username
            del st.session_state.User_Role
            switch_page("Home")
st.title("Welcome to Ecommerce Website")
st.image("banner.jpg")
login_auth()
