import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import json
import os
from datetime import date
import matplotlib.pyplot as plt
import ttkbootstrap as ttkb

from profile_management import ProfileManagement
from appearance import AppearanceSettings


class WeightTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Progress Tracker")
        self.style = ttkb.Style('cosmo')

        self.profiles = []
        self.current_profile = None

        self.create_widgets()
        self.load_profiles()
        self.create_menu()

        self.load_settings()

        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def create_widgets(self):
        self.profile_label = ttk.Label(self.root, text="Select profile:")
        self.profile_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.profile_combobox = ttk.Combobox(self.root, values=self.profiles)
        self.profile_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.profile_combobox.bind("<<ComboboxSelected>>", self.load_profile)

        self.new_profile_button = ttk.Button(self.root, text="New profile", command=self.new_profile)
        self.new_profile_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        self.value_label = ttk.Label(self.root, text="Today's value:")
        self.value_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.value_entry = ttk.Entry(self.root)
        self.value_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.bind_enter_key(self.value_entry, self.add_value)

        self.add_value_button = ttk.Button(self.root, text="Add Value", command=self.add_value)
        self.add_value_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        self.historical_date_label = ttk.Label(self.root, text="Historical date:")
        self.historical_date_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.historical_date_entry = ttk.Entry(self.root)
        self.historical_date_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        self.historical_value_label = ttk.Label(self.root, text="Historical value:")
        self.historical_value_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.historical_value_entry = ttk.Entry(self.root)
        self.historical_value_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        self.add_historical_value_button = ttk.Button(self.root, text="Add Historical Value",
                                                      command=self.add_historical_value)
        self.add_historical_value_button.grid(row=5, column=2, padx=10, pady=10, sticky="e")

        self.data_text = tk.Text(self.root, height=10, width=50)
        self.data_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.delete_button = ttk.Button(self.root, text="Delete Entry", command=self.delete_entry)
        self.delete_button.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.plot_button = ttk.Button(self.root, text="Plot Data", command=self.plot_data)
        self.plot_button.grid(row=3, column=2, padx=10, pady=10, sticky="e")

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)

        self.settings_menu.add_command(label="Profile Management", command=self.open_profile_management)
        self.settings_menu.add_command(label="Export as CSV", command=self.export_as_csv)
        self.settings_menu.add_command(label="Appearance", command=self.open_appearance_settings)
        self.settings_menu.add_command(label="Language", command=self.open_language_settings)
        self.settings_menu.add_command(label="Historical Values", command=self.open_historical_values)

    def open_profile_management(self):
        self.profile_management_window = tk.Toplevel(self.root)
        self.profile_management_window.title("Profile Management")
        ProfileManagement(self.profile_management_window, self)

    def open_appearance_settings(self):
        self.appearance_window = tk.Toplevel(self.root)
        self.appearance_window.title("Appearance Settings")
        AppearanceSettings(self.appearance_window, self)

    def open_language_settings(self):
        languages = ['English', 'Deutsch', 'Polski']

        self.language_window = tk.Toplevel(self.root)
        self.language_window.title("Language Settings")

        self.language_label = ttk.Label(self.language_window, text="Select language:")
        self.language_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.language_combobox = ttk.Combobox(self.language_window, values=languages)
        self.language_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.language_confirm_button = ttk.Button(self.language_window, text="Confirm", command=self.confirm_language)
        self.language_confirm_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

    def confirm_language(self):
        selected_language = self.language_combobox.get()
        if selected_language:
            lang_code = selected_language.lower()[:2]
            lang_file = os.path.join("languages", f"language_{lang_code}.json")

            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8') as file:
                    lang_data = json.load(file)

                self.update_ui_with_language(lang_data)
                messagebox.showinfo("Language changed", f"Switched to {selected_language}.")
            else:
                messagebox.showerror("Error", f"Language file for {selected_language} not found.")

            self.language_window.destroy()

    def update_ui_with_language(self, lang_data):
        self.profile_label.config(text=lang_data.get("Select profile:", "Select profile:"))
        self.new_profile_button.config(text=lang_data.get("New profile", "New profile"))
        self.value_label.config(text=lang_data.get("Today's value:", "Today's value:"))
        self.add_value_button.config(text=lang_data.get("Add Value", "Add Value"))
        self.delete_button.config(text=lang_data.get("Delete Entry", "Delete Entry"))
        self.plot_button.config(text=lang_data.get("Plot Data", "Plot Data"))
        self.settings_menu.entryconfigure(0, label=lang_data.get("Profile Management", "Profile Management"))
        self.settings_menu.entryconfigure(1, label=lang_data.get("Export as CSV", "Export as CSV"))
        self.settings_menu.entryconfigure(2, label=lang_data.get("Appearance", "Appearance"))
        self.settings_menu.entryconfigure(3, label=lang_data.get("Language", "Language"))
        self.settings_menu.entryconfigure(4, label=lang_data.get("Historical Values", "Historical Values"))

    def open_historical_values(self):
        self.historical_values_window = tk.Toplevel(self.root)
        self.historical_values_window.title("Historical Values")

        self.historical_values_text = tk.Text(self.historical_values_window, height=10, width=50)
        self.historical_values_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.display_historical_values()

    def display_historical_values(self):
        self.historical_values_text.delete('1.0', tk.END)
        for entry in self.data:
            self.historical_values_text.insert(tk.END, f"{entry['date']}: {entry['value']}\n")

    def export_as_csv(self):
        import csv

        if self.current_profile and self.data:
            file_path = f"{self.current_profile}.csv"
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Value'])
                for entry in self.data:
                    writer.writerow([entry['date'], entry['value']])
            messagebox.showinfo("Exported", f"Profile data exported to {file_path}.")
        else:
            messagebox.showerror("Error", "No profile data to export.")

    def load_profiles(self):
        if not os.path.exists('profiles'):
            os.makedirs('profiles')
        self.profiles = [f.split('.')[0] for f in os.listdir('profiles') if f.endswith('.json')]
        self.profile_combobox['values'] = self.profiles

    def load_profile(self, event=None):
        profile_name = self.profile_combobox.get()
        if profile_name:
            self.current_profile = profile_name
            self.load_data()

    def load_data(self):
        with open(f'profiles/{self.current_profile}.json', 'r') as file:
            self.data = json.load(file)
        self.display_data()

    def display_data(self):
        self.data_text.delete('1.0', tk.END)
        for entry in self.data:
            self.data_text.insert(tk.END, f"{entry['date']}: {entry['value']}\n")

    def new_profile(self):
        profile_name = askstring("New profile", "Enter profile name:")
        if profile_name:
            self.current_profile = profile_name
            self.data = []
            self.save_data()
            self.load_profiles()
            self.profile_combobox.set(profile_name)

    def add_value(self):
        value = self.value_entry.get().replace(',', '.')
        try:
            float(value)
            if value and self.current_profile:
                self.data.append({'date': str(date.today()), 'value': value})
                self.save_data()
                self.display_data()
                self.value_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Please select a profile and/or enter a value.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def add_historical_value(self):
        historical_date = self.historical_date_entry.get()
        historical_value = self.historical_value_entry.get().replace(',', '.')

        try:
            float(historical_value)
            if historical_date and historical_value and self.current_profile:
                self.data.append({'date': historical_date, 'value': historical_value})
                self.save_data()
                self.display_data()
                self.historical_date_entry.delete(0, tk.END)
                self.historical_value_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Please select a profile, enter a historical date and/or a valid value.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for historical value.")

    def delete_entry(self):
        try:
            selected_text = self.data_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            date_to_delete, value_to_delete = selected_text.split(": ")
            date_to_delete = date_to_delete.strip()
            value_to_delete = value_to_delete.strip()

            self.data = [entry for entry in self.data if
                         not (entry['date'] == date_to_delete and entry['value'] == value_to_delete)]
            self.save_data()
            self.display_data()
        except tk.TclError:
            messagebox.showerror("Error", "No entry selected.")

    def delete_current_profile(self):
        if self.current_profile:
            profile_file = f"profiles/{self.current_profile}.json"
            if os.path.exists(profile_file):
                os.remove(profile_file)
                messagebox.showinfo("Profile deleted", f"Profile '{self.current_profile}' has been deleted.")
                self.current_profile = None
                self.load_profiles()
                self.profile_combobox.set('')
                self.data_text.delete('1.0', tk.END)
            else:
                messagebox.showerror("Error", "Profile file not found.")

    def change_profile_name(self):
        new_name = askstring("Change profile name", "Enter new profile name:")
        if new_name:
            old_profile_file = f"profiles/{self.current_profile}.json"
            new_profile_file = f"profiles/{new_name}.json"
            if os.path.exists(old_profile_file):
                os.rename(old_profile_file, new_profile_file)
                messagebox.showinfo("Profile renamed", f"Profile '{self.current_profile}' renamed to '{new_name}'.")
                self.current_profile = new_name
                self.load_profiles()
                self.profile_combobox.set(new_name)
            else:
                messagebox.showerror("Error", "Profile file not found.")

    def save_data(self):
        if self.current_profile:
            with open(f'profiles/{self.current_profile}.json', 'w') as file:
                json.dump(self.data, file)

    def plot_data(self):
        if not self.data:
            messagebox.showerror("Error", "No data to plot.")
            return
        dates = [entry['date'] for entry in self.data]
        values = [float(entry['value']) for entry in self.data]
        plt.plot(dates, values, marker='o')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title(f'Progress for {self.current_profile}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
                self.style.theme_use(settings.get("theme", "cosmo"))
        except FileNotFoundError:
            pass

    def save_settings(self, theme):
        settings = {"theme": theme}
        with open("settings.json", "w") as file:
            json.dump(settings, file)

    def bind_enter_key(self, widget, callback):
        widget.bind("<Return>", lambda event: callback())


if __name__ == "__main__":
    root = ttkb.Window(themename='cosmo')
    app = WeightTrackerApp(root)
    root.resizable(True, True)
    root.mainloop()
