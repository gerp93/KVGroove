"""
KVGroove Login Dialog
Password entry dialog for app protection
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from core.auth import Auth


class LoginDialog:
    """Login/password dialog"""
    
    def __init__(self, parent: Optional[tk.Tk] = None):
        self.auth = Auth()
        self.authenticated = False
        
        # Create dialog window
        if parent:
            self.dialog = tk.Toplevel(parent)
        else:
            self.dialog = tk.Tk()
        
        self.dialog.title("KVGroove")
        self.dialog.geometry("350x200")
        self.dialog.resizable(False, False)
        
        # Center on screen
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() - 350) // 2
        y = (self.dialog.winfo_screenheight() - 200) // 2
        self.dialog.geometry(f"350x200+{x}+{y}")
        
        # Make modal
        self.dialog.transient(parent) if parent else None
        self.dialog.grab_set()
        
        # Handle close button
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)
        
        self._create_widgets()
        
        # Focus password field
        self.password_entry.focus_set()
    
    def _create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # App title
        title_label = ttk.Label(main_frame, text="🎵 KVGroove", 
                                font=('Segoe UI', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        if self.auth.is_password_set():
            # Login mode
            prompt_text = "Enter password to continue:"
        else:
            # First-time setup
            prompt_text = "Set a password to protect KVGroove:"
        
        prompt_label = ttk.Label(main_frame, text=prompt_text,
                                 font=('Segoe UI', 10))
        prompt_label.pack(anchor=tk.W)
        
        # Password entry
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var,
                                        show="●", font=('Segoe UI', 11), width=30)
        self.password_entry.pack(fill=tk.X, pady=(5, 5))
        self.password_entry.bind('<Return>', lambda e: self._on_submit())
        
        # Confirm password (only for first-time setup)
        if not self.auth.is_password_set():
            confirm_label = ttk.Label(main_frame, text="Confirm password:",
                                      font=('Segoe UI', 10))
            confirm_label.pack(anchor=tk.W, pady=(10, 0))
            
            self.confirm_var = tk.StringVar()
            self.confirm_entry = ttk.Entry(main_frame, textvariable=self.confirm_var,
                                           show="●", font=('Segoe UI', 11), width=30)
            self.confirm_entry.pack(fill=tk.X, pady=(5, 5))
            self.confirm_entry.bind('<Return>', lambda e: self._on_submit())
        else:
            self.confirm_var = None
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        if self.auth.is_password_set():
            submit_text = "Unlock"
        else:
            submit_text = "Set Password"
        
        submit_btn = tk.Button(btn_frame, text=submit_text, width=12,
                               command=self._on_submit)
        submit_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        cancel_btn = tk.Button(btn_frame, text="Exit", width=10,
                               command=self._on_cancel)
        cancel_btn.pack(side=tk.RIGHT)
        
        # Skip button (only for first-time)
        if not self.auth.is_password_set():
            skip_btn = tk.Button(btn_frame, text="Skip", width=10,
                                 command=self._on_skip)
            skip_btn.pack(side=tk.LEFT)
    
    def _on_submit(self):
        """Handle submit button"""
        password = self.password_var.get()
        
        if not password:
            messagebox.showwarning("Password Required", 
                                   "Please enter a password.",
                                   parent=self.dialog)
            return
        
        if self.auth.is_password_set():
            # Verify password
            if self.auth.verify_password(password):
                self.authenticated = True
                self.dialog.destroy()
            else:
                messagebox.showerror("Incorrect Password",
                                     "The password you entered is incorrect.",
                                     parent=self.dialog)
                self.password_var.set("")
                self.password_entry.focus_set()
        else:
            # Set new password
            confirm = self.confirm_var.get() if self.confirm_var else ""
            
            if password != confirm:
                messagebox.showerror("Password Mismatch",
                                     "Passwords do not match.",
                                     parent=self.dialog)
                return
            
            if len(password) < 4:
                messagebox.showwarning("Password Too Short",
                                       "Password must be at least 4 characters.",
                                       parent=self.dialog)
                return
            
            self.auth.set_password(password)
            self.authenticated = True
            messagebox.showinfo("Password Set",
                               "Password has been set successfully!",
                               parent=self.dialog)
            self.dialog.destroy()
    
    def _on_skip(self):
        """Skip password setup"""
        self.authenticated = True
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Cancel and exit"""
        self.authenticated = False
        self.dialog.destroy()
    
    def run(self) -> bool:
        """Run the dialog and return whether authenticated"""
        self.dialog.mainloop()
        return self.authenticated


class PasswordSettingsDialog:
    """Dialog for changing/removing password from settings"""
    
    def __init__(self, parent: tk.Tk):
        self.auth = Auth()
        self.parent = parent
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Password Settings")
        self.dialog.geometry("350x250")
        self.dialog.resizable(False, False)
        
        # Center on parent
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 350) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 250) // 2
        self.dialog.geometry(f"350x250+{x}+{y}")
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(main_frame, text="Password Settings",
                          font=('Segoe UI', 14, 'bold'))
        title.pack(pady=(0, 15))
        
        if self.auth.is_password_set():
            # Current password
            ttk.Label(main_frame, text="Current password:").pack(anchor=tk.W)
            self.current_var = tk.StringVar()
            current_entry = ttk.Entry(main_frame, textvariable=self.current_var,
                                      show="●", width=30)
            current_entry.pack(fill=tk.X, pady=(2, 10))
            current_entry.focus_set()
        else:
            self.current_var = None
        
        # New password
        ttk.Label(main_frame, text="New password (leave blank to remove):").pack(anchor=tk.W)
        self.new_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.new_var,
                  show="●", width=30).pack(fill=tk.X, pady=(2, 5))
        
        # Confirm
        ttk.Label(main_frame, text="Confirm new password:").pack(anchor=tk.W)
        self.confirm_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.confirm_var,
                  show="●", width=30).pack(fill=tk.X, pady=(2, 15))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="Save", width=10,
                  command=self._on_save).pack(side=tk.RIGHT, padx=(5, 0))
        tk.Button(btn_frame, text="Cancel", width=10,
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
    
    def _on_save(self):
        """Save password changes"""
        # Verify current password if set
        if self.current_var:
            if not self.auth.verify_password(self.current_var.get()):
                messagebox.showerror("Incorrect Password",
                                     "Current password is incorrect.",
                                     parent=self.dialog)
                return
        
        new_password = self.new_var.get()
        confirm = self.confirm_var.get()
        
        if not new_password:
            # Remove password
            self.auth.remove_password()
            messagebox.showinfo("Password Removed",
                               "Password protection has been removed.",
                               parent=self.dialog)
            self.dialog.destroy()
            return
        
        if new_password != confirm:
            messagebox.showerror("Password Mismatch",
                                 "Passwords do not match.",
                                 parent=self.dialog)
            return
        
        if len(new_password) < 4:
            messagebox.showwarning("Password Too Short",
                                   "Password must be at least 4 characters.",
                                   parent=self.dialog)
            return
        
        self.auth.set_password(new_password)
        messagebox.showinfo("Password Updated",
                           "Password has been updated successfully!",
                           parent=self.dialog)
        self.dialog.destroy()
