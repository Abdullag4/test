import streamlit as st
import sqlite3
import requests
import base64
import os

# GitHub repo info and access token
GITHUB_TOKEN = st.secrets["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"]  # Store your token in Streamlit secrets
REPO_OWNER = "Abdullag4"
REPO_NAME = "test"
DB_FILE_PATH = "erp_system.db"  # Path to the .db file in the GitHub repo

# GitHub API URL
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{DB_FILE_PATH}"

# Download the .db file from GitHub
def download_db_file():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(GITHUB_API_URL, headers=headers)
    if response.status_code == 200:
        file_content = base64.b64decode(response.json()["content"])
        with open(DB_FILE_PATH, "wb") as db_file:
            db_file.write(file_content)
    else:
        st.error("Failed to download the database file from GitHub.")
        st.stop()

# Upload the updated .db file to GitHub
def upload_db_file():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    with open(DB_FILE_PATH, "rb") as db_file:
        file_content = base64.b64encode(db_file.read()).decode("utf-8")
    # Get the current file's SHA to update it
    response = requests.get(GITHUB_API_URL, headers=headers)
    if response.status_code == 200:
        sha = response.json()["sha"]
        data = {
            "message": "Update database file",
            "content": file_content,
            "sha": sha,
        }
        response = requests.put(GITHUB_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            st.success("Database updated successfully on GitHub.")
        else:
            st.error("Failed to upload the updated database file to GitHub.")
    else:
        st.error("Failed to fetch the file's SHA from GitHub.")

# Connect to the database
def get_connection():
    return sqlite3.connect(DB_FILE_PATH)

# Insert data into tables
def insert_into_erp_table(name, category, price, quantity):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO erp_table (name, category, price, quantity) VALUES (?, ?, ?, ?)",
        (name, category, price, quantity),
    )
    connection.commit()
    connection.close()

def insert_into_supplier_table(supplier_name, contact_number, address, email):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO supplier_table (supplier_name, contact_number, address, email) VALUES (?, ?, ?, ?)",
        (supplier_name, contact_number, address, email),
    )
    connection.commit()
    connection.close()

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

# Download the database file from GitHub at startup
if not os.path.exists(DB_FILE_PATH):
    download_db_file()

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
        upload_db_file()
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
        upload_db_file()
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
        upload_db_file()
        st.success("Data added to Customer Table!")
