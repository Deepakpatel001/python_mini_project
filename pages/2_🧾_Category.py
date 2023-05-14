import time
import streamlit as st
import mysql.connector
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid
from streamlit_extras.switch_page_button import switch_page

if 'Logged_Username' not in st.session_state:
    switch_page("Home")


if ('Logged_Username' in st.session_state) and ('User_Role' in st.session_state):
    col1,col2 = st.columns(2)
    with col1:
        st.write("Hello", st.session_state.Logged_Username, "(", st.session_state.User_Role, ")")
    with col2:
        logout = st.button("Logout")
        if logout:
            del st.session_state.Logged_Username
            del st.session_state.User_Role
            switch_page("Home")
st.image("banner_3.jpg")


def db_cnx():
    mydb = mysql.connector.connect(
        host="localhost",
        user="ecommerce",
        password="Strom@123",
        database="ecommerce_management"
    )
    return mydb


def format_func(option):
    return CHOICES[option]


def Category():
    Refresh_btn = st.button("Refresh Table")
    if Refresh_btn:
        st.experimental_rerun()
    st.title("View all Category: ")
    mydb = db_cnx()
    cnx = mydb.cursor()
    cnx.execute("select * from category")
    df = pd.DataFrame(cnx)
    mydb.close()
    df = df.rename(columns={0: 'Category_Id', 1: 'Category_Name'})
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=True)

    gridoptions = gb.build()

    AgGrid(
        df,
        gridOptions=gridoptions,
        fit_columns=False,
    )


def insert_Category():

    st.title("Insert a category:")
    st.text_input("Category Id:", key="insert_category_id", placeholder="123")
    st.text_input("Category Name:", key="insert_category_name", placeholder="Fruits")
    insert_btn = st.button("Add")
    insert_category_id = st.session_state.insert_category_id
    insert_category_name = st.session_state.insert_category_name

    if insert_btn:
        mydb = db_cnx()
        cnx = mydb.cursor()
        sql = f"select * from category where category_id = {insert_category_id}"
        cnx.execute(sql)
        data1 = cnx.fetchall()
        cnx.close()
        if data1:
            st.error("Category Id already exist")
        else:
            sql = "INSERT INTO category(Category_id,Category_Name) VALUES (%s, %s)"
            data1 = (int(insert_category_id), str(insert_category_name))
            cnx.execute(sql, data1)
            mydb.commit()
            st.success("Category Added ")
            time.sleep(2)
            st.experimental_rerun()
        mydb.close()

def update_category():
    st.subheader("Update Products:")
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = "select * from category"
    cnx.execute(sql)
    data1 = cnx.fetchall()
    cnx.close()
    choices = dict((x, y) for x, y in data1)

    option = st.selectbox("Select Category For Modify", options=list(choices.keys()),format_func=format_func)
    st.write("---")

    mydb = db_cnx()

    cnx = mydb.cursor()
    cnx.execute(f"select * from category where category_id = {option}")
    old_data = cnx.fetchall()
    cnx.close()
    if old_data:
        st.text_input("Category ID", key="update_category_id",value=old_data[0][0])
        st.text_input("Category Name", key="update_category_name",value=old_data[0][1])
        update_category_id = str(option)
        update_category_name = st.session_state.update_category_name
        update_btn = st.button("Update", key="update_btn")
        if update_btn:
            if update_category_id == "":
                st.error("Enter a category Id")
            else:
                if (update_category_id.isalnum()):
                    mydb = db_cnx()
                    cnx = mydb.cursor()
                    sql = "UPDATE category SET category_id = %s, category_Name = %s WHERE category_id  = %s"
                    data1 = (int(update_category_id), str(update_category_name), int(option))
                    cnx.execute(sql, data1)
                    mydb.commit()
                    st.success("Category updated ")
                    mydb.close()
                else:
                    st.error("Please enter valid category id")

def del_category():
    st.subheader("Update Products:")
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = "select * from category"
    cnx.execute(sql)
    data1 = cnx.fetchall()
    cnx.close()
    choices = dict((x, y) for x, y in data1)

    option = st.selectbox("Select Category", options=list(choices.keys()), format_func=format_func)
    st.write("---")
    del_category_btn = st.button("Delete")
    if del_category_btn:
        mydb = db_cnx()
        cnx = mydb.cursor()
        cnx.execute(f"select * from product where category_id = {option}")
        data = cnx.fetchall()
        cnx.close()
        if data:
            st.error("You cant delete this category")
        else:
            cnx.execute(f"delete from category where category_id = {option}")
            st.success("Category Deleted")

        mydb.commit()
        mydb.close()


mydb = db_cnx()
cnx = mydb.cursor()
sql = f"select * from  category"
cnx.execute(sql)
data1 = cnx.fetchall()
cnx.close()
CHOICES = dict((x, y) for x, y in data1)


if 'User_Role' in st.session_state and st.session_state.User_Role == "Admin":
    tab1, tab2, tab3, tab4 = st.tabs(["View All Category ", "Add Category", "Modify Category", "Delete Category"])
    with tab1:
        Category()

    with tab2:
        insert_Category()

    with tab3:
        update_category()

    with tab4:
        del_category()

elif 'User_Role' in st.session_state and st.session_state.User_Role == "Customer":
    Category()

