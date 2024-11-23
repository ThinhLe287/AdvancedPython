import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Management App")
        self.root.geometry("600x500")
        self.setup_gui()

    def setup_gui(self):
        # Connection frame
        conn_frame = ttk.LabelFrame(self.root, text="Database Connection")
        conn_frame.pack(fill="x", padx=10, pady=5)

        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='sinhvien')

        ttk.Label(conn_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(conn_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(conn_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(conn_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(conn_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(conn_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(conn_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(conn_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(conn_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        ttk.Entry(conn_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(conn_frame, text="Connect", command=self.connect_db).grid(row=5, column=0, columnspan=2, pady=5)

        # Query frame
        query_frame = ttk.LabelFrame(self.root, text="Table Operations")
        query_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(query_frame, text="Table Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(query_frame, text="Load Data", command=self.load_data).grid(row=1, column=0, columnspan=2, pady=5)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self.root, columns=("massv", "hoten"), show="headings")
        self.tree.heading("massv", text="MSSV")
        self.tree.heading("hoten", text="Họ tên")
        self.tree.column("massv", width=100, anchor="center")
        self.tree.column("hoten", width=200, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Insert/Update/Delete frame
        crud_frame = ttk.LabelFrame(self.root, text="Insert/Update/Delete Data")
        crud_frame.pack(fill="x", padx=10, pady=5)

        self.hoten = tk.StringVar()
        self.massv = tk.StringVar()

        ttk.Label(crud_frame, text="Họ tên:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(crud_frame, textvariable=self.hoten).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(crud_frame, text="MSSV:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(crud_frame, textvariable=self.massv).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(crud_frame, text="Insert", command=self.insert_data).grid(row=2, column=0, pady=5, padx=5)
        ttk.Button(crud_frame, text="Update", command=self.update_data).grid(row=2, column=1, pady=5, padx=5)
        ttk.Button(crud_frame, text="Delete", command=self.delete_data).grid(row=2, column=2, pady=5, padx=5)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def load_data(self):
        try:
            self.tree.delete(*self.tree.get_children())  # Clear existing data
            query = sql.SQL("SELECT massv, hoten FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (massv, hoten) VALUES (%s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.massv.get(), self.hoten.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
            self.load_data()  # Refresh data
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")

    def update_data(self):
        try:
            update_query = sql.SQL("UPDATE {} SET hoten = %s WHERE massv = %s").format(sql.Identifier(self.table_name.get()))
            data_to_update = (self.hoten.get(), self.massv.get())
            self.cur.execute(update_query, data_to_update)
            self.conn.commit()
            messagebox.showinfo("Success", "Data updated successfully!")
            self.load_data()  # Refresh data
        except Exception as e:
            messagebox.showerror("Error", f"Error updating data: {e}")

    def delete_data(self):
        try:
            delete_query = sql.SQL("DELETE FROM {} WHERE massv = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(delete_query, (self.massv.get(),))
            self.conn.commit()
            messagebox.showinfo("Success", "Data deleted successfully!")
            self.load_data()  # Refresh data
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
