# ui/bank_dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Optional, List, Dict
import csv
import webbrowser
from database.db_manager import db_manager
from utils.predictor import predict_loan_eligibility
from utils.helpers import format_currency
from ui.themes import BankTheme, IconManager, AnimationUtils, CardWidget, StatCard

class BankDashboard:
    """Main banking dashboard with account management features."""
    
    def __init__(self, account_number: int):
        self.account_number = account_number
        self.root = tk.Tk()
        self.root.title(f"🏦 Banking Dashboard | Account #{account_number}")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=BankTheme.COLORS['background'])
        
        # Configure theme
        self.style = BankTheme.configure_styles()
        
        # Initialize cleanup flag
        self.is_closing = False
        
        # Load account details
        self.account_details = db_manager.get_account_details(account_number)
        if not self.account_details:
            messagebox.showerror("Error", "Account not found!")
            self.root.destroy()
            return
        
        # Center window
        self.center_window()
        
        # Set up window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        self.setup_ui()
        self.load_account_summary()
        
        # Add fade in animation
        AnimationUtils.fade_in(self.root)
        
    def setup_ui(self):
        """Initialize all UI components."""
        # Main layout - horizontal split
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar for navigation
        self.create_sidebar(main_paned)
        
        # Right content area
        self.create_content_area(main_paned)
        
        # Status bar
        self.create_status_bar()
        
    def create_sidebar(self, parent):
        """Create the navigation sidebar."""
        sidebar_frame = tk.Frame(parent, bg=BankTheme.COLORS['sidebar'], width=250)
        sidebar_frame.pack_propagate(False)
        parent.add(sidebar_frame, weight=0)
        
        # User info section
        user_frame = tk.Frame(sidebar_frame, bg=BankTheme.COLORS['sidebar'])
        user_frame.pack(fill=tk.X, pady=20, padx=20)
        
        # User avatar
        avatar_label = tk.Label(
            user_frame, 
            text=IconManager.get_icon('account'), 
            font=('Segoe UI', 30),
            bg=BankTheme.COLORS['sidebar'],
            fg=BankTheme.COLORS['sidebar_text']
        )
        avatar_label.pack(pady=(0, 10))
        
        # User name
        name_label = tk.Label(
            user_frame, 
            text=self.account_details['name'], 
            font=BankTheme.FONTS['subheading'],
            bg=BankTheme.COLORS['sidebar'],
            fg=BankTheme.COLORS['sidebar_text']
        )
        name_label.pack()
        
        # Account number
        acc_label = tk.Label(
            user_frame, 
            text=f"Account #{self.account_number}", 
            font=BankTheme.FONTS['small'],
            bg=BankTheme.COLORS['sidebar'],
            fg=BankTheme.COLORS['text_muted']
        )
        acc_label.pack(pady=(5, 0))
        
        # Balance display
        self.sidebar_balance_var = tk.StringVar()
        self.balance_var = tk.StringVar()  # Initialize balance_var for main display
        balance_label = tk.Label(
            user_frame, 
            textvariable=self.sidebar_balance_var, 
            font=BankTheme.FONTS['heading'],
            bg=BankTheme.COLORS['sidebar'],
            fg=BankTheme.COLORS['accent']
        )
        balance_label.pack(pady=(10, 0))
        
        # Separator
        separator = tk.Frame(sidebar_frame, height=2, bg=BankTheme.COLORS['border'])
        separator.pack(fill=tk.X, pady=20)
        
        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ('dashboard', 'Dashboard', 'dashboard'),
            ('transactions', 'Transactions', 'transaction'),
            ('transfer', 'Transfer Money', 'transfer'),
            ('loans', 'Loans', 'loan'),
            ('settings', 'Settings', 'settings'),
        ]
        
        for key, text, icon in nav_items:
            btn_frame = tk.Frame(sidebar_frame, bg=BankTheme.COLORS['sidebar'])
            btn_frame.pack(fill=tk.X, padx=10, pady=2)
            
            btn = tk.Button(
                btn_frame,
                text=f"{IconManager.get_icon(icon)}  {text}",
                font=BankTheme.FONTS['button'],
                bg=BankTheme.COLORS['sidebar'],
                fg=BankTheme.COLORS['sidebar_text'],
                activebackground='#374151',
                activeforeground='white',
                bd=0,
                pady=12,
                anchor='w',
                command=lambda k=key: self.switch_tab(k)
            )
            btn.pack(fill=tk.X)
            self.nav_buttons[key] = btn
        
        # Logout button at bottom
        logout_frame = tk.Frame(sidebar_frame, bg=BankTheme.COLORS['sidebar'])
        logout_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=20)
        
        logout_btn = tk.Button(
            logout_frame,
            text=f"{IconManager.get_icon('logout')}  Logout",
            font=BankTheme.FONTS['button'],
            bg=BankTheme.COLORS['danger'],
            fg='white',
            activebackground='#dc2626',
            activeforeground='white',
            bd=0,
            pady=12,
            command=self.logout
        )
        logout_btn.pack(fill=tk.X)
        
    def create_content_area(self, parent):
        """Create the main content area."""
        content_frame = ttk.Frame(parent)
        parent.add(content_frame, weight=1)
        
        # Header
        self.create_header(content_frame)
        
        # Main content with notebook
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_transactions_tab()
        self.create_transfer_tab()
        self.create_loans_tab()
        self.create_settings_tab()
        
        # Bind tab change event
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
    def create_header(self, parent):
        """Create the header section."""
        header_frame = tk.Frame(parent, bg=BankTheme.COLORS['primary'], height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Welcome message
        welcome_label = tk.Label(
            header_frame,
            text=f"Welcome back, {self.account_details['name']}!",
            font=BankTheme.FONTS['heading'],
            bg=BankTheme.COLORS['primary'],
            fg='white'
        )
        welcome_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Current time
        self.time_var = tk.StringVar()
        time_label = tk.Label(
            header_frame,
            textvariable=self.time_var,
            font=BankTheme.FONTS['small'],
            bg=BankTheme.COLORS['primary'],
            fg='white'
        )
        time_label.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Update time every second
        self.update_time()
        
    def update_time(self):
        """Update the current time display."""
        if self.is_closing:
            return
            
        try:
            # Check if the root window still exists and is valid
            if hasattr(self, 'root') and self.root.winfo_exists():
                current_time = datetime.now().strftime("%A, %B %d, %Y - %I:%M:%S %p")
                if hasattr(self, 'time_var'):
                    self.time_var.set(current_time)
                    # Schedule next update
                    self.root.after(1000, self.update_time)
        except (tk.TclError, AttributeError):
            # Widget has been destroyed or is invalid, stop the timer
            return
            
    def on_window_close(self):
        """Handle window close event."""
        self.is_closing = True
        self.root.destroy()
        from ui.login_window import show_login_window
        show_login_window()
        
    def switch_tab(self, tab_key):
        """Switch to the specified tab."""
        tab_mapping = {
            'dashboard': 0,
            'transactions': 1,
            'transfer': 2,
            'loans': 3,
            'settings': 4
        }
        
        if tab_key in tab_mapping:
            self.notebook.select(tab_mapping[tab_key])
            
            # Update sidebar button states
            for key, btn in self.nav_buttons.items():
                if key == tab_key:
                    btn.config(bg='#374151', fg='white')
                else:
                    btn.config(bg=BankTheme.COLORS['sidebar'], fg=BankTheme.COLORS['sidebar_text'])
    
    def on_tab_changed(self, event):
        """Handle tab change event."""
        selected_tab = self.notebook.index(self.notebook.select())
        tab_keys = ['dashboard', 'transactions', 'transfer', 'loans', 'settings']
        
        if 0 <= selected_tab < len(tab_keys):
            current_tab = tab_keys[selected_tab]
            
            # Update sidebar button states
            for key, btn in self.nav_buttons.items():
                if key == current_tab:
                    btn.config(bg='#374151', fg='white')
                else:
                    btn.config(bg=BankTheme.COLORS['sidebar'], fg=BankTheme.COLORS['sidebar_text'])
    
    def create_status_bar(self):
        """Create the status bar."""
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var,
            font=BankTheme.FONTS['small'],
            bg=BankTheme.COLORS['surface_dark'],
            fg=BankTheme.COLORS['text_secondary'],
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.update_status("Ready")
        
    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_dashboard_tab(self):
        """Create the main dashboard tab with quick actions."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dashboard")
        
        # Quick actions frame
        actions_frame = ttk.LabelFrame(tab, text="Quick Actions", padding=10)
        actions_frame.pack(fill=tk.X, pady=5)
        
        # Amount entry
        ttk.Label(actions_frame, text="Amount (₹):").grid(row=0, column=0, sticky=tk.W)
        self.amount_entry = ttk.Entry(actions_frame)
        self.amount_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(actions_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Deposit", 
            command=self.perform_deposit,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Withdraw", 
            command=self.perform_withdraw
        ).pack(side=tk.LEFT, padx=5)
        
        actions_frame.columnconfigure(1, weight=1)
        
        # Recent transactions preview
        ttk.Label(tab, text="Recent Transactions", style="Header.TLabel").pack(anchor=tk.W, pady=(15, 5))
        
        self.recent_transactions_tree = ttk.Treeview(
            tab, 
            columns=("Type", "Amount", "Date"), 
            show="headings",
            height=5
        )
        self.recent_transactions_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns
        for col in ("Type", "Amount", "Date"):
            self.recent_transactions_tree.heading(col, text=col)
            self.recent_transactions_tree.column(col, width=100, anchor=tk.CENTER if col != "Type" else tk.W)
        
        # Load recent transactions
        self.load_recent_transactions()
        
    def create_transactions_tab(self):
        """Create the transactions history tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transactions")
        
        # Filter frame
        filter_frame = ttk.Frame(tab)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_type_var = tk.StringVar(value="All")
        ttk.Combobox(
            filter_frame,
            textvariable=self.filter_type_var,
            values=["All", "Deposit", "Withdrawal", "Transfer"],
            state="readonly",
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            filter_frame,
            text="Apply",
            command=self.load_transactions
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            filter_frame,
            text="Export CSV",
            command=self.export_transactions
        ).pack(side=tk.RIGHT)
        
        # Transactions treeview
        self.transactions_tree = ttk.Treeview(
            tab,
            columns=("ID", "Type", "Amount", "Description", "Date"),
            show="headings",
            height=15
        )
        self.transactions_tree.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Configure columns
        col_widths = {"ID": 50, "Type": 80, "Amount": 100, "Description": 200, "Date": 120}
        for col in self.transactions_tree["columns"]:
            self.transactions_tree.heading(col, text=col)
            self.transactions_tree.column(col, width=col_widths.get(col, 100), 
                                        anchor=tk.CENTER if col not in ("Description", "Type") else tk.W)
        
        # Load transactions
        self.load_transactions()
        
    def create_transfer_tab(self):
        """Create the money transfer tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transfer")
        
        # Transfer form
        form_frame = ttk.Frame(tab, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Recipient Account Number:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.recipient_entry = ttk.Entry(form_frame)
        self.recipient_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Amount (₹):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.transfer_amount_entry = ttk.Entry(form_frame)
        self.transfer_amount_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.transfer_desc_entry = ttk.Entry(form_frame)
        self.transfer_desc_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Button(
            form_frame,
            text="Send Money",
            command=self.perform_transfer,
            style="Accent.TButton"
        ).grid(row=3, column=0, columnspan=2, pady=10)
        
        form_frame.columnconfigure(1, weight=1)
        
    def create_loans_tab(self):
        """Create the loans and eligibility tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Loans")
        
        # Loan application form
        form_frame = ttk.LabelFrame(tab, text="Loan Eligibility Check", padding=10)
        form_frame.pack(fill=tk.X, pady=5)
        
        fields = [
            ("Monthly Income (₹):", "income_entry"),
            ("Credit Score (300-850):", "score_entry"),
            ("Loan Amount (₹):", "loan_amt_entry"),
            ("Loan Term (months):", "term_entry")
        ]
        
        for i, (label, var_name) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, sticky=tk.EW, padx=5, pady=2)
            setattr(self, var_name, entry)
            
        # Result display
        self.loan_result_var = tk.StringVar()
        ttk.Label(
            form_frame,
            textvariable=self.loan_result_var,
            font=("Helvetica", 10),
            wraplength=300
        ).grid(row=len(fields), column=0, columnspan=2, pady=5)
        
        ttk.Button(
            form_frame,
            text="Check Eligibility",
            command=self.check_loan_eligibility,
            style="Accent.TButton"
        ).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Loan history
        ttk.Label(tab, text="My Loan Applications", style="Header.TLabel").pack(anchor=tk.W, pady=(15, 5))
        
        self.loans_tree = ttk.Treeview(
            tab,
            columns=("ID", "Amount", "Term", "Status", "Date"),
            show="headings",
            height=5
        )
        self.loans_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Configure columns
        for col in self.loans_tree["columns"]:
            self.loans_tree.heading(col, text=col)
            self.loans_tree.column(col, width=80, anchor=tk.CENTER if col != "Status" else tk.W)
        
        # Load loan history
        self.load_loan_history()
        
    def create_settings_tab(self):
        """Create the settings and help tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Settings")
        
        # Account info
        info_frame = ttk.LabelFrame(tab, text="Account Information", padding=10)
        info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(info_frame, text=f"Account Number: {self.account_number}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Account Holder: {self.account_details['name']}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Member Since: {self.account_details['created_at'][:10]}").pack(anchor=tk.W)
        
        # Help section
        help_frame = ttk.LabelFrame(tab, text="Help & Support", padding=10)
        help_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            help_frame,
            text="Contact Customer Support",
            command=lambda: webbrowser.open("mailto:support@bank.com")
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            help_frame,
            text="View FAQ",
            command=lambda: webbrowser.open("https://bank.com/faq")
        ).pack(fill=tk.X, pady=2)
        
        # Logout button
        ttk.Button(
            tab,
            text="Logout",
            command=self.logout,
            style="Accent.TButton"
        ).pack(side=tk.BOTTOM, pady=10)
        
    def load_account_summary(self):
        """Load and display account summary information."""
        # Refresh account details from database
        self.account_details = db_manager.get_account_details(self.account_number)
        balance = self.account_details['balance']
        
        # Update both balance displays
        self.balance_var.set(f"Balance: ₹{balance:,.2f}")
        self.sidebar_balance_var.set(f"₹{balance:,.2f}")
        
        self.update_status("Account summary updated")
        
    def load_recent_transactions(self):
        """Load recent transactions for the dashboard preview."""
        transactions = db_manager.get_transactions(self.account_number, limit=5)
        self.update_transactions_tree(self.recent_transactions_tree, transactions)
        
    def load_transactions(self):
        """Load full transaction history with filters."""
        trans_type = self.filter_type_var.get()
        transactions = db_manager.get_transactions(self.account_number, limit=100)
        
        if trans_type != "All":
            transactions = [t for t in transactions if t['type'] == trans_type]
            
        self.update_transactions_tree(self.transactions_tree, transactions)
        
    def update_transactions_tree(self, tree: ttk.Treeview, transactions: List[Dict]):
        """Update a treeview with transaction data."""
        tree.delete(*tree.get_children())
        
        for t in transactions:
            amount = f"₹{t['amount']:,.2f}"
            if t['type'] in ("Withdrawal", "Transfer Out"):
                amount = f"-{amount}"
                
            tree.insert("", tk.END, values=(
                t.get('transaction_id', ''),
                t['type'],
                amount,
                t.get('description', ''),
                t['timestamp']
            ))
            
    def load_loan_history(self):
        """Load the user's loan application history."""
        loans = db_manager.get_loan_applications(self.account_number)
        self.loans_tree.delete(*self.loans_tree.get_children())
        
        # Configure tags for status colors
        self.loans_tree.tag_configure("approved", foreground="green")
        self.loans_tree.tag_configure("rejected", foreground="red")
        self.loans_tree.tag_configure("pending", foreground="orange")
        
        for loan in loans:
            status = loan.get('status', 'Pending')
            decision_date = loan.get('decision_date', 'N/A')
            
            # Format decision date
            if decision_date and decision_date != 'N/A':
                try:
                    if isinstance(decision_date, str):
                        decision_date = decision_date[:10]  # Get just the date part
                except:
                    decision_date = 'N/A'
            
            # Determine tag based on status
            tag = ""
            if status.lower() == "approved":
                tag = "approved"
            elif status.lower() == "rejected":
                tag = "rejected"
            elif status.lower() == "pending":
                tag = "pending"
            
            item = self.loans_tree.insert("", tk.END, values=(
                loan['application_id'],
                f"₹{loan['loan_amount']:,.2f}",
                f"{loan['loan_term']} months",
                status,
                decision_date
            ))
            
            # Apply color tag
            if tag:
                self.loans_tree.item(item, tags=(tag,))
            
    def perform_deposit(self):
        """Handle deposit operation."""
        amount_str = self.amount_entry.get()
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")
                
            if db_manager.deposit(self.account_number, amount):
                messagebox.showinfo("Success", f"Deposit of ₹{amount:,.2f} completed successfully")
                self.amount_entry.delete(0, tk.END)
                self.load_account_summary()
                self.load_recent_transactions()
                self.load_transactions()
            else:
                messagebox.showerror("Error", "Deposit failed. Please try again.")
                
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid positive number")
            
    def perform_withdraw(self):
        """Handle withdrawal operation."""
        amount_str = self.amount_entry.get()
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")
                
            if db_manager.withdraw(self.account_number, amount):
                messagebox.showinfo("Success", f"Withdrawal of ₹{amount:,.2f} completed successfully")
                self.amount_entry.delete(0, tk.END)
                self.load_account_summary()
                self.load_recent_transactions()
                self.load_transactions()
            else:
                messagebox.showerror("Error", "Withdrawal failed. Insufficient balance or other error.")
                
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid positive number")
            
    def perform_transfer(self):
        """Handle money transfer to another account."""
        recipient = self.recipient_entry.get()
        amount_str = self.transfer_amount_entry.get()
        description = self.transfer_desc_entry.get() or "Funds transfer"
        
        try:
            recipient_num = int(recipient)
            amount = float(amount_str)
            
            if amount <= 0:
                raise ValueError("Amount must be positive")
                
            if recipient_num == self.account_number:
                raise ValueError("Cannot transfer to your own account")
                
            if db_manager.transfer(self.account_number, recipient_num, amount, description):
                messagebox.showinfo(
                    "Success", 
                    f"Transfer of ₹{amount:,.2f} to account #{recipient_num} completed"
                )
                self.recipient_entry.delete(0, tk.END)
                self.transfer_amount_entry.delete(0, tk.END)
                self.transfer_desc_entry.delete(0, tk.END)
                self.load_account_summary()
                self.load_recent_transactions()
                self.load_transactions()
            else:
                messagebox.showerror(
                    "Transfer Failed", 
                    "Transfer could not be completed. Check recipient account and balance."
                )
                
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e) or "Please enter valid account number and amount")
            
    def check_loan_eligibility(self):
        """Check loan eligibility using ML model."""
        try:
            income = float(self.income_entry.get())
            credit_score = int(self.score_entry.get())
            loan_amount = float(self.loan_amt_entry.get())
            loan_term = int(self.term_entry.get())
            
            if income <= 0 or loan_amount <= 0 or loan_term <= 0:
                raise ValueError("Values must be positive")
                
            if credit_score < 300 or credit_score > 850:
                raise ValueError("Credit score must be between 300-850")
                
            # Predict eligibility
            eligible = predict_loan_eligibility(income, credit_score, loan_amount, loan_term)
            
            if eligible:
                result = "✅ Congratulations! You are eligible for this loan."
                color = "green"
                status = "Approved"
            else:
                result = "❌ Sorry, you are not eligible for this loan based on our criteria."
                color = "red"
                status = "Rejected"
                
            self.loan_result_var.set(result)
            self.loans_tree.item(self.loans_tree.selection(), tags=(color,))
            
            # Save application with predicted status
            db_manager.submit_loan_application(
                self.account_number,
                income,
                credit_score,
                loan_amount,
                loan_term,
                status  # Pass the predicted status
            )
            self.load_loan_history()
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e) or "Please enter valid numbers in all fields")
            
    def export_transactions(self):
        """Export transactions to CSV file."""
        transactions = db_manager.get_transactions(self.account_number)
        
        if not transactions:
            messagebox.showwarning("No Data", "No transactions to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Save Transactions As"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Type", "Amount", "Description", "Date"])
                
                for t in transactions:
                    writer.writerow([
                        t.get('transaction_id', ''),
                        t['type'],
                        t['amount'],
                        t.get('description', ''),
                        t['timestamp']
                    ])
                    
            messagebox.showinfo("Success", f"Transactions exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Error exporting transactions: {str(e)}")
            
    def update_status(self, message: str):
        """Update the status bar message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"[{timestamp}] {message}")
        
    def logout(self):
        """Handle logout process."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.is_closing = True
            self.root.destroy()
            from ui.login_window import show_login_window
            show_login_window()
            
    def run(self):
        """Run the application."""
        self.root.mainloop()

def open_dashboard(account_number: int):
    """Entry point for opening the dashboard."""
    app = BankDashboard(account_number)
    app.run()