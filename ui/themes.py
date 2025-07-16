# ui/themes.py
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class BankTheme:
    """Professional banking theme with modern colors and styling."""
    
    # Professional Banking Color Palette
    COLORS = {
        # Primary Colors
        'primary': '#1B4F72',        # Deep blue - trust and stability
        'primary_light': '#2E86AB',   # Light blue
        'primary_dark': '#0F263A',    # Dark blue
        
        # Secondary Colors
        'secondary': '#F39C12',       # Gold - premium feel
        'secondary_light': '#F4D03F', # Light gold
        'secondary_dark': '#D68910',  # Dark gold
        
        # Accent Colors
        'accent': '#E74C3C',         # Red for alerts
        'success': '#27AE60',        # Green for success
        'warning': '#F39C12',        # Orange for warnings
        'info': '#3498DB',           # Blue for information
        
        # Background Colors
        'background': '#F8F9FA',     # Light gray background
        'card_bg': '#FFFFFF',        # White card background
        'sidebar': '#1B4F72',        # Dark blue sidebar
        'header': '#2E86AB',         # Blue header
        'footer': '#34495E',         # Dark gray footer
        'surface_dark': '#34495E',   # Dark surface for status bar
        
        # Text Colors
        'text_primary': '#2C3E50',   # Dark gray primary text
        'text_secondary': '#7F8C8D', # Gray secondary text
        'text_light': '#BDC3C7',    # Light gray text
        'text_white': '#FFFFFF',     # White text
        'sidebar_text': '#FFFFFF',   # White sidebar text
        'text_muted': '#95A5A6',     # Muted text
        
        # Border Colors
        'border': '#BDC3C7',         # Light gray border
        'border_dark': '#7F8C8D',    # Dark gray border
        'focus_border': '#3498DB',   # Blue focus border
        
        # Status Colors
        'approved': '#27AE60',       # Green for approved
        'rejected': '#E74C3C',       # Red for rejected
        'pending': '#F39C12',        # Orange for pending
        'danger': '#E74C3C',         # Red for danger/error actions
        
        # Hover Effects
        'hover_light': '#ECF0F1',    # Light hover
        'hover_dark': '#34495E',     # Dark hover
    }
    
    # Professional Font System
    FONTS = {
        'heading': ('Segoe UI', 18, 'bold'),
        'subheading': ('Segoe UI', 14, 'bold'),
        'body': ('Segoe UI', 10),
        'small': ('Segoe UI', 8),
        'button': ('Segoe UI', 10, 'bold'),
        'logo': ('Segoe UI', 24, 'bold'),
        'amount': ('Segoe UI', 16, 'bold'),
        'card_title': ('Segoe UI', 12, 'bold'),
        'card_value': ('Segoe UI', 14, 'bold'),
    }
    
    # Spacing and Dimensions
    SPACING = {
        'xs': 5,
        'sm': 10,
        'md': 15,
        'lg': 20,
        'xl': 30,
        'xxl': 40,
    }
    
    @staticmethod
    def configure_styles():
        """Configure ttk styles for professional banking theme."""
        style = ttk.Style()
        
        # Configure theme
        style.theme_use('clam')
        
        # Main window styles
        style.configure('TFrame', background=BankTheme.COLORS['background'])
        style.configure('TLabel', background=BankTheme.COLORS['background'], 
                       foreground=BankTheme.COLORS['text_primary'], font=BankTheme.FONTS['body'])
        
        # Button styles
        style.configure('Accent.TButton',
                       background=BankTheme.COLORS['primary'],
                       foreground=BankTheme.COLORS['text_white'],
                       font=BankTheme.FONTS['button'],
                       borderwidth=0,
                       relief='flat')
        
        style.map('Accent.TButton',
                 background=[('active', BankTheme.COLORS['primary_light']),
                            ('pressed', BankTheme.COLORS['primary_dark'])])
        
        style.configure('Secondary.TButton',
                       background=BankTheme.COLORS['secondary'],
                       foreground=BankTheme.COLORS['text_white'],
                       font=BankTheme.FONTS['button'],
                       borderwidth=0,
                       relief='flat')
        
        style.map('Secondary.TButton',
                 background=[('active', BankTheme.COLORS['secondary_light']),
                            ('pressed', BankTheme.COLORS['secondary_dark'])])
        
        style.configure('Success.TButton',
                       background=BankTheme.COLORS['success'],
                       foreground=BankTheme.COLORS['text_white'],
                       font=BankTheme.FONTS['button'],
                       borderwidth=0,
                       relief='flat')
        
        style.configure('Danger.TButton',
                       background=BankTheme.COLORS['accent'],
                       foreground=BankTheme.COLORS['text_white'],
                       font=BankTheme.FONTS['button'],
                       borderwidth=0,
                       relief='flat')
        
        # Entry styles
        style.configure('TEntry',
                       fieldbackground=BankTheme.COLORS['card_bg'],
                       borderwidth=2,
                       relief='flat',
                       font=BankTheme.FONTS['body'])
        
        style.map('TEntry',
                 focuscolor=[('focus', BankTheme.COLORS['focus_border'])])
        
        # Combobox styles
        style.configure('TCombobox',
                       fieldbackground=BankTheme.COLORS['card_bg'],
                       borderwidth=2,
                       relief='flat',
                       font=BankTheme.FONTS['body'])
        
        # Treeview styles
        style.configure('Treeview',
                       background=BankTheme.COLORS['card_bg'],
                       foreground=BankTheme.COLORS['text_primary'],
                       fieldbackground=BankTheme.COLORS['card_bg'],
                       borderwidth=1,
                       relief='flat',
                       font=BankTheme.FONTS['body'])
        
        style.configure('Treeview.Heading',
                       background=BankTheme.COLORS['header'],
                       foreground=BankTheme.COLORS['text_white'],
                       font=BankTheme.FONTS['subheading'],
                       borderwidth=1,
                       relief='flat')
        
        # Notebook styles
        style.configure('TNotebook',
                       background=BankTheme.COLORS['background'],
                       borderwidth=0)
        
        style.configure('TNotebook.Tab',
                       background=BankTheme.COLORS['card_bg'],
                       foreground=BankTheme.COLORS['text_primary'],
                       font=BankTheme.FONTS['button'],
                       padding=[15, 10])
        
        style.map('TNotebook.Tab',
                 background=[('selected', BankTheme.COLORS['primary']),
                            ('active', BankTheme.COLORS['hover_light'])],
                 foreground=[('selected', BankTheme.COLORS['text_white'])])
        
        # LabelFrame styles
        style.configure('TLabelframe',
                       background=BankTheme.COLORS['card_bg'],
                       borderwidth=1,
                       relief='flat')
        
        style.configure('TLabelframe.Label',
                       background=BankTheme.COLORS['card_bg'],
                       foreground=BankTheme.COLORS['primary'],
                       font=BankTheme.FONTS['subheading'])
        
        # Progressbar styles
        style.configure('TProgressbar',
                       background=BankTheme.COLORS['primary'],
                       borderwidth=0,
                       relief='flat')
        
        # Separator styles
        style.configure('TSeparator',
                       background=BankTheme.COLORS['border'])
        
        # Custom styles for dashboard
        style.configure('Success.TFrame',
                       background=BankTheme.COLORS['success'],
                       borderwidth=0)
        
        style.configure('Header.TLabel',
                       background=BankTheme.COLORS['background'],
                       foreground=BankTheme.COLORS['primary'],
                       font=BankTheme.FONTS['subheading'])
        
        return style

