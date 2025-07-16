# ui/login_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from utils.helpers import validate_input
from ui.themes import BankTheme, IconManager, AnimationUtils, ModernButton, GradientFrame

class LoginWindow:
    def __init__(self, navigator):
        self.navigator = navigator
        self.window = tk.Toplevel()
        self.window.title("🏦 Banking System - Login")
        self.window.geometry("520x680")
        self.window.resizable(False, False)
        self.window.configure(bg=BankTheme.COLORS['background'])
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Configure theme
        self.style = BankTheme.configure_styles()
        
        # Initialize animation variables
        self.animation_step = 0
        self.animation_direction = 1
        self.logo_elements = []
        
        # Center window
        self.center_window()
        
        self.setup_ui()
        
        # Add fade in animation
        AnimationUtils.fade_in(self.window)

    def create_animated_logo(self, canvas):
        """Create animated logo elements."""
        # Clear previous elements
        canvas.delete("all")
        
        # Create bank building silhouette
        building_color = "#FFD700"  # Gold color
        
        # Main building
        canvas.create_rectangle(80, 40, 120, 80, fill=building_color, outline="#FFA500", width=2)
        
        # Side buildings
        canvas.create_rectangle(60, 50, 80, 80, fill="#FFA500", outline="#FF8C00", width=1)
        canvas.create_rectangle(120, 50, 140, 80, fill="#FFA500", outline="#FF8C00", width=1)
        
        # Pillars
        for x in [85, 95, 105, 115]:
            canvas.create_rectangle(x, 50, x+3, 75, fill="#FFFFFF", outline="#E0E0E0")
        
        # Roof
        canvas.create_polygon(75, 40, 100, 25, 125, 40, fill="#FF6B35", outline="#FF4500", width=2)
        
        # Windows with glow effect
        for i, x in enumerate([65, 75, 125, 135]):
            for y in [55, 65]:
                glow_color = "#FFFF00" if (i + y) % 2 == 0 else "#00FFFF"
                canvas.create_rectangle(x, y, x+6, y+6, fill=glow_color, outline=glow_color)
        
        # Animated dollar sign
        canvas.create_text(100, 60, text="$", font=("Arial", 16, "bold"), fill="#00FF00")
        
        # Animated particles around the logo
        self.create_particles(canvas)
        
    def create_particles(self, canvas):
        """Create animated particles around the logo."""
        import random
        import math
        
        # Create floating particles
        for i in range(8):
            angle = (i * 45) + self.animation_step
            radius = 30 + 10 * math.sin(self.animation_step * 0.1)
            x = 100 + radius * math.cos(math.radians(angle))
            y = 50 + radius * math.sin(math.radians(angle))
            
            # Alternating colors
            colors = ["#FFD700", "#00FFFF", "#FF69B4", "#00FF00"]
            color = colors[i % len(colors)]
            
            canvas.create_oval(x-3, y-3, x+3, y+3, fill=color, outline=color)
            
    def animate_logo(self, canvas):
        """Animate the logo continuously."""
        if hasattr(self, 'window') and self.window.winfo_exists():
            self.animation_step += 2
            if self.animation_step >= 360:
                self.animation_step = 0
                
            # Recreate animated elements
            self.create_animated_logo(canvas)
            
            # Schedule next animation frame
            self.window.after(100, lambda: self.animate_logo(canvas))

    def center_window(self):
        """Center the window on screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Initialize all UI components with modern banking design."""
        # Header section with gradient background
        header_frame = tk.Frame(self.window, bg=BankTheme.COLORS['primary'], height=160)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Add a subtle border at the bottom of header
        border_frame = tk.Frame(self.window, bg=BankTheme.COLORS['secondary'], height=3)
        border_frame.pack(fill=tk.X)
        
        # Bank logo and title
        logo_frame = tk.Frame(header_frame, bg=BankTheme.COLORS['primary'])
        logo_frame.pack(expand=True, fill=tk.BOTH, pady=30)
        
        # Animated bank logo
        logo_canvas = tk.Canvas(
            logo_frame,
            width=200,
            height=100,
            bg=BankTheme.COLORS['primary'],
            highlightthickness=0
        )
        logo_canvas.pack(pady=(0, 10))
        
        # Create animated logo elements
        self.create_animated_logo(logo_canvas)
        
        # Start logo animation
        self.animate_logo(logo_canvas)
        
        subtitle_label = tk.Label(
            logo_frame,
            text="Your Trusted Banking Partner",
            font=('Segoe UI', 12),
            bg=BankTheme.COLORS['primary'],
            fg=BankTheme.COLORS['text_white']
        )
        subtitle_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.window, bg=BankTheme.COLORS['background'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=30)
        
        # Login card
        login_card = tk.Frame(
            main_frame,
            bg=BankTheme.COLORS['card_bg'],
            relief='flat',
            bd=1,
            highlightbackground=BankTheme.COLORS['border']
        )
        login_card.pack(fill=tk.BOTH, expand=True)
        
        # Login form
        form_frame = tk.Frame(login_card, bg=BankTheme.COLORS['card_bg'])
        form_frame.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)
        
        # Login header
        login_header = tk.Label(
            form_frame,
            text="Sign In to Your Account",
            font=BankTheme.FONTS['heading'],
            bg=BankTheme.COLORS['card_bg'],
            fg=BankTheme.COLORS['text_primary']
        )
        login_header.pack(pady=(0, 20))
        
        # Account number field
        self.create_input_field(
            form_frame,
            "Account Number",
            IconManager.get_icon('account'),
            'acc_entry'
        )
        
        # Password field
        self.create_input_field(
            form_frame,
            "Password",
            IconManager.get_icon('security'),
            'pwd_entry',
            show="•"
        )
        
        # Login button
        login_btn = ModernButton(
            form_frame,
            "Sign In",
            self.attempt_login,
            style='primary',
            icon=IconManager.get_icon('key'),
            width=20
        )
        login_btn.pack(pady=(20, 10), fill=tk.X)
        
        # Divider
        divider_frame = tk.Frame(form_frame, bg=BankTheme.COLORS['card_bg'])
        divider_frame.pack(fill=tk.X, pady=15)
        
        divider_line = tk.Frame(divider_frame, bg=BankTheme.COLORS['border'], height=1)
        divider_line.pack(fill=tk.X, pady=5)
        
        divider_text = tk.Label(
            divider_frame,
            text="or",
            font=BankTheme.FONTS['small'],
            bg=BankTheme.COLORS['card_bg'],
            fg=BankTheme.COLORS['text_muted']
        )
        divider_text.pack()
        
        # Register button
        register_btn = ModernButton(
            form_frame,
            "Create New Account",
            self.navigator.show_register,
            style='outline',
            icon=IconManager.get_icon('add'),
            width=20
        )
        register_btn.pack(pady=(10, 0), fill=tk.X)
        
        # Admin access
        admin_frame = tk.Frame(form_frame, bg=BankTheme.COLORS['card_bg'])
        admin_frame.pack(fill=tk.X, pady=(20, 0))
        
        admin_separator = tk.Frame(admin_frame, bg=BankTheme.COLORS['border'], height=1)
        admin_separator.pack(fill=tk.X, pady=(0, 10))
        
        admin_btn = ModernButton(
            admin_frame,
            "Admin Login",
            self.show_admin_login,
            style='secondary',
            icon=IconManager.get_icon('shield'),
            width=20
        )
        admin_btn.pack(fill=tk.X)
        
        # Footer
        footer_frame = tk.Frame(self.window, bg=BankTheme.COLORS['footer'], height=50)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        footer_text = tk.Label(
            footer_frame,
            text="© 2025 Modern Banking System. All rights reserved. | 📞 1-800-HELP | 🌐 www.bankingsystem.com",
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

    def attempt_login(self):
        """Handle login attempt"""
        acc = self.acc_entry.get().strip()
        pwd = self.pwd_entry.get()

        if not validate_input(acc, "account_number"):
            messagebox.showwarning("Invalid Input", "Please enter a valid account number")
            return

        if not validate_input(pwd, "password"):
            messagebox.showwarning("Invalid Input", "Password must be at least 8 characters")
            return

        # Import inside method to avoid circular imports
        from database.db_manager import db_manager
        if db_manager.authenticate_user(acc, pwd):
            self.window.destroy()
            from ui.bank_dashboard import BankDashboard
            BankDashboard(acc).run()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def show_admin_login(self):
        """Show admin login dialog"""
        from ui.admin_login import AdminLoginDialog
        AdminLoginDialog(self.window)

    def on_close(self):
        """Handle window close"""
        if messagebox.askokcancel("Quit", "Do you want to exit the banking system?"):
            self.window.destroy()
            self.navigator.root.quit()

    def show(self):
        """Display the window"""
        self.window.deiconify()
        self.window.grab_set()

def show_login_window():
    """Standalone function to show login window."""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    class DummyNavigator:
        def __init__(self):
            self.root = root
        
        def show_register(self):
            messagebox.showinfo("Coming Soon", "Registration will open the registration window")
    
    nav = DummyNavigator()
    login = LoginWindow(nav)
    login.show()
    
    root.mainloop()