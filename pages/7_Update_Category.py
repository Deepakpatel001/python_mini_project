import streamlit as st
import mysql.connector
def db_cnx():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Night@123",
        database="ecommerce_management"
    )
    return mydb


def data_cat_update():

    st.text_input("Category Id", key="update_category_id")
    if st.session_state.update_category_id:
        mydb = db_cnx()

        cnx = mydb.cursor()
        cnx.execute("select * from category")
        old_data = cnx.fetchall()
        st.text_input("Category Name", key="update_category_name",value=old_data[0][1])
    fetch = st.button("Fetch",key="fetch")
    if fetch:
        update_category_id = st.session_state.update_category_id
        update_category_name = st.session_state.update_category_name
        update_btn = st.button("Update", key="update_btn")
        if update_btn:
            if update_category_id == "":
                st.error("Enter a category Id")
            else:
                mydb = db_cnx()
                cnx = mydb.cursor()
                sql = "UPDATE category SET category_Name = %s"
                data1 = (str(update_category_name))
                cnx.execute(sql,data1)
                mydb.commit()
                st.success("Category updated ")
                mydb.close()



st.title("Update a category")
st.text_input("category id", key="search_category_id")
search_btn = st.button("Search", key="search_btn", type="primary")
data = ""

if st.session_state.search_btn:
    search_category_id = st.session_state.search_category_id
    if search_category_id == "":
        st.error("Enter a Category Id")
    else:
        mydb = db_cnx()
        cnx = mydb.cursor()
        cnx.execute(f"select * from category where category_id = {search_category_id}")
        data = cnx.fetchall()
        if data:
            st.success("category found")


pages = {
    0 : data_cat_update
}

if "current" not in st.session_state:

    st.session_state.current = None

if st.session_state.search_btn:
    st.session_state.current = 0
if st.session_state.current != None:
    pages[st.session_state.current]()



