import streamlit as st
import mysql.connector

st.title("Delete a Category")
def db_cnx():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Night@123",
        database="ecommerce_management"
    )
    return mydb
def del_category():
    st.text_input("Category", key='del_category_id')
    del_category_btn = st.button("Delete")
    if del_category_btn:
        categorys_id = int(st.session_state.del_category_id)
        mydb = db_cnx()
        cnx = mydb.cursor()
        print(f"delete from category where category_id = {categorys_id}")
        cnx.execute(f"select * from category where category_id = {categorys_id}")
        data = cnx.fetchall()
        if data:
            cnx.execute(f"delete from category where category_id = {categorys_id}")
            st.success(f"category deleted Id is '{data[0][0]}' and category name is '{data[0][1]}''")
        else:
            st.error("Id not Found")

        mydb.commit()
        mydb.close()

del_category()