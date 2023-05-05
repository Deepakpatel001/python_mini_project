import streamlit as st
import mysql.connector
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid

def db_cnx():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Night@123",
        database="ecommerce_management"
    )
    return mydb


def products():
    mydb = db_cnx()

    cnx= mydb.cursor()
    cnx.execute("select * from Product")
    df = pd.DataFrame(cnx)
    df = df.rename(columns={0: 'Product_Id', 1: 'Product_Name', 2: 'Category_Id', 3: 'Price'})
    gb = GridOptionsBuilder.from_dataframe(df)

    gridoptions = gb.build()

    AgGrid(
        df,
        gridOptions=gridoptions,
    )

st.title("View all Products: ")
products()