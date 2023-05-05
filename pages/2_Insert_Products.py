import streamlit as st
import mysql.connector
import pandas as pd

def db_cnx():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Night@123",
        database="ecommerce_management"
    )
    return mydb


def format_func(option):
    return CHOICES[option]




def insert_products():
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = f"select * from  category"
    cnx.execute(sql)
    data1 = cnx.fetchall()
    cnx.close()
    print(data1)
    CHOICES = dict((x, y) for x, y in data1)


    st.title("Insert a product:")
    st.text_input("Product Id:", key="insert_product_id")
    st.text_input("Product Name:", key="insert_product_name")
    option = st.selectbox("Product Category", options=list(CHOICES.keys()), format_func=format_func)
    # st.text_input("Product Category:", key="insert_product_category")
    st.text_input("Product Price:", key="insert_product_price")
    insert_btn = st.button("Add")
    insert_product_id = st.session_state.insert_product_id
    insert_product_name = st.session_state.insert_product_name
    # insert_product_category = st.session_state.insert_product_category
    insert_product_category = option
    insert_product_price = st.session_state.insert_product_price
    if insert_btn:
        if (insert_product_id.isnumeric() and insert_product_name.isalpha()):
            mydb = db_cnx()
            cnx = mydb.cursor()
            sql = f"select * from  product where product_id = {insert_product_id}"
            cnx.execute(sql)
            data1 = cnx.fetchall()
            if data1:
                st.error("product Id already found")
            else:
                sql = "INSERT INTO product(Product_Id,Product_Name,Category_Id,Price)VALUES (%s, %s, %s, %s)"
                data1 = (int(insert_product_id), str(insert_product_name), str(insert_product_category), float(insert_product_price))
                cnx.execute(sql,data1)
                mydb.commit()
                st.success("Product Added ")
            mydb.close()
        else:
            st.error("Check the input format")


mydb = db_cnx()
cnx = mydb.cursor()
sql = f"select * from  category"
cnx.execute(sql)
data1 = cnx.fetchall()
cnx.close()
print(data1)
CHOICES = dict((x, y) for x, y in data1)

insert_products()
