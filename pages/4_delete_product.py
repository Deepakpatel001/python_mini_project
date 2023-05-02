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
def del_product():
    st.text_input("Product_ID", key='del_product_id')
    del_product_btn = st.button("Delete")
    if del_product_btn:
        products_id = int(st.session_state.del_product_id)
        mydb = db_cnx()
        cnx = mydb.cursor()
        cnx.execute(f"select * from Product where product_id = {products_id}")
        data = cnx.fetchall()
        if data:
            cnx.execute(f"delete from Product where product_id = {products_id}")
            st.success(f"Product deleted Id is '{data[0][0]}' and product name is '{data[0][1]}''")
        else:
            st.error("Id not Found")

        mydb.commit()
        mydb.close()

del_product()