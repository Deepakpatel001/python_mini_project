import streamlit as st
import mysql.connector

st.title("Delete a product")
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

def del_product():
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = "select Product_Id,Product_Name from  product"
    cnx.execute(sql)
    data1 = cnx.fetchall()
    cnx.close()
    CHOICES = dict((x, y) for x, y in data1)
    option = st.selectbox("Product Category", options=list(CHOICES.keys()), format_func=format_func)
    # st.text_input("Product_ID", key='del_product_id')
    del_product_btn = st.button("Delete")
    if del_product_btn:
        # products_id = int(st.session_state.del_product_id)
        mydb = db_cnx()
        cnx = mydb.cursor()
        cnx.execute(f"select * from Product where Product_Id = {option}")
        data = cnx.fetchall()
        if data:
            cnx.execute(f"delete from Product where Product_Id = {option}")
            st.success("Product deleted")
        else:
            st.error("Id not Found")

        mydb.commit()
        mydb.close()

mydb = db_cnx()
cnx = mydb.cursor()
sql = "select Product_Id,Product_Name from  product"
cnx.execute(sql)
data1 = cnx.fetchall()
cnx.close()
print(data1)
CHOICES = dict((x, y) for x, y in data1)
del_product()