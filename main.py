import streamlit as st
import mysql.connector
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid
#
st.set_page_config(page_title="The Tech collective",page_icon="🧊")
st.title("The Tech Collective")
st.subheader("Python Mini Project ")

st.subheader("Project contributors")

st.write("Deepak Patel (Team Lead)")
col1, col2= st.columns(2)
with col1:
    st.write("Ajinkya Fuke (Database)")
    st.write("Aditya Ugale (Frontend)")
    st.write("Arpit Tiwari (Backend)")
with col2:
    st.write("Aishwarya Chopade (Database)")
    st.write("Akshay Shetty (Frontend)")
    st.write("Charudatta Patil (Backend)")


# def db_cnx():
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="Night@123",
#         database="ecommerce_management"
#     )
#     return mydb
#
#
# def show():
#     add_admin = st.button("add a admin", key="add_admin")
#     del_admin = st.button("delete a admin", key="del_admin")
#
#     # if st.session_state.add_admin:
#     #     modal = Modal(key="DemoKey", title="Add a Admin")
#     #     with modal.container():
#     #         st.text_input("username:", key="modal_add_user_name")
#     #         st.text_input("Password:", key="modal_add_password")
#     #         st.text_input("Confirm Password:", key="modal_add_confirm_password")
#     #         modal_add_btn = st.button("Add")
#     #
#     #         if modal_add_btn:
#     #             print(st.session_state.add_admin)
#     #             modal_add_user_name = st.session_state.modal_add_user_name
#     #             modal_add_password = st.session_state.modal_add_password
#     #             modal_add_confirm_password = st.session_state.modal_add_confirm_password
#     #             mydb = db_cnx()
#     #
#     #             cnx = mydb.cursor()
#     #             sql = "INSERT INTO admin(User_Id,Password,Confirm_Password,Role)VALUES (%s, %s, %s, %s)"
#     #             data1 = (int(modal_add_user_name), str(modal_add_password), str(modal_add_confirm_password), 'Admin')
#     #             print(sql, data1)
#     #             cnx.execute(sql, data1)
#     #             mydb.commit()
#     #             mydb.close()
#
#     if del_admin:
#         del_product()
#         # modal = Modal(key="DemoKey2", title="del a Admin")
#         # with modal.container():
#         #     st.text_input("username:", key="modal_del_user_name")
#         #     model_del_user_btn = st.button("delete")
#         #     print("Deepak")
#         #     if model_del_user_btn:
#         #         st.session_state['modal_del_user_name'] = True
#         #         modal_del_user_name = st.session_state.modal_del_user_name
#         #         mydb = db_cnx()
#         #         cnx = mydb.cursor()
#         #         sql = f"DELETE INTO admin WHERE user_id = {modal_del_user_name}"
#         #         print(sql)
#         #         cnx.execute(sql)
#         #         mydb.commit()
#         #         mydb.close()
#
#
#
#
#
#     mydb = db_cnx()
#
#     mycursor = mydb.cursor()
#     mycursor.execute("select * from admin")
#     df = pd.DataFrame(mycursor)
#     df = df.rename(columns={0: 'user_id', 1: 'user_name', 2: 'password', 3: 'Role'})
#     gb = GridOptionsBuilder.from_dataframe(df)
#
#     gridoptions = gb.build()
#
#     AgGrid(
#         df,
#         gridOptions=gridoptions,
#         fit_columns=False
#     )
#
# def products():
#     mydb = db_cnx()
#
#     mycursor = mydb.cursor()
#     mycursor.execute("select * from Product")
#     df = pd.DataFrame(mycursor)
#     df = df.rename(columns={0: 'Product_Id', 1: 'Product_Name', 2: 'Category_Id', 3: 'Price'})
#     gb = GridOptionsBuilder.from_dataframe(df)
#
#     gridoptions = gb.build()
#
#     AgGrid(
#         df,
#         gridOptions=gridoptions,
#         fit_columns=False
#     )
#
# def del_product():
#     st.title("Delete Product")
#     st.text_input("Product_ID", key='del_product_id')
#     del_product_btn = st.button("Delete")
#     if del_product_btn:
#         products_id = int(st.session_state.del_product_id)
#         mydb = db_cnx()
#         cnx = mydb.cursor()
#         print(f"delete from Product where product_id = {products_id}")
#         cnx.execute(f"delete from Product where product_id = {products_id}")
#         mydb.commit()
#         mydb.close()
#
# # def login():
# #     st.title("Login")
# #     st.text_input("name", key='user_name')
# #     st.text_input("Login_Password", type="password",key="password")
# #     login_btn = st.button("Login")
# #     if login_btn:
# #         user_name = st.session_state.user_name
# #         password = st.session_state.password
# #         mydb = db_cnx()
# #         cnx = mydb.cursor()
# #         sql = f"select * from admin where user_id = {user_name} and password = '{password}'"
# #         cnx.execute(sql)
# #         data = cnx.fetchall()
# #         print(len(data))
# #         if len(data) == 1:
# #             st.success("logged in")
# #             page = st.sidebar.selectbox('Select page', [ 'Show'])
# #             if page == 'show':
# #                 show()
# #
# #         else:
# #             st.error("Username and Password not matched")
#
# # st.header("The Tech Collective")
# # page = st.sidebar.selectbox('Select page', ['login', 'show','products','del_product'])
# #
# # if page == 'show':
# #     show()
# # elif page == 'products':
# #     products()
# # elif page == 'del_product':
# #     del_product()
#
#