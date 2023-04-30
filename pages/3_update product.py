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


def data_update():
    st.text_input("Product Id", key="update_product_id")
    if st.session_state.update_product_id:
        mydb = db_cnx()

        cnx = mydb.cursor()
        cnx.execute("select * from Product")
        old_data = cnx.fetchall()
        st.text_input("Product Name", key="update_product_name",value=old_data[0][1])
        st.text_input("Product Category", key="update_product_category",value=old_data[0][2])
        st.text_input("Product Price", key="update_product_price",value=old_data[0][3])
    fetch = st.button("Fetch")
    if fetch:
        update_product_id = st.session_state.update_product_id
        update_product_name = st.session_state.update_product_name
        update_product_category = st.session_state.update_product_category
        update_product_price = st.session_state.update_product_price
        update_btn = st.button("Update")
        if update_btn:
            if update_product_id == "":
                st.error("Enter a Product Id")
            else:
                mydb = db_cnx()
                cnx = mydb.cursor()
                sql = "UPDATE product SET Product_Name = %s, Category_Id = %s, Price = %s WHERE Product_Id = %s"
                data1 = (str(update_product_name), str(update_product_category), float(update_product_price),int(update_product_id))
                cnx.execute(sql,data1)
                mydb.commit()
                st.success("Product updated ")
                mydb.close()




st.title("Update a product")
st.text_input("Product id", key="search_product_id")
search_btn = st.button("Search",key="search_btn", type="primary")
data = ""

if st.session_state.search_btn:
    search_product_id = st.session_state.search_product_id
    if search_product_id == "":
        st.error("Enter a Product Id")
    else:
        mydb = db_cnx()
        cnx = mydb.cursor()
        cnx.execute(f"select * from Product where product_id = {search_product_id}")
        data = cnx.fetchall()
        if data:
            st.success("product found")


pages = {
    0 : data_update
}

if "current" not in st.session_state:

    st.session_state.current = None

if st.session_state.search_btn:
    st.session_state.current = 0
if st.session_state.current != None:
    pages[st.session_state.current]()