class IconManager:
    """Manages icons and symbols for the banking interface."""
    
    ICONS = {
        'account': '👤',
        'balance': '💰',
        'deposit': '📥',
        'withdraw': '📤',
        'transfer': '↔️',
        'loan': '🏦',
        'history': '📋',
        'settings': '⚙️',
        'logout': '🚪',
        'dashboard': '🏠',
        'card': '💳',
        'security': '🔒',
        'notification': '🔔',
        'help': '❓',
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'approved': '✅',
        'rejected': '❌',
        'pending': '⏳',
        'bank': '🏦',
        'money': '💵',
        'chart': '📊',
        'report': '📈',
        'email': '📧',
        'phone': '📞',
        'location': '📍',
        'calendar': '📅',
        'clock': '🕐',
        'search': '🔍',
        'filter': '🔽',
        'export': '📤',
        'print': '🖨️',
        'edit': '✏️',
        'delete': '🗑️',
        'add': '➕',
        'subtract': '➖',
        'star': '⭐',
        'shield': '🛡️',
        'key': '🔑',
    }
    
    @staticmethod
    def get_icon(name):
        """Get icon by name."""
        return IconManager.ICONS.get(name, '•')

class AnimationUtils:
    """Utility class for animations and transitions."""
    
    @staticmethod
    def fade_in(widget, duration=500):
        """Fade in animation for widgets."""
        widget.attributes('-alpha', 0)
        widget.after(10, lambda: AnimationUtils._fade_step(widget, 0, 1, duration, 10))
    
    @staticmethod
    def _fade_step(widget, current, target, duration, steps):
        """Internal fade animation step."""
        step_size = (target - current) / (duration / steps)
        new_alpha = current + step_size
        
        if abs(new_alpha - target) < 0.01:
            widget.attributes('-alpha', target)
        else:
            widget.attributes('-alpha', new_alpha)
            widget.after(steps, lambda: AnimationUtils._fade_step(widget, new_alpha, target, duration, steps))
    
    @staticmethod
    def slide_in(widget, direction='left', duration=300):
        """Slide in animation for widgets."""
        if direction == 'left':
            widget.place(x=-widget.winfo_width(), y=0)
            AnimationUtils._slide_step(widget, -widget.winfo_width(), 0, duration, 10)
    
    @staticmethod
    def _slide_step(widget, current, target, duration, steps):
        """Internal slide animation step."""
        step_size = (target - current) / (duration / steps)
        new_x = current + step_size
        
        if abs(new_x - target) < 1:
            widget.place(x=target)
        else:
            widget.place(x=new_x)
            widget.after(steps, lambda: AnimationUtils._slide_step(widget, new_x, target, duration, steps))

