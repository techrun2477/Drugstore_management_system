import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

# Initialize dataframes
medicines_df = pd.DataFrame(columns=["MedicineID", "Name", "Type", "Price", "Stock"])
customers_df = pd.DataFrame(columns=["CustomerID", "Name", "Contact"])

# Save dataframes to CSV
def save_data():
    medicines_df.to_csv('medicines.csv', index=False)
    customers_df.to_csv('customers.csv', index=False)

# Load dataframes from CSV
def load_data():
    global medicines_df, customers_df
    try:
        medicines_df = pd.read_csv('medicines.csv')
        customers_df = pd.read_csv('customers.csv')
    except FileNotFoundError:
        pass

# Add Medicine
def add_medicine():
    global medicines_df
    medicine_id = medicine_id_entry.get()
    name = medicine_name_entry.get()
    m_type = medicine_type_entry.get()
    price = medicine_price_entry.get()
    stock = medicine_stock_entry.get()

    if medicine_id and name and m_type and price and stock:
        new_medicine = pd.DataFrame([{
            "MedicineID": medicine_id,
            "Name": name,
            "Type": m_type,
            "Price": price,
            "Stock": stock
        }])
        medicines_df = pd.concat([medicines_df, new_medicine], ignore_index=True)
        save_data()
        update_medicine_table()
        clear_medicine_entries()
    else:
        messagebox.showwarning("Input Error", "All fields are required")

# Update Medicine
def update_medicine():
    global medicines_df
    selected_item = medicine_table.selection()[0]
    medicine_id = medicine_id_entry.get()
    name = medicine_name_entry.get()
    m_type = medicine_type_entry.get()
    price = medicine_price_entry.get()
    stock = medicine_stock_entry.get()

    if selected_item and medicine_id and name and m_type and price and stock:
        medicines_df.loc[medicines_df['MedicineID'] == medicine_table.item(selected_item)['values'][0]] = [medicine_id, name, m_type, price, stock]
        save_data()
        update_medicine_table()
        clear_medicine_entries()
    else:
        messagebox.showwarning("Input Error", "All fields are required")

# Delete Medicine
def delete_medicine():
    global medicines_df
    selected_item = medicine_table.selection()[0]
    if selected_item:
        medicines_df.drop(medicines_df[medicines_df['MedicineID'] == medicine_table.item(selected_item)['values'][0]].index, inplace=True)
        save_data()
        update_medicine_table()
        clear_medicine_entries()
    else:
        messagebox.showwarning("Selection Error", "No item selected")

# Add Customer
def add_customer():
    global customers_df
    customer_id = customer_id_entry.get()
    name = customer_name_entry.get()
    contact = customer_contact_entry.get()

    if customer_id and name and contact:
        new_customer = pd.DataFrame([{
            "CustomerID": customer_id,
            "Name": name,
            "Contact": contact
        }])
        customers_df = pd.concat([customers_df, new_customer], ignore_index=True)
        save_data()
        update_customer_table()
        clear_customer_entries()
    else:
        messagebox.showwarning("Input Error", "All fields are required")

# Update Customer
def update_customer():
    global customers_df
    selected_item = customer_table.selection()[0]
    customer_id = customer_id_entry.get()
    name = customer_name_entry.get()
    contact = customer_contact_entry.get()

    if selected_item and customer_id and name and contact:
        customers_df.loc[customers_df['CustomerID'] == customer_table.item(selected_item)['values'][0]] = [customer_id, name, contact]
        save_data()
        update_customer_table()
        clear_customer_entries()
    else:
        messagebox.showwarning("Input Error", "All fields are required")

# Delete Customer
def delete_customer():
    global customers_df
    selected_item = customer_table.selection()[0]
    if selected_item:
        customers_df.drop(customers_df[customers_df['CustomerID'] == customer_table.item(selected_item)['values'][0]].index, inplace=True)
        save_data()
        update_customer_table()
        clear_customer_entries()
    else:
        messagebox.showwarning("Selection Error", "No item selected")

# Update Medicine Table
def update_medicine_table():
    for row in medicine_table.get_children():
        medicine_table.delete(row)
    for index, row in medicines_df.iterrows():
        medicine_table.insert("", tk.END, values=row.tolist())

# Update Customer Table
def update_customer_table():
    for row in customer_table.get_children():
        customer_table.delete(row)
    for index, row in customers_df.iterrows():
        customer_table.insert("", tk.END, values=row.tolist())

# Clear Medicine Entries
def clear_medicine_entries():
    medicine_id_entry.delete(0, tk.END)
    medicine_name_entry.delete(0, tk.END)
    medicine_type_entry.delete(0, tk.END)
    medicine_price_entry.delete(0, tk.END)
    medicine_stock_entry.delete(0, tk.END)

# Clear Customer Entries
def clear_customer_entries():
    customer_id_entry.delete(0, tk.END)
    customer_name_entry.delete(0, tk.END)
    customer_contact_entry.delete(0, tk.END)

# Login Function
def login():
    user_id = user_id_entry.get()
    password = password_entry.get()
    # Replace 'admin' and 'password' with your actual credentials
    if user_id == 'admin' and password == 'password':
        login_frame.pack_forget()
        notebook.pack(expand=True, fill='both')
    else:
        messagebox.showerror("Login Error", "Invalid User ID or Password")

