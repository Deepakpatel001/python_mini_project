import time

import streamlit as st
import mysql.connector
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid
from streamlit_extras.switch_page_button import switch_page

# here is code for checking session for login
if 'Logged_Username' not in st.session_state:
    switch_page("Home")


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

st.image("banner_2.jpg")


def db_cnx():
    mydb = mysql.connector.connect(
        host="localhost",
        user="ecommerce",
        password="Strom@123",
        database="ecommerce_management"
    )
    return mydb


def format_func_cat(option):
    return CHOICES_cat[option]


def format_func_prod(option):
    return CHOICES_prod[option]


def format_func_update_prod(option):
    return CHOICES_update_prod[option]


def products():
    st.subheader("Product List: ")
    Refresh_btn = st.button("Refresh Table")
    if Refresh_btn:
        st.experimental_rerun()
    mydb = db_cnx()
    cnx = mydb.cursor()
    cnx.execute("select p.product_id,p.product_name,p.price,c.category_name from product p join category c on c.category_id =p.category_id;")
    df = pd.DataFrame(cnx)
    cnx.close()
    df = df.rename(columns={0: 'Product_Id', 1: 'Product_Name', 2: 'Price', 3: 'Category'})
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=True)

    gridoptions = gb.build()

    AgGrid(
        df,
        gridOptions=gridoptions,
    )


def insert_products():
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = f"select * from  category"
    cnx.execute(sql)
    data1 = cnx.fetchall()
    cnx.close()
    choices = dict((x, y) for x, y in data1)

    st.subheader("Add Products:")
    st.text_input("Product Id:", key="insert_product_id",  placeholder="123456")
    st.text_input("Product Name:", key="insert_product_name", placeholder="Mango")
    option = st.selectbox("Product Category", options=list(choices.keys()), format_func=format_func_cat)
    st.text_input("Product Price:", key="insert_product_price",placeholder="125")
    insert_btn = st.button("Add")
    insert_product_id = st.session_state.insert_product_id
    insert_product_name = st.session_state.insert_product_name
    insert_product_category = option
    insert_product_price = st.session_state.insert_product_price
    if insert_btn:
        if insert_product_id.isnumeric() and insert_product_name.isalpha():
            mydb = db_cnx()
            cnx = mydb.cursor()
            sql = f"select * from  product where product_id = {insert_product_id}"
            cnx.execute(sql)
            data1 = cnx.fetchall()
            if data1:
                st.error("product Id already found")
            else:
                sql = "INSERT INTO product(Product_Id,Product_Name,Category_Id,Price)VALUES (%s, %s, %s, %s)"
                data1 = (
                    insert_product_id, str(insert_product_name), str(insert_product_category),float(insert_product_price))
                cnx.execute(sql, data1)
                mydb.commit()

                st.success("Product Added ")
                time.sleep(2)
                st.experimental_rerun()

            mydb.close()


        else:
            st.error("Check the input format")

def product_update():
    st.subheader("Update Products:")
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = "select Product_Id,Product_Name from  product"
    cnx.execute(sql)
    data1 = cnx.fetchall()
    cnx.close()
    choices = dict((x, y) for x, y in data1)

    option = st.selectbox("Select Product For Modify", options=list(choices.keys()), format_func=format_func_update_prod)
    st.write("---")
    mydb = db_cnx()

    cnx = mydb.cursor()
    cnx.execute(f"select * from Product where product_id = {option}")
    old_data = cnx.fetchall()
    cnx.close()
    if old_data:
        st.text_input("Product Name", key="update_product_name",value=old_data[0][1])
        st.text_input("Product Category", key="update_product_category",value=old_data[0][2])
        st.number_input ("Product Price", key="update_product_price",value=float(old_data[0][3]))
        update_btn = st.button("Update")

        if update_btn:
            update_product_id = str(option)
            update_product_name = str(st.session_state.update_product_name)
            update_product_category = str(st.session_state.update_product_category)
            update_product_price = str(st.session_state.update_product_price)
            if update_product_id == "":
                st.error("Enter a Product Id")
            else:
                if(update_product_id.isnumeric() and update_product_category.isnumeric()) :
                    mydb = db_cnx()
                    cnx = mydb.cursor()
                    sql = "UPDATE product SET Product_Name = %s, Category_Id = %s, Price = %s WHERE Product_Id = %s"
                    data1 = (str(update_product_name), str(update_product_category), float(update_product_price),int(update_product_id))
                    cnx.execute(sql,data1)
                    mydb.commit()
                    st.success("Product updated ")
                    mydb.close()
                else:
                    st.error("check the format")
    else:
        st.error("Wrong product id")

def del_product():
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = "select Product_Id,Product_Name from  product"
    cnx.execute(sql)
    data1 = cnx.fetchall()
    cnx.close()
    choices = dict((x, y) for x, y in data1)
    st.subheader("Delete Product:")
    option = st.selectbox("Select Product", options=list(choices.keys()), format_func=format_func_prod)
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
sql = f"select * from  category"
cnx.execute(sql)
data1 = cnx.fetchall()
cnx.close()
CHOICES_cat = dict((x, y) for x, y in data1)

mydb = db_cnx()
cnx = mydb.cursor()
sql = "select Product_Id,Product_Name from  product"
cnx.execute(sql)
data1 = cnx.fetchall()
cnx.close()
CHOICES_prod = dict((x, y) for x, y in data1)

mydb = db_cnx()
cnx = mydb.cursor()
sql = "select Product_Id,Product_Name from  product"
cnx.execute(sql)
data1 = cnx.fetchall()
cnx.close()
CHOICES_update_prod = dict((x, y) for x, y in data1)


if 'User_Role' in st.session_state and st.session_state.User_Role == "Admin":
    tab1, tab2, tab3, tab4 = st.tabs(["View All Products ", "Add Products", "Modify Products", "Delete Products"])
    with tab1:
        products()

    with tab2:
        insert_products()

    with tab3:
        product_update()

    with tab4:
        del_product()

elif 'User_Role' in st.session_state and st.session_state.User_Role == "Customer":
    products()