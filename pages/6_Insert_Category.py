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


def insert_Category():

    st.title("Insert a category:")
    st.text_input("Category Id:",key="insert_category_id")
    st.text_input("Category Name:",key="insert_category_name")
    insert_btn = st.button("Add")
    insert_category_id = st.session_state.insert_category_id
    insert_category_name = st.session_state.insert_category_name

    if insert_btn:
        mydb = db_cnx()
        cnx = mydb.cursor()
        sql = f"select * from category where category_id = {insert_category_id}"
        cnx.execute(sql)
        data1 = cnx.fetchall()
        if data1:
            st.error("Category Id already found")
        else:
            sql = "INSERT INTO category(Category_id,Category_Name) VALUES (%s, %s)"
            data1 = (int(insert_category_id), str(insert_category_name))
            data = cnx.execute(sql, data1)
            mydb.commit()
            st.success("Category Added ")
        mydb.close()

insert_Category()