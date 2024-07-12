# Weight Tracker Application

This project is a Tkinter-based weight tracking application that allows users to manage profiles, track weight entries, add historical data, and visualize progress over time. It includes features for multilingual support and customizable appearance settings.

## Features

- **Profile Management:** Create, delete, and rename profiles.
- **Weight Tracking:** Add daily and historical weight entries.
- **Data Visualization:** Plot weight data over time.
- **Multilingual Support:** Change the application language.
- **Customizable Appearance:** Adjust the application's appearance settings.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/weight-tracker-app.git
    ```
2. Navigate to the project directory:
    ```sh
    cd weight-tracker-app
    ```
3. Install the required dependencies:
    ```sh
    pip install tkinter ttkbootstrap matplotlib
    ```

## Usage

1. Run the main application script:
    ```sh
    python main.py
    ```
2. Use the application to manage profiles, track weight, and visualize progress.

## Code Explanation

- `WeightTrackerApp`: Main class for the application, handling UI creation, event binding, and core functionality.
- `create_widgets()`: Sets up the UI components for the application.
- `create_menu()`: Creates the menu bar with options for settings and profile management.
- `open_profile_management()`, `open_appearance_settings()`, `open_language_settings()`, `open_historical_values()`: Functions to open various settings and management windows.
- `add_value()`, `add_historical_value()`, `delete_entry()`: Functions to manage weight entries.
- `load_profiles()`, `load_profile()`, `load_data()`, `save_data()`, `display_data()`: Functions to handle profile and data loading/saving.
- `plot_data()`: Function to visualize weight data.
- `load_settings()`, `save_settings()`: Functions to manage application settings.

## Example

```python
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import json
import os
from datetime import date
import matplotlib.pyplot as plt
import ttkbootstrap as ttkb

# Additional imports for profile management and appearance settings
from profile_management import ProfileManagement
from appearance import AppearanceSettings

class WeightTrackerApp:
    # Initialization and UI setup
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

    # Function implementations...

if __name__ == "__main__":
    root = ttkb.Window(themename='cosmo')
    app = WeightTrackerApp(root)
    root.resizable(True, True)
    root.mainloop()
