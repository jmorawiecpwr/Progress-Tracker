import ttkbootstrap as ttkb
import tkinter as tk
from tkinter import ttk

class AppearanceSettings:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.master, text="Select theme:").grid(row=0, column=0, padx=10, pady=10)

        self.themes = self.app.style.theme_names()
        self.theme_combobox = ttk.Combobox(self.master, values=self.themes)
        self.theme_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.theme_combobox.set(self.app.style.theme_use())  # Set current theme
        ttk.Button(self.master, text="Apply", command=self.apply_theme).grid(row=0, column=2, padx=10, pady=10)

    def apply_theme(self):
        selected_theme = self.theme_combobox.get()
        self.app.style.theme_use(selected_theme)
        self.app.save_settings(selected_theme)
