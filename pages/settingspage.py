import tkinter as tk

from managers.thememanager import ThemeManager

class SettingsPage:

    def __init__(self, parent, refresh_callback):

        self.theme = ThemeManager()

        self.refresh_callback = refresh_callback

        self.frame = tk.Frame(
            parent,
            bg=self.theme.get("background")
        )

        tk.Label(
            self.frame,
            text="Settings",
            font=("Segoe UI", 28, "bold"),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(
            pady=40
        )

        theme_label = tk.Label(
            self.frame,
            text="Appearance",
            font=("Segoe UI", 16, "bold"),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        )

        theme_label.pack(
            pady=(20, 10)
        )

        dark_button = tk.Button(
            self.frame,
            text="Dark Mode",
            command=lambda: self.change_theme("dark"),
            bg=self.theme.get("button"),
            fg=self.theme.get("text"),
            bd=0,
            width=20,
            height=2
        )

        dark_button.pack(
            pady=10
        )

        light_button = tk.Button(
            self.frame,
            text="Light Mode",
            command=lambda: self.change_theme("light"),
            bg=self.theme.get("button"),
            fg=self.theme.get("text"),
            bd=0,
            width=20,
            height=2
        )

        light_button.pack(
            pady=10
        )

    def change_theme(self, theme):

        self.theme.set_theme(theme)

        print("Theme changed to:", theme)

        self.refresh_callback()