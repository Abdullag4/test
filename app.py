import streamlit as st
import sqlite3

# Define the path to the SQLite database file (assumes it's in the same directory as the app)
db_file = "erp_system.db"

# Connect to the database
def get_connection():
    return sqlite3.connect(db_file)

# Insert data into erp_table
def insert_into_erp_table(name, category, price, quantity):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO erp_table (name, category, price, quantity) VALUES (?, ?, ?, ?)",
        (name, category, price, quantity),
    )
    connection.commit()
    connection.close()

# Insert data into supplier_table
def insert_into_supplier_table(supplier_name, contact_number, address, email):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO supplier_table (supplier_name, contact_number, address, email) VALUES (?, ?, ?, ?)",
        (supplier_name, contact_number, address, email),
    )
    connection.commit()
    connection.close()

# Insert data into customer_table
def insert_into_customer_table(customer_name, contact_number, address, email):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO customer_table (customer_name, contact_number, address, email) VALUES (?, ?, ?, ?)",
        (customer_name, contact_number, address, email),
    )
    connection.commit()
    connection.close()

# Streamlit UI
st.title("ERP Database - Add Data")

# Tab layout for different tables
tab1, tab2, tab3 = st.tabs(["Add to ERP Table", "Add to Supplier Table", "Add to Customer Table"])

# ERP Table Form
with tab1:
    st.header("Add Data to ERP Table")
    erp_name = st.text_input("Product Name", key="erp_name")
    erp_category = st.text_input("Category", key="erp_category")
    erp_price = st.number_input("Price", min_value=0.0, format="%.2f", key="erp_price")
    erp_quantity = st.number_input("Quantity", min_value=0, format="%d", key="erp_quantity")
    if st.button("Add to ERP Table", key="add_erp"):
        insert_into_erp_table(erp_name, erp_category, erp_price, erp_quantity)
        st.success("Data added to ERP Table!")

# Supplier Table Form
with tab2:
    st.header("Add Data to Supplier Table")
    supplier_name = st.text_input("Supplier Name", key="supplier_name")
    supplier_contact = st.text_input("Contact Number", key="supplier_contact")
    supplier_address = st.text_input("Address", key="supplier_address")
    supplier_email = st.text_input("Email", key="supplier_email")
    if st.button("Add to Supplier Table", key="add_supplier"):
        insert_into_supplier_table(supplier_name, supplier_contact, supplier_address, supplier_email)
        st.success("Data added to Supplier Table!")

# Customer Table Form
with tab3:
    st.header("Add Data to Customer Table")
    customer_name = st.text_input("Customer Name", key="customer_name")
    customer_contact = st.text_input("Contact Number", key="customer_contact")
    customer_address = st.text_input("Address", key="customer_address")
    customer_email = st.text_input("Email", key="customer_email")
    if st.button("Add to Customer Table", key="add_customer"):
        insert_into_customer_table(customer_name, customer_contact, customer_address, customer_email)
        st.success("Data added to Customer Table!")
