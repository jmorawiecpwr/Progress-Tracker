import tkinter as tk
from tkinter import ttk

class ProfileManagement:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        ttk.Button(self.master, text="Delete current profile", command=self.app.delete_current_profile).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(self.master, text="Add new profile", command=self.app.new_profile).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(self.master, text="Change profile name", command=self.app.change_profile_name).grid(row=2, column=0, padx=10, pady=10)
