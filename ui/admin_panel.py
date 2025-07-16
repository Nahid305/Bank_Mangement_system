# ui/admin_panel.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
from typing import List, Dict, Optional
import csv
from database.db_manager import db_manager

class AdminPanel:
    """Administrative interface for managing bank accounts and system settings."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bank Admin Panel")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Current admin user (set during login)
        self.admin_user = None
        
        self.setup_ui()
        self.load_dashboard()
        
    def setup_ui(self):
        """Initialize all UI components."""
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("Accent.TButton", foreground="white", background="#4a6baf")
        self.style.configure("Warning.TButton", foreground="white", background="#d32f2f")
        self.style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        self.style.configure("Treeview", rowheight=25)
        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Header with admin info
        self.create_header()
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH, pady=(10, 0))
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_accounts_tab()
        self.create_transactions_tab()
        self.create_loans_tab()
        self.create_system_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, pady=(5, 0))
        self.update_status("Admin panel initialized")
        
    def create_header(self):
        """Create the header section with admin info."""
        header_frame = ttk.Frame(self.main_frame, style="Success.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Admin info
        self.admin_info_var = tk.StringVar(value="Logged in as: Administrator")
        ttk.Label(
            header_frame, 
            textvariable=self.admin_info_var,
            font=("Helvetica", 12, "bold")
        ).pack(side=tk.LEFT, padx=10, pady=5)
        
        # System stats
        self.stats_var = tk.StringVar()
        ttk.Label(
            header_frame,
            textvariable=self.stats_var,
            font=("Helvetica", 10)
        ).pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Logout button
        ttk.Button(
            header_frame,
            text="Logout",
            command=self.logout,
            style="Warning.TButton"
        ).pack(side=tk.RIGHT, padx=5)
        
    def create_dashboard_tab(self):
        """Create the admin dashboard overview tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dashboard")
        
        # Stats cards
        cards_frame = ttk.Frame(tab)
        cards_frame.pack(fill=tk.X, pady=10)
        
        # Card 1: Total Accounts
        self.total_accounts_var = tk.StringVar(value="Loading...")
        self.create_stat_card(
            cards_frame, 
            "Total Accounts", 
            self.total_accounts_var, 
            "#4a6baf",
            0, 0
        )
        
        # Card 2: Total Balance
        self.total_balance_var = tk.StringVar(value="Loading...")
        self.create_stat_card(
            cards_frame, 
            "Total Deposits", 
            self.total_balance_var, 
            "#2e7d32",
            0, 1
        )
        
        # Card 3: Recent Activity
        self.recent_activity_var = tk.StringVar(value="Loading...")
        self.create_stat_card(
            cards_frame, 
            "Recent Activity", 
            self.recent_activity_var, 
            "#d84315",
            0, 2
        )
        
        cards_frame.columnconfigure((0, 1, 2), weight=1, uniform="cards")
        
        # Recent transactions
        ttk.Label(tab, text="Recent System Activity", style="Header.TLabel").pack(anchor=tk.W, pady=(15, 5))
        
        self.activity_tree = ttk.Treeview(
            tab, 
            columns=("Time", "Type", "Account", "Amount", "Description"), 
            show="headings",
            height=8
        )
        self.activity_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns
        col_widths = {"Time": 120, "Type": 80, "Account": 80, "Amount": 100, "Description": 200}
        for col in self.activity_tree["columns"]:
            self.activity_tree.heading(col, text=col)
            self.activity_tree.column(col, width=col_widths.get(col, 100), 
                                    anchor=tk.CENTER if col not in ("Description", "Type") else tk.W)
        
        # Load initial data
        self.load_dashboard_stats()
        
    def create_stat_card(self, parent, title, value_var, color, row, column):
        """Create a statistic card UI element."""
        card = ttk.Frame(parent, borderwidth=1, relief=tk.RAISED)
        card.grid(row=row, column=column, padx=5, pady=5, sticky=tk.NSEW)
        
        ttk.Label(
            card,
            text=title,
            font=("Helvetica", 10, "bold"),
            foreground=color
        ).pack(pady=(5, 0))
        
        ttk.Label(
            card,
            textvariable=value_var,
            font=("Helvetica", 14, "bold")
        ).pack(pady=(0, 5))
        
        return card
        
    def create_accounts_tab(self):
        """Create the account management tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Accounts")
        
        # Search and filter controls
        control_frame = ttk.Frame(tab)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.load_accounts())
        
        ttk.Button(
            control_frame,
            text="Refresh",
            command=self.load_accounts
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="Create Account",
            command=self.create_account_dialog,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        # Accounts treeview
        self.accounts_tree = ttk.Treeview(
            tab,
            columns=("ID", "Name", "Balance", "Created", "Last Activity"),
            show="headings",
            height=15
        )
        self.accounts_tree.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Configure columns
        col_widths = {"ID": 60, "Name": 150, "Balance": 100, "Created": 120, "Last Activity": 120}
        for col in self.accounts_tree["columns"]:
            self.accounts_tree.heading(col, text=col)
            self.accounts_tree.column(col, width=col_widths.get(col, 100), 
                                    anchor=tk.CENTER if col not in ("Name",) else tk.W)
        
        # Context menu
        self.account_menu = tk.Menu(self.root, tearoff=0)
        self.account_menu.add_command(label="View Details", command=self.view_account_details)
        self.account_menu.add_command(label="Transaction History", command=self.view_account_transactions)
        self.account_menu.add_separator()
        self.account_menu.add_command(label="Delete Account", command=self.delete_account_dialog)
        
        self.accounts_tree.bind("<Button-3>", self.show_account_context_menu)
        
        # Load initial data
        self.load_accounts()
        
    def create_transactions_tab(self):
        """Create the transaction monitoring tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transactions")
        
        # Filter controls
        filter_frame = ttk.Frame(tab)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Date Range:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.from_date_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.from_date_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(filter_frame, text="to").pack(side=tk.LEFT, padx=5)
        
        self.to_date_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.to_date_var, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            filter_frame,
            text="Apply",
            command=self.load_transactions
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            filter_frame,
            text="Export CSV",
            command=self.export_transactions
        ).pack(side=tk.RIGHT, padx=5)
        
        # Transactions treeview
        self.transactions_tree = ttk.Treeview(
            tab,
            columns=("ID", "Account", "Type", "Amount", "Description", "Date"),
            show="headings",
            height=15
        )
        self.transactions_tree.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Configure columns
        col_widths = {"ID": 50, "Account": 80, "Type": 80, "Amount": 100, "Description": 200, "Date": 120}
        for col in self.transactions_tree["columns"]:
            self.transactions_tree.heading(col, text=col)
            self.transactions_tree.column(col, width=col_widths.get(col, 100), 
                                        anchor=tk.CENTER if col not in ("Description", "Type") else tk.W)
        
        # Load initial data
        self.load_transactions()
        
    def create_loans_tab(self):
        """Create the loan management tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Loan Applications")
        
        # Filter controls
        filter_frame = ttk.Frame(tab)
        filter_frame.pack(fill=tk.X, pady=5)
        
        self.loan_status_var = tk.StringVar(value="All")
        ttk.Combobox(
            filter_frame,
            textvariable=self.loan_status_var,
            values=["All", "Pending", "Approved", "Rejected"],
            state="readonly",
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            filter_frame,
            text="Apply",
            command=self.load_loan_applications
        ).pack(side=tk.LEFT, padx=5)
        
        # Loans treeview
        self.loans_tree = ttk.Treeview(
            tab,
            columns=("ID", "Account", "Amount", "Term", "Income", "Score", "Status", "Applied"),
            show="headings",
            height=15
        )
        self.loans_tree.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Configure columns
        col_widths = {"ID": 50, "Account": 80, "Amount": 100, "Term": 60, "Income": 100, "Score": 60, "Status": 80, "Applied": 120}
        for col in self.loans_tree["columns"]:
            self.loans_tree.heading(col, text=col)
            self.loans_tree.column(col, width=col_widths.get(col, 80), 
                                 anchor=tk.CENTER if col not in ("Status",) else tk.W)
        
        # Context menu
        self.loan_menu = tk.Menu(self.root, tearoff=0)
        self.loan_menu.add_command(label="Approve", command=lambda: self.process_loan_application("Approved"))
        self.loan_menu.add_command(label="Reject", command=lambda: self.process_loan_application("Rejected"))
        
        self.loans_tree.bind("<Button-3>", self.show_loan_context_menu)
        
        # Load initial data
        self.load_loan_applications()
        
    def create_system_tab(self):
        """Create the system settings tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="System")
        
        # Admin management
        admin_frame = ttk.LabelFrame(tab, text="Administrator Accounts", padding=10)
        admin_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            admin_frame,
            text="Add Administrator",
            command=self.add_admin_dialog,
            style="Accent.TButton"
        ).pack(fill=tk.X, pady=2)
        
        # Admin list
        self.admin_tree = ttk.Treeview(
            admin_frame,
            columns=("Username", "Full Name", "Last Login"),
            show="headings",
            height=5
        )
        self.admin_tree.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Configure columns
        for col in self.admin_tree["columns"]:
            self.admin_tree.heading(col, text=col)
            self.admin_tree.column(col, width=120, anchor=tk.W)
        
        # System actions
        action_frame = ttk.LabelFrame(tab, text="System Actions", padding=10)
        action_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            action_frame,
            text="Backup Database",
            command=self.backup_database
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            action_frame,
            text="View System Logs",
            command=self.view_system_logs
        ).pack(fill=tk.X, pady=2)
        
        # Load admin list
        self.load_admin_list()
        
    # Data loading methods
    def load_dashboard_stats(self):
        """Load statistics for the dashboard."""
        try:
            # Total accounts
            accounts = db_manager.get_all_accounts()
            self.total_accounts_var.set(f"{len(accounts):,}")
            
            # Total balance
            total_balance = sum(acc['balance'] for acc in accounts)
            self.total_balance_var.set(f"₹{total_balance:,.2f}")
            
            # Recent activity
            transactions = db_manager.get_all_transactions(limit=10)
            self.recent_activity_var.set(f"{len(transactions)} recent")
            
            # Update activity tree
            self.activity_tree.delete(*self.activity_tree.get_children())
            for t in transactions:
                self.activity_tree.insert("", tk.END, values=(
                    t['timestamp'],
                    t['type'],
                    t['account_number'],
                    f"₹{t['amount']:,.2f}",
                    t.get('description', '')
                ))
                
            # Update system stats
            self.stats_var.set(f"Accounts: {len(accounts):,} | Balance: ₹{total_balance:,.2f}")
            
        except Exception as e:
            self.update_status(f"Error loading dashboard: {str(e)}")
            
    def load_accounts(self):
        """Load account data with optional search filter."""
        try:
            search_term = self.search_var.get().lower()
            accounts = db_manager.get_all_accounts()
            
            self.accounts_tree.delete(*self.accounts_tree.get_children())
            
            for acc in accounts:
                # Apply search filter
                if search_term:
                    if (search_term not in str(acc['account_number']) and 
                        search_term not in acc['name'].lower()):
                        continue
                        
                # Get last activity
                last_txn = db_manager.get_last_activity(acc['account_number'])
                
                self.accounts_tree.insert("", tk.END, values=(
                    acc['account_number'],
                    acc['name'],
                    f"₹{acc['balance']:,.2f}",
                    acc['created_at'][:10],
                    last_txn['timestamp'][:16] if last_txn else "Never"
                ))
                
        except Exception as e:
            self.update_status(f"Error loading accounts: {str(e)}")
            
    def load_transactions(self):
        """Load transaction data with optional date filter."""
        try:
            from_date = self.from_date_var.get()
            to_date = self.to_date_var.get()
            
            transactions = db_manager.get_all_transactions(
                from_date=from_date if from_date else None,
                to_date=to_date if to_date else None
            )
            
            self.transactions_tree.delete(*self.transactions_tree.get_children())
            
            for t in transactions:
                self.transactions_tree.insert("", tk.END, values=(
                    t['transaction_id'],
                    t['account_number'],
                    t['type'],
                    f"₹{t['amount']:,.2f}",
                    t.get('description', ''),
                    t['timestamp']
                ))
                
        except Exception as e:
            self.update_status(f"Error loading transactions: {str(e)}")
            
    def load_loan_applications(self):
        """Load loan applications with status filter."""
        try:
            status_filter = self.loan_status_var.get()
            loans = db_manager.get_all_loan_applications()
            
            self.loans_tree.delete(*self.loans_tree.get_children())
            
            for loan in loans:
                if status_filter != "All" and loan['status'] != status_filter:
                    continue
                    
                self.loans_tree.insert("", tk.END, values=(
                    loan['application_id'],
                    loan['account_number'],
                    f"₹{loan['loan_amount']:,.2f}",
                    f"{loan['loan_term']} months",
                    f"₹{loan['income']:,.2f}",
                    loan['credit_score'],
                    loan['status'],
                    loan.get('decision_date', loan.get('applied_date', ''))[:10]
                ))
                
        except Exception as e:
            self.update_status(f"Error loading loan applications: {str(e)}")
            
    def load_admin_list(self):
        """Load list of system administrators."""
        try:
            admins = db_manager.get_all_admins()
            self.admin_tree.delete(*self.admin_tree.get_children())
            
            for admin in admins:
                self.admin_tree.insert("", tk.END, values=(
                    admin['username'],
                    admin['full_name'],
                    admin['last_login'][:16] if admin['last_login'] else "Never"
                ))
                
        except Exception as e:
            self.update_status(f"Error loading admin list: {str(e)}")
            
    # Action methods
    def create_account_dialog(self):
        """Show dialog to create a new account."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Account")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text="Account Holder Name:").pack(pady=(10, 0))
        name_entry = ttk.Entry(dialog)
        name_entry.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(dialog, text="Initial Password:").pack()
        pwd_entry = ttk.Entry(dialog, show="*")
        pwd_entry.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(dialog, text="Initial Deposit (₹):").pack()
        deposit_entry = ttk.Entry(dialog)
        deposit_entry.pack(fill=tk.X, padx=20, pady=5)
        
        def create_account():
            name = name_entry.get().strip()
            password = pwd_entry.get()
            deposit = deposit_entry.get()
            
            if not name or not password:
                messagebox.showerror("Error", "Name and password are required")
                return
                
            try:
                deposit_amount = float(deposit) if deposit else 0.0
                if deposit_amount < 0:
                    raise ValueError("Negative amount")
                    
                account_number = db_manager.create_account(name, password)
                if account_number and deposit_amount > 0:
                    db_manager.deposit(account_number, deposit_amount, "Initial deposit")
                    
                messagebox.showinfo(
                    "Success", 
                    f"Account created successfully!\nAccount Number: {account_number}"
                )
                dialog.destroy()
                self.load_accounts()
                self.load_dashboard_stats()
            except ValueError:
                messagebox.showerror("Error", "Invalid deposit amount")
            except Exception as e:
                messagebox.showerror("Error", f"Account creation failed: {str(e)}")
                
        ttk.Button(
            dialog,
            text="Create Account",
            command=create_account,
            style="Accent.TButton"
        ).pack(pady=10)
        
    def view_account_details(self):
        """Show details of selected account."""
        selected = self.accounts_tree.selection()
        if not selected:
            return
            
        account_id = self.accounts_tree.item(selected[0], "values")[0]
        account = db_manager.get_account_details(account_id)
        
        if account:
            details = (
                f"Account Number: {account['account_number']}\n"
                f"Account Holder: {account['name']}\n"
                f"Current Balance: ₹{account['balance']:,.2f}\n"
                f"Created On: {account['created_at']}\n"
                f"Last Activity: {db_manager.get_last_activity(account_id)['timestamp']}"
            )
            messagebox.showinfo("Account Details", details)
            
    def view_account_transactions(self):
        """Show transaction history for selected account."""
        selected = self.accounts_tree.selection()
        if not selected:
            return
            
        account_id = self.accounts_tree.item(selected[0], "values")[0]
        
        # Create transaction viewer dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Transactions for Account #{account_id}")
        dialog.geometry("800x500")
        
        # Transaction treeview
        tree = ttk.Treeview(
            dialog,
            columns=("ID", "Type", "Amount", "Description", "Date"),
            show="headings",
            height=20
        )
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure columns
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER if col not in ("Description", "Type") else tk.W)
        
        # Load transactions
        transactions = db_manager.get_transactions(account_id, limit=100)
        for t in transactions:
            tree.insert("", tk.END, values=(
                t.get('transaction_id', ''),
                t['type'],
                f"₹{t['amount']:,.2f}",
                t.get('description', ''),
                t['timestamp']
            ))
            
    def delete_account_dialog(self):
        """Confirm and delete selected account."""
        selected = self.accounts_tree.selection()
        if not selected:
            return
            
        account_id = self.accounts_tree.item(selected[0], "values")[0]
        account_name = self.accounts_tree.item(selected[0], "values")[1]
        
        if messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete account #{account_id} ({account_name})?\n"
            "This will permanently delete all account data including transaction history."
        ):
            if db_manager.delete_account(account_id):
                messagebox.showinfo("Success", "Account deleted successfully")
                self.load_accounts()
                self.load_dashboard_stats()
            else:
                messagebox.showerror("Error", "Failed to delete account")
                
    def process_loan_application(self, decision):
        """Approve or reject a loan application."""
        selected = self.loans_tree.selection()
        if not selected:
            return
            
        app_id = self.loans_tree.item(selected[0], "values")[0]
        
        if decision == "Approved":
            message = "Approve this loan application?"
        else:
            message = "Reject this loan application?"
            
        if messagebox.askyesno("Confirm", message):
            if db_manager.update_loan_application(app_id, decision):
                messagebox.showinfo("Success", f"Loan application {decision.lower()}")
                self.load_loan_applications()
            else:
                messagebox.showerror("Error", "Failed to update loan application")
                
    def add_admin_dialog(self):
        """Show dialog to add a new admin user."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Administrator")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text="Username:").pack(pady=(10, 0))
        user_entry = ttk.Entry(dialog)
        user_entry.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(dialog, text="Full Name:").pack()
        name_entry = ttk.Entry(dialog)
        name_entry.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(dialog, text="Password:").pack()
        pwd_entry = ttk.Entry(dialog, show="*")
        pwd_entry.pack(fill=tk.X, padx=20, pady=5)
        
        def add_admin():
            username = user_entry.get().strip()
            full_name = name_entry.get().strip()
            password = pwd_entry.get()
            
            if not username or not password or not full_name:
                messagebox.showerror("Error", "All fields are required")
                return
                
            try:
                if db_manager.create_admin(username, full_name, password):
                    messagebox.showinfo("Success", "Administrator added successfully")
                    dialog.destroy()
                    self.load_admin_list()
                else:
                    messagebox.showerror("Error", "Failed to add administrator")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add administrator: {str(e)}")
                
        ttk.Button(
            dialog,
            text="Add Administrator",
            command=add_admin,
            style="Accent.TButton"
        ).pack(pady=10)
        
    def export_transactions(self):
        """Export transactions to CSV file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Save Transactions As"
        )
        
        if not file_path:
            return
            
        try:
            transactions = db_manager.get_all_transactions()
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Account", "Type", "Amount", "Description", "Date"])
                
                for t in transactions:
                    writer.writerow([
                        t['transaction_id'],
                        t['account_number'],
                        t['type'],
                        t['amount'],
                        t.get('description', ''),
                        t['timestamp']
                    ])
                    
            messagebox.showinfo("Success", f"Transactions exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export transactions: {str(e)}")
            
    def backup_database(self):
        """Create a backup of the database."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Database Files", "*.db"), ("All Files", "*.*")],
            title="Save Database Backup As"
        )
        
        if not file_path:
            return
            
        try:
            import shutil
            shutil.copyfile('bank.db', file_path)
            messagebox.showinfo("Success", f"Database backup created at {file_path}")
            self.update_status(f"Database backed up to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")
            self.update_status(f"Backup error: {str(e)}")
            
    def view_system_logs(self):
        """View system logs (placeholder implementation)."""
        messagebox.showinfo("Info", "System logs viewer will be implemented in a future version")
        
    # UI helper methods
    def show_account_context_menu(self, event):
        """Show context menu for account actions."""
        item = self.accounts_tree.identify_row(event.y)
        if item:
            self.accounts_tree.selection_set(item)
            self.account_menu.post(event.x_root, event.y_root)
            
    def show_loan_context_menu(self, event):
        """Show context menu for loan actions."""
        item = self.loans_tree.identify_row(event.y)
        if item:
            self.loans_tree.selection_set(item)
            self.loan_menu.post(event.x_root, event.y_root)
            
    def update_status(self, message: str):
        """Update the status bar message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"[{timestamp}] {message}")
        
    def logout(self):
        """Handle logout process."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            from ui.login_window import show_login_window
            show_login_window()
            
    def run(self):
        """Run the admin panel application."""
        self.root.mainloop()

def open_admin_panel():
    """Entry point for opening the admin panel."""
    # First authenticate the admin
    username = simpledialog.askstring("Admin Login", "Username:", show="*")
    password = simpledialog.askstring("Admin Login", "Password:", show="*")
    
    if username and password:
        if db_manager.authenticate_admin(username, password):
            app = AdminPanel()
            app.admin_user = username
            app.admin_info_var.set(f"Logged in as: {username}")
            app.run()
        else:
            messagebox.showerror("Access Denied", "Invalid admin credentials")