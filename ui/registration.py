# ui/registration.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import create_account
from ui.login_window import show_login_window
from ui.themes import BankTheme, IconManager, AnimationUtils, ModernButton
import re

class RegistrationWindow:
    def __init__(self, navigator=None):
        self.navigator = navigator
        self.root = tk.Tk()
        self.root.title("🏦 Banking System - Account Registration")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(bg=BankTheme.COLORS['background'])
        
        # Configure theme
        self.style = BankTheme.configure_styles()
        
        # Center window
        self.center_window()
        
        self.setup_ui()
        
        # Add fade in animation
        AnimationUtils.fade_in(self.root)
        
    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """Initialize all UI components with modern banking design."""
        # Header section
        header_frame = tk.Frame(self.root, bg=BankTheme.COLORS['primary'], height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Bank logo and title
        logo_frame = tk.Frame(header_frame, bg=BankTheme.COLORS['primary'])
        logo_frame.pack(expand=True, fill=tk.BOTH, pady=15)
        
        bank_icon = tk.Label(
            logo_frame,
            text=IconManager.get_icon('bank'),
            font=('Segoe UI', 24),
            bg=BankTheme.COLORS['primary'],
            fg=BankTheme.COLORS['text_white']
        )
        bank_icon.pack(pady=(0, 5))
        
        title_label = tk.Label(
            logo_frame,
            text="Create New Account",
            font=BankTheme.FONTS['heading'],
            bg=BankTheme.COLORS['primary'],
            fg=BankTheme.COLORS['text_white']
        )
        title_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg=BankTheme.COLORS['background'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=30)
        
        # Registration card
        reg_card = tk.Frame(
            main_frame,
            bg=BankTheme.COLORS['card_bg'],
            relief='flat',
            bd=1,
            highlightbackground=BankTheme.COLORS['border']
        )
        reg_card.pack(fill=tk.BOTH, expand=True)
        
        # Form frame
        form_frame = tk.Frame(reg_card, bg=BankTheme.COLORS['card_bg'])
        form_frame.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)
        
        # Form header
        form_header = tk.Label(
            form_frame,
            text="Join Our Banking Family",
            font=BankTheme.FONTS['subheading'],
            bg=BankTheme.COLORS['card_bg'],
            fg=BankTheme.COLORS['text_primary']
        )
        form_header.pack(pady=(0, 20))
        
        # Form fields
        self.create_input_field(
            form_frame,
            "Full Name",
            IconManager.get_icon('account'),
            'name_entry'
        )
        
        self.create_input_field(
            form_frame,
            "Password",
            IconManager.get_icon('security'),
            'pwd_entry',
            show="•"
        )
        
        self.create_input_field(
            form_frame,
            "Confirm Password",
            IconManager.get_icon('security'),
            'confirm_pwd_entry',
            show="•"
        )
        
        # Password requirements
        req_frame = tk.Frame(form_frame, bg=BankTheme.COLORS['card_bg'])
        req_frame.pack(fill=tk.X, pady=(0, 20))
        
        req_label = tk.Label(
            req_frame,
            text="Password Requirements:",
            font=BankTheme.FONTS['small'],
            bg=BankTheme.COLORS['card_bg'],
            fg=BankTheme.COLORS['text_secondary']
        )
        req_label.pack(anchor=tk.W)
        
        requirements = [
            "• At least 8 characters long",
            "• Contains uppercase and lowercase letters",
            "• Contains at least one number",
            "• Contains at least one special character"
        ]
        
        for req in requirements:
            req_item = tk.Label(
                req_frame,
                text=req,
                font=BankTheme.FONTS['small'],
                bg=BankTheme.COLORS['card_bg'],
                fg=BankTheme.COLORS['text_muted']
            )
            req_item.pack(anchor=tk.W, padx=(10, 0))
        
        # Register button
        register_btn = ModernButton(
            form_frame,
            "Create Account",
            self.register,
            style='primary',
            icon=IconManager.get_icon('add'),
            width=20
        )
        register_btn.pack(pady=(20, 10), fill=tk.X)
        
        # Login link
        login_frame = tk.Frame(form_frame, bg=BankTheme.COLORS['card_bg'])
        login_frame.pack(fill=tk.X, pady=(10, 0))
        
        login_text = tk.Label(
            login_frame,
            text="Already have an account?",
            font=BankTheme.FONTS['small'],
            bg=BankTheme.COLORS['card_bg'],
            fg=BankTheme.COLORS['text_secondary']
        )
        login_text.pack(side=tk.LEFT)
        
        login_link = tk.Label(
            login_frame,
            text="Sign In",
            font=BankTheme.FONTS['small'],
            bg=BankTheme.COLORS['card_bg'],
            fg=BankTheme.COLORS['primary'],
            cursor='hand2'
        )
        login_link.pack(side=tk.LEFT, padx=(5, 0))
        login_link.bind("<Button-1>", lambda e: self.back_to_login())
        
        # Footer
        footer_frame = tk.Frame(self.root, bg=BankTheme.COLORS['footer'], height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        footer_text = tk.Label(
            footer_frame,
            text="By creating an account, you agree to our Terms of Service and Privacy Policy",
            font=BankTheme.FONTS['small'],
            bg=BankTheme.COLORS['footer'],
            fg=BankTheme.COLORS['text_light']
        )
        footer_text.pack(expand=True)

    def create_input_field(self, parent, label_text, icon, var_name, show=None):
        """Create a modern input field with icon and styling."""
        # Container frame
        field_frame = tk.Frame(parent, bg=BankTheme.COLORS['card_bg'])
        field_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Label with icon
        label_frame = tk.Frame(field_frame, bg=BankTheme.COLORS['card_bg'])
        label_frame.pack(fill=tk.X, pady=(0, 5))
        
        icon_label = tk.Label(
            label_frame,
            text=icon,
            font=('Segoe UI', 12),
            bg=BankTheme.COLORS['card_bg'],
            fg=BankTheme.COLORS['primary']
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 8))
        
        label = tk.Label(
            label_frame,
            text=label_text,
            font=BankTheme.FONTS['body'],
            bg=BankTheme.COLORS['card_bg'],
            fg=BankTheme.COLORS['text_primary']
        )
        label.pack(side=tk.LEFT)
        
        # Input field with styling
        entry_frame = tk.Frame(field_frame, bg=BankTheme.COLORS['card_bg'])
        entry_frame.pack(fill=tk.X)
        
        entry = tk.Entry(
            entry_frame,
            font=BankTheme.FONTS['body'],
            bg=BankTheme.COLORS['card_bg'],
            fg=BankTheme.COLORS['text_primary'],
            relief='flat',
            bd=2,
            highlightbackground=BankTheme.COLORS['border'],
            highlightcolor=BankTheme.COLORS['focus_border'],
            highlightthickness=1,
            show=show
        )
        entry.pack(fill=tk.X, ipady=8)
        
        # Add focus effects
        def on_focus_in(event):
            entry.configure(highlightbackground=BankTheme.COLORS['focus_border'])
        
        def on_focus_out(event):
            entry.configure(highlightbackground=BankTheme.COLORS['border'])
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        # Store entry reference
        setattr(self, var_name, entry)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("Accent.TButton", foreground="white", background="#4a6baf")
        
    def validate_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True
        
    def register(self):
        name = self.name_entry.get().strip()
        pwd = self.pwd_entry.get()
        confirm_pwd = self.confirm_pwd_entry.get()
        
        if not name or not pwd or not confirm_pwd:
            messagebox.showwarning("Input Error", "All fields are required")
            return
            
        if pwd != confirm_pwd:
            messagebox.showwarning("Input Error", "Passwords do not match")
            return
            
        if not self.validate_password(pwd):
            messagebox.showwarning("Password Error", 
                "Password must be at least 8 characters with a number and special character")
            return
            
        account_number = create_account(name, pwd)
        if account_number:
            messagebox.showinfo("Success", 
                f"Account created successfully!\nYour account number is: {account_number}\nPlease keep it safe.")
            self.root.destroy()
            show_login_window()
        else:
            messagebox.showerror("Error", "Account creation failed. Please try again.")
            
    def back_to_login(self):
        self.root.destroy()
        show_login_window()
        
    def show(self):
        """Display the registration window."""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        
    def run(self):
        self.root.mainloop()

def open_registration_window():
    app = RegistrationWindow()
    app.run()