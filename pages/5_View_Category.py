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


def Category():
    mydb = db_cnx()
    cnx = mydb.cursor()
    cnx.execute("select * from category")
    df = pd.DataFrame(cnx)
    df = df.rename(columns={0: 'Category_Id', 1: 'Category_Name'})
    gb = GridOptionsBuilder.from_dataframe(df)

    gridoptions = gb.build()

    AgGrid(
        df,
        gridOptions=gridoptions,
        fit_columns=False,
    )
st.title("View all Category: ")
Category()