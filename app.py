import sqlite3
import streamlit as st

# Define the database path (assumes it's in the same directory as the app)
db_file = "erp_system.db"

# Function to connect to the database
def get_connection():
    return sqlite3.connect(db_file)

# Function to get all data from a table
def get_all_data(table_name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    connection.close()
    return rows

# Streamlit UI
st.title("Simple ERP Database App")

# Choose a table to interact with
table_options = ["erp_table", "supplier_table", "customer_table"]
selected_table = st.selectbox("Choose a table to view:", table_options)

# Display the data from the selected table
st.header(f"Data from {selected_table}")
data = get_all_data(selected_table)
if data:
    st.table(data)
else:
    st.write("No data found in the selected table.")