# Import Data Function
def import_data():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
    if file_path:
        if file_path.endswith('.csv'):
            new_data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            new_data = pd.read_excel(file_path, engine='openpyxl')
        if "MedicineID" in new_data.columns and "Name" in new_data.columns:
            global medicines_df
            medicines_df = pd.concat([medicines_df, new_data], ignore_index=True).drop_duplicates().reset_index(drop=True)
            save_data()
            update_medicine_table()
        elif "CustomerID" in new_data.columns and "Name" in new_data.columns:
            global customers_df
            customers_df = pd.concat([customers_df, new_data], ignore_index=True).drop_duplicates().reset_index(drop=True)
            save_data()
            update_customer_table()
        else:
            messagebox.showerror("File Error", "The file does not match the required format")

# UI Setup
root = tk.Tk()
root.title("Pharmacy Management System")

# Login Frame
login_frame = tk.Frame(root, padx=10, pady=10)
tk.Label(login_frame, text="User ID").grid(row=0, column=0, padx=5, pady=5)
user_id_entry = tk.Entry(login_frame)
user_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(login_frame, text="Password").grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

login_frame.pack()

# Notebook for tabbed interface
notebook = ttk.Notebook(root)

# Medicine Management Frame
medicine_frame = tk.Frame(notebook, padx=10, pady=10)
notebook.add(medicine_frame, text="Medicines")

tk.Label(medicine_frame, text="Medicine ID").grid(row=0, column=0, padx=5, pady=5)
medicine_id_entry = tk.Entry(medicine_frame)
medicine_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(medicine_frame, text="Name").grid(row=1, column=0, padx=5, pady=5)
medicine_name_entry = tk.Entry(medicine_frame)
medicine_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(medicine_frame, text="Type").grid(row=2, column=0, padx=5, pady=5)
medicine_type_entry = tk.Entry(medicine_frame)
medicine_type_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(medicine_frame, text="Price").grid(row=3, column=0, padx=5, pady=5)
medicine_price_entry = tk.Entry(medicine_frame)
medicine_price_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(medicine_frame, text="Stock").grid(row=4, column=0, padx=5, pady=5)
medicine_stock_entry = tk.Entry(medicine_frame)
medicine_stock_entry.grid(row=4, column=1, padx=5, pady=5)

add_medicine_button = tk.Button(medicine_frame, text="Add Medicine", command=add_medicine)
add_medicine_button.grid(row=5, column=0, pady=5)

update_medicine_button = tk.Button(medicine_frame, text="Update Medicine", command=update_medicine)
update_medicine_button.grid(row=5, column=1, pady=5)

delete_medicine_button = tk.Button(medicine_frame, text="Delete Medicine", command=delete_medicine)
delete_medicine_button.grid(row=6, column=0, pady=5)

medicine_table = ttk.Treeview(medicine_frame, columns=("MedicineID", "Name", "Type", "Price", "Stock"), show="headings")
medicine_table.heading("MedicineID", text="Medicine ID")
medicine_table.heading("Name", text="Name")
medicine_table.heading("Type", text="Type")
medicine_table.heading("Price", text="Price")
medicine_table.heading("Stock", text="Stock")
medicine_table.grid(row=7, column=0, columnspan=2, pady=10)

import_medicine_button = tk.Button(medicine_frame, text="Import Medicines", command=import_data)
import_medicine_button.grid(row=8, column=0, columnspan=2, pady=5)

# Customer Management Frame
customer_frame = tk.Frame(notebook, padx=10, pady=10)
notebook.add(customer_frame, text="Customers")

tk.Label(customer_frame, text="Customer ID").grid(row=0, column=0, padx=5, pady=5)
customer_id_entry = tk.Entry(customer_frame)
customer_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(customer_frame, text="Name").grid(row=1, column=0, padx=5, pady=5)
customer_name_entry = tk.Entry(customer_frame)
customer_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(customer_frame, text="Contact").grid(row=2, column=0, padx=5, pady=5)
customer_contact_entry = tk.Entry(customer_frame)
customer_contact_entry.grid(row=2, column=1, padx=5, pady=5)

add_customer_button = tk.Button(customer_frame, text="Add Customer", command=add_customer)
add_customer_button.grid(row=3, column=0, pady=5)

update_customer_button = tk.Button(customer_frame, text="Update Customer", command=update_customer)
update_customer_button.grid(row=3, column=1, pady=5)

delete_customer_button = tk.Button(customer_frame, text="Delete Customer", command=delete_customer)
delete_customer_button.grid(row=4, column=0, pady=5)

customer_table = ttk.Treeview(customer_frame, columns=("CustomerID", "Name", "Contact"), show="headings")
customer_table.heading("CustomerID", text="Customer ID")
customer_table.heading("Name", text="Name")
customer_table.heading("Contact", text="Contact")
customer_table.grid(row=5, column=0, columnspan=2, pady=10)

import_customer_button = tk.Button(customer_frame, text="Import Customers", command=import_data)
import_customer_button.grid(row=6, column=0, columnspan=2, pady=5)

# Load initial data and start main loop
load_data()
update_medicine_table()
update_customer_table()
root.mainloop()
