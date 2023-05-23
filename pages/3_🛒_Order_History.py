import time

import streamlit as st
import mysql.connector
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode
from streamlit_extras.switch_page_button import switch_page

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
        database="ecommerce_management_1"
    )
    return mydb
def format_func(option):
    return CHOICES[option]
def view_order_history():
    st.subheader("Order History:")
    Refresh_btn = st.button("Refresh Table")
    if Refresh_btn:
        st.experimental_rerun()
    mydb = db_cnx()
    cnx = mydb.cursor()
    cnx.execute(
        f"""select h.Order_ID,p.Product_name, c.Category_name, h.Qty, h.Order_date,s.status_name
            from orders_history h, order_status s, product p, category c where h.Order_Status = s.status_id and 
            h.Product_Id = p.Product_Id and p.Category_Id = c.Category_Id and  (h.User_Id = {st.session_state.User_id})
             order by Order_Date desc;
            """)
    df = pd.DataFrame(cnx)
    cnx.close()
    df = df.rename(columns={0: 'Order_ID', 1: 'Product_name', 2: 'Category_name', 3: 'Qty',4: 'Order_date',5:'status_name'})
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=True)

    gridoptions = gb.build()

    AgGrid(
        df,
        gridOptions=gridoptions,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
    )



def insert_order_history():
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = "select Product_Id,Product_Name from  product;"
    cnx.execute(sql)
    data1 = cnx.fetchall()
    cnx.close()
    choices = dict((x, y) for x, y in data1)

    st.subheader("Add a order:")
    option = st.selectbox("Product Category", options=list(choices.keys()), format_func=format_func)
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = f"select Product_Id,Product_Name,Price from  product where product_id = {option};"
    cnx.execute(sql)
    data1 = cnx.fetchall()
    cnx.close()
    st.text_input("Price", key="price", disabled=True,value=data1[0][2])
    st.number_input("Quantity", key="qty",min_value=1,step=1)
    st.write("Total Rs: ", str(float(st.session_state.price)*st.session_state.qty), "/-")
    buy_btn = st.button("Buy now")

    if buy_btn:
        product_id = option
        qty = st.session_state.qty
        mydb = db_cnx()
        cnx = mydb.cursor()
        sql = """INSERT INTO `orders_history` (`User_Id`, `Product_Id`,`Order_Date`, `Qty`,`Order_Status`)
                VALUES (%s, %s, now(), %s, %s);"""
        data1 = (int(st.session_state.User_id), int(option), int(qty), 1)
        cnx.execute(sql, data1)
        mydb.commit()
        cnx.close()
        st.success("Order Created")


def delete_order_history():
    st.subheader("Cancel a order:")
    st.divider()
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = f"select order_id from orders_history where user_id = {st.session_state.User_id}  order by Order_Date desc limit 5; "
    cnx.execute(sql)
    orders_list = cnx.fetchall()
    cnx.close()
    lst = [i[0] for i in orders_list]
    option = st.selectbox("Order Number:", options=lst, key="order_number")
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = f"""select h.Order_ID,p.Product_name, p.Price, c.Category_name, h.User_id, h.Qty, h.Order_date,s.status_name
            from orders_history h, order_status s, product p, category c where h.Order_Status = s.status_id and 
            h.Product_Id = p.Product_Id and p.Category_Id = c.Category_Id and  (h.User_Id = {st.session_state.User_id} and 
            h.Order_id = {option}) order by Order_Date desc;
            """
    cnx.execute(sql)
    data1 = cnx.fetchall()
    cnx.close()
    st.text_input("Product Name", key="product_name",disabled=True,value=data1[0][1])
    st.text_input("Category", key="category", disabled=True, value=data1[0][3])
    st.text_input("Price", key="price", disabled=True, value=data1[0][2])
    st.number_input("Quantity", key="qty",value=data1[0][5], min_value=1, step=1,disabled=True)
    st.text_input("Status",value=data1[0][7],disabled=True)

    st.write("Total Rs: ", str(float(st.session_state.price) * st.session_state.qty), "/-")
    st.divider()
    cancel = st.button("Cancel Order")


    if cancel:
        st.success("Ordered cancelled")
        mydb = db_cnx()
        cnx = mydb.cursor()
        sql = f"""Update Orders_history set order_status = 6 where order_id = {option}"""
        cnx.execute(sql)
        mydb.commit()
        cnx.close()
        time.sleep(2)
        st.experimental_rerun()


def Temp_order_history():
    st.subheader("Cancel a order:")
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = f"select order_id from orders_history where user_id = {st.session_state.User_id}  order by Order_Date desc limit 5; "
    cnx.execute(sql)
    orders_list = cnx.fetchall()
    cnx.close()
    lst = [i[0] for i in orders_list]
    mydb = db_cnx()
    cnx = mydb.cursor()
    sql = f"""select h.Order_ID,p.Product_name, p.Price, c.Category_name, h.User_id, h.Qty, h.Order_date,s.status_name
            from orders_history h, order_status s, product p, category c where h.Order_Status = s.status_id and 
            h.Product_Id = p.Product_Id and p.Category_Id = c.Category_Id and  (h.User_Id = {st.session_state.User_id}) order by Order_Date desc;
            """
    cnx.execute(sql)
    data1 = cnx.fetchall()
    cnx.close()
    for i in data1:
        st.divider()
        print(i)
        with st.container():
            # st.write(data1)
            col1,col2 = st.columns(2)
            with col1:
                st.write("Order Number: ", str(i[0]))
                st.write("Product Name: ", str(i[1]))
                st.write("Total: ", str(i[2] * i[5]))

            with col2:
                st.write("Date: ", str(i[6]))
                st.write("Category: ", str(i[3]))
                st.write("Status: ",str(i[7]))



        cancel = st.button("Cancel Order",key=f"Cancel_{i[0]}")


        if cancel:
            st.success("Ordered cancelled")
            mydb = db_cnx()
            cnx = mydb.cursor()
            sql = f"""Update Orders_history set order_status = 6 where order_id = {i[0]}"""
            cnx.execute(sql)
            mydb.commit()
            cnx.close()
            time.sleep(1)
            st.experimental_rerun()



mydb = db_cnx()
cnx = mydb.cursor()
sql = "select Product_Id,Product_Name from  product;"
cnx.execute(sql)
data1 = cnx.fetchall()
cnx.close()
CHOICES = dict((x, y) for x, y in data1)





# view_order_history()
# insert_order_history()
# delete_order_history()
# Temp_order_history()

# if 'User_Role' in st.session_state and st.session_state.User_Role == "Customer":
if 'User_Role' in st.session_state:
    tab1, tab2, tab3 = st.tabs(["View All Orders ", "Create a Order", "Cancel Products"])
    with tab1:
        view_order_history()

    with tab2:
        insert_order_history()

    with tab3:
        Temp_order_history()