class CardWidget:
    """Custom card widget for displaying information."""
    
    def __init__(self, parent, title, value, icon=None, color=None):
        self.parent = parent
        self.title = title
        self.value = value
        self.icon = icon or '•'
        self.color = color or BankTheme.COLORS['primary']
        
        self.frame = tk.Frame(parent, bg=BankTheme.COLORS['card_bg'], relief='flat', bd=0)
        self._create_card()
    
    def _create_card(self):
        """Create the card layout."""
        # Card shadow effect
        shadow_frame = tk.Frame(self.parent, bg=BankTheme.COLORS['border'], height=2)
        shadow_frame.place(in_=self.frame, x=2, y=2, relwidth=1, relheight=1)
        
        # Main card content
        self.frame.configure(relief='flat', bd=1, highlightbackground=BankTheme.COLORS['border'])
        
        # Header with icon and title
        header_frame = tk.Frame(self.frame, bg=BankTheme.COLORS['card_bg'])
        header_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        # Icon
        icon_label = tk.Label(
            header_frame,
            text=self.icon,
            font=('Segoe UI', 16),
            bg=BankTheme.COLORS['card_bg'],
            fg=self.color
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text=self.title,
            font=BankTheme.FONTS['card_title'],
            bg=BankTheme.COLORS['card_bg'],
            fg=BankTheme.COLORS['text_secondary']
        )
        title_label.pack(side=tk.LEFT)
        
        # Value
        value_label = tk.Label(
            self.frame,
            text=str(self.value),
            font=BankTheme.FONTS['card_value'],
            bg=BankTheme.COLORS['card_bg'],
            fg=self.color
        )
        value_label.pack(padx=15, pady=(0, 15), anchor=tk.W)
        
        # Hover effect
        self._add_hover_effect()
    
    def _add_hover_effect(self):
        """Add hover effect to card."""
        def on_enter(event):
            self.frame.configure(bg=BankTheme.COLORS['hover_light'])
            for child in self.frame.winfo_children():
                if isinstance(child, tk.Frame):
                    child.configure(bg=BankTheme.COLORS['hover_light'])
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, tk.Label):
                            grandchild.configure(bg=BankTheme.COLORS['hover_light'])
                elif isinstance(child, tk.Label):
                    child.configure(bg=BankTheme.COLORS['hover_light'])
        
        def on_leave(event):
            self.frame.configure(bg=BankTheme.COLORS['card_bg'])
            for child in self.frame.winfo_children():
                if isinstance(child, tk.Frame):
                    child.configure(bg=BankTheme.COLORS['card_bg'])
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, tk.Label):
                            grandchild.configure(bg=BankTheme.COLORS['card_bg'])
                elif isinstance(child, tk.Label):
                    child.configure(bg=BankTheme.COLORS['card_bg'])
        
        self.frame.bind("<Enter>", on_enter)
        self.frame.bind("<Leave>", on_leave)
    
    def pack(self, **kwargs):
        """Pack the card frame."""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the card frame."""
        self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the card frame."""
        self.frame.place(**kwargs)

class StatCard(CardWidget):
    """Specialized card for displaying statistics."""
    
    def __init__(self, parent, title, value, icon=None, color=None, change=None):
        self.change = change
        super().__init__(parent, title, value, icon, color)
    
    def _create_card(self):
        """Create the stat card layout."""
        super()._create_card()
        
        # Add change indicator if provided
        if self.change is not None:
            change_color = BankTheme.COLORS['success'] if self.change >= 0 else BankTheme.COLORS['accent']
            change_symbol = '↑' if self.change >= 0 else '↓'
            
            change_label = tk.Label(
                self.frame,
                text=f"{change_symbol} {abs(self.change)}%",
                font=BankTheme.FONTS['small'],
                bg=BankTheme.COLORS['card_bg'],
                fg=change_color
            )
            change_label.pack(padx=15, pady=(0, 10), anchor=tk.W)

class ModernButton:
    """Modern button with enhanced styling."""
    
    def __init__(self, parent, text, command=None, style='primary', icon=None, width=None):
        self.parent = parent
        self.text = text
        self.command = command
        self.style = style
        self.icon = icon or ''
        self.width = width
        
        self.button = self._create_button()
    
    def _create_button(self):
        """Create the modern button."""
        # Button colors based on style
        style_colors = {
            'primary': (BankTheme.COLORS['primary'], BankTheme.COLORS['primary_light']),
            'secondary': (BankTheme.COLORS['secondary'], BankTheme.COLORS['secondary_light']),
            'success': (BankTheme.COLORS['success'], '#2ECC71'),
            'danger': (BankTheme.COLORS['accent'], '#EC7063'),
            'outline': (BankTheme.COLORS['card_bg'], BankTheme.COLORS['hover_light'])
        }
        
        bg_color, hover_color = style_colors.get(self.style, style_colors['primary'])
        text_color = BankTheme.COLORS['text_white'] if self.style != 'outline' else BankTheme.COLORS['text_primary']
        
        button_text = f"{self.icon} {self.text}".strip()
        
        button = tk.Button(
            self.parent,
            text=button_text,
            command=self.command,
            bg=bg_color,
            fg=text_color,
            font=BankTheme.FONTS['button'],
            relief='flat',
            bd=0,
            cursor='hand2',
            width=self.width
        )
        
        # Add hover effect
        def on_enter(event):
            button.configure(bg=hover_color)
        
        def on_leave(event):
            button.configure(bg=bg_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    def pack(self, **kwargs):
        """Pack the button."""
        self.button.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the button."""
        self.button.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the button."""
        self.button.place(**kwargs)

class GradientFrame:
    """Frame with gradient background effect."""
    
    def __init__(self, parent, width, height, color1, color2):
        self.parent = parent
        self.width = width
        self.height = height
        self.color1 = color1
        self.color2 = color2
        
        self.canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
        self._create_gradient()
    
    def _create_gradient(self):
        """Create gradient background."""
        # Simple gradient simulation using rectangles
        for i in range(self.height):
            ratio = i / self.height
            # Simple color interpolation
            r1, g1, b1 = self._hex_to_rgb(self.color1)
            r2, g2, b2 = self._hex_to_rgb(self.color2)
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, self.width, i, fill=color, width=1)
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def pack(self, **kwargs):
        """Pack the canvas."""
        self.canvas.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the canvas."""
        self.canvas.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the canvas."""
        self.canvas.place(**kwargs)
