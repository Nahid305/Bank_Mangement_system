import sqlite3
from tkinter import *
from tkinter import messagebox, filedialog
from datetime import datetime

# Database setup
def create_connection():
    conn = sqlite3.connect('bank.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_number INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            balance REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number INTEGER,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_number) REFERENCES accounts(account_number)
        )
    ''')
    conn.commit()
    conn.close()

# GUI Application
class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("500x400")

        # Labels
        Label(root, text="Account Number").grid(row=0, column=0)
        Label(root, text="Name").grid(row=1, column=0)
        Label(root, text="Password").grid(row=2, column=0)
        Label(root, text="Amount").grid(row=3, column=0)

        # Entry fields
        self.account_number = Entry(root)
        self.account_number.grid(row=0, column=1)
        self.name = Entry(root)
        self.name.grid(row=1, column=1)
        self.password = Entry(root, show="*")
        self.password.grid(row=2, column=1)
        self.amount = Entry(root)
        self.amount.grid(row=3, column=1)

        # Buttons
        Button(root, text="Create Account", command=self.create_account).grid(row=4, column=0)
        Button(root, text="Deposit", command=self.deposit).grid(row=4, column=1)
        Button(root, text="Withdraw", command=self.withdraw).grid(row=5, column=0)
        Button(root, text="Check Balance", command=self.check_balance).grid(row=5, column=1)
        Button(root, text="Transaction History", command=self.transaction_history).grid(row=6, column=0)
        Button(root, text="Export History", command=self.export_history).grid(row=6, column=1)
        Button(root, text="Admin Panel", command=self.admin_panel).grid(row=7, column=0)

    def create_account(self):
        name = self.name.get()
        password = self.password.get()
        if name and password:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO accounts (name, password, balance) VALUES (?, ?, ?)", (name, password, 0))
            conn.commit()
            account_number = cursor.lastrowid
            conn.close()
            messagebox.showinfo("Success", f"Account created successfully! Account Number: {account_number}")
        else:
            messagebox.showerror("Error", "Name and password are required!")

    def deposit(self):
        account_number = self.account_number.get()
        password = self.password.get()
        amount = self.amount.get()
        if account_number and password and amount:
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM accounts WHERE account_number = ? AND password = ?", (account_number, password))
                if cursor.fetchone():
                    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_number = ?", (amount, account_number))
                    cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (?, 'Deposit', ?)", (account_number, amount))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Amount deposited successfully!")
                else:
                    messagebox.showerror("Error", "Invalid account number or password!")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def withdraw(self):
        account_number = self.account_number.get()
        password = self.password.get()
        amount = self.amount.get()
        if account_number and password and amount:
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT balance FROM accounts WHERE account_number = ? AND password = ?", (account_number, password))
                result = cursor.fetchone()
                if result:
                    balance = result[0]
                    if balance >= amount:
                        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_number = ?", (amount, account_number))
                        cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (?, 'Withdraw', ?)", (account_number, amount))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Success", "Amount withdrawn successfully!")
                    else:
                        messagebox.showerror("Error", "Insufficient balance!")
                else:
                    messagebox.showerror("Error", "Invalid account number or password!")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def check_balance(self):
        account_number = self.account_number.get()
        password = self.password.get()
        if account_number and password:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM accounts WHERE account_number = ? AND password = ?", (account_number, password))
            result = cursor.fetchone()
            conn.close()
            if result:
                messagebox.showinfo("Balance", f"Your balance is: {result[0]}")
            else:
                messagebox.showerror("Error", "Invalid account number or password!")
        else:
            messagebox.showerror("Error", "Account number and password are required!")

    def transaction_history(self):
        account_number = self.account_number.get()
        password = self.password.get()
        if account_number and password:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE account_number = ? AND password = ?", (account_number, password))
            if cursor.fetchone():
                cursor.execute("SELECT type, amount, timestamp FROM transactions WHERE account_number = ?", (account_number,))
                transactions = cursor.fetchall()
                conn.close()
                history = "\n".join([f"{t[0]} of {t[1]} on {t[2]}" for t in transactions])
                messagebox.showinfo("Transaction History", history if history else "No transactions found!")
            else:
                messagebox.showerror("Error", "Invalid account number or password!")
        else:
            messagebox.showerror("Error", "Account number and password are required!")

    def export_history(self):
        account_number = self.account_number.get()
        password = self.password.get()
        if account_number and password:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE account_number = ? AND password = ?", (account_number, password))
            if cursor.fetchone():
                cursor.execute("SELECT type, amount, timestamp FROM transactions WHERE account_number = ?", (account_number,))
                transactions = cursor.fetchall()
                conn.close()
                if transactions:
                    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
                    if file_path:
                        with open(file_path, "w") as file:
                            file.write("Transaction History:\n")
                            file.write("\n".join([f"{t[0]} of {t[1]} on {t[2]}" for t in transactions]))
                        messagebox.showinfo("Success", "Transaction history exported successfully!")
                else:
                    messagebox.showerror("Error", "No transactions found!")
            else:
                messagebox.showerror("Error", "Invalid account number or password!")
        else:
            messagebox.showerror("Error", "Account number and password are required!")

    def admin_panel(self):
        admin_window = Toplevel(self.root)
        admin_window.title("Admin Panel")
        admin_window.geometry("400x300")

        Label(admin_window, text="Admin Password").grid(row=0, column=0)
        self.admin_password = Entry(admin_window, show="*")
        self.admin_password.grid(row=0, column=1)

        Button(admin_window, text="View All Accounts", command=self.view_all_accounts).grid(row=1, column=0)
        Button(admin_window, text="Delete Account", command=self.delete_account).grid(row=1, column=1)

    def view_all_accounts(self):
        password = self.admin_password.get()
        if password == "admin123":  # Default admin password
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT account_number, name, balance FROM accounts")
            accounts = cursor.fetchall()
            conn.close()
            if accounts:
                account_list = "\n".join([f"Account Number: {a[0]}, Name: {a[1]}, Balance: {a[2]}" for a in accounts])
                messagebox.showinfo("All Accounts", account_list)
            else:
                messagebox.showinfo("All Accounts", "No accounts found!")
        else:
            messagebox.showerror("Error", "Invalid admin password!")

    def delete_account(self):
        password = self.admin_password.get()
        if password == "admin123":
            account_number = self.account_number.get()
            if account_number:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM accounts WHERE account_number = ?", (account_number,))
                cursor.execute("DELETE FROM transactions WHERE account_number = ?", (account_number,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Account deleted successfully!")
            else:
                messagebox.showerror("Error", "Account number is required!")
        else:
            messagebox.showerror("Error", "Invalid admin password!")

# Main function
if __name__ == "__main__":
    create_tables()
    root = Tk()
    app = BankApp(root)
    root.mainloop()