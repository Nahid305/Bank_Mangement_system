# ui/navigator.py
import tkinter as tk

class Navigator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
    def show_login(self):
        from ui.login_window import LoginWindow
        LoginWindow(self).show()
        
    def show_register(self):
        from ui.registration import RegistrationWindow
        RegistrationWindow(self).show()
        
    def start(self):
        self.show_login()
        self.root.mainloop()