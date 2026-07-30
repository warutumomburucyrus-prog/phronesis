import tkinter as tk
import json
import os

from managers.thememanager import ThemeManager


class ProfilePage:

    def __init__(self, parent):

        self.theme = ThemeManager()

        self.frame = tk.Frame(
            parent,
            bg=self.theme.get("background")
        )

        title = tk.Label(
            self.frame,
            text="Profile",
            font=("Segoe UI", 28),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        )

        title.pack(pady=30)

        self.content = tk.Frame(
            self.frame,
            bg=self.theme.get("background")
        )

        self.content.pack(
            fill="both",
            expand=True
        )

        self.refresh()


    def refresh(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        if os.path.exists("Data/user_profile.json"):
            self.show_profile()
        else:
            self.show_create_account()


    def show_create_account(self):

        tk.Label(
            self.content,
            text="No account found.",
            font=("Segoe UI", 18, "bold"),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(pady=(80, 10))

        tk.Label(
            self.content,
            text="Create an account to personalize your Phronesis experience.",
            bg=self.theme.get("background"),
            fg=self.theme.get("secondary_text")
        ).pack()

        tk.Button(
            self.content,
            text="Create Account",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.open_account_setup
        ).pack(pady=30)


    def show_profile(self):

        with open(
            "Data/user_profile.json",
            "r",
            encoding="utf-8"
        ) as file:

            profile = json.load(file)

        name = profile.get("name", "User")

        tk.Label(
            self.content,
            text=f"Hi, {name}! 👋",
            font=("Segoe UI", 22, "bold"),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(pady=(50, 20))

        tk.Label(
            self.content,
            text=f"University: {profile.get('university','')}",
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(anchor="w", padx=50)

        tk.Label(
            self.content,
            text=f"Program: {profile.get('program','')}",
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(anchor="w", padx=50)

        tk.Label(
            self.content,
            text=f"Year: {profile.get('year','')}",
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(anchor="w", padx=50)

        tk.Label(
            self.content,
            text=f"Semester: {profile.get('semester','')}",
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(anchor="w", padx=50)

        tk.Button(
            self.content,
            text="Edit Profile",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.open_account_setup
        ).pack(pady=30)


    def open_account_setup(self):

        print("Open Account Setup Dialog")