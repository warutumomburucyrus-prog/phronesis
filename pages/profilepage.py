import tkinter as tk
import json
import os

from tkinter import ttk
from managers.thememanager import ThemeManager


class ProfilePage:

    def __init__(self, parent):

        self.theme = ThemeManager()

        self.frame = tk.Frame(
            parent,
            bg=self.theme.get("background")
        )

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
        ).pack(
            pady=(80, 10)
        )

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
            activebackground=self.theme.get("accent"),
            activeforeground=self.theme.get("text"),
            relief="flat",
            bd=0,
            command=self.open_account_setup
        ).pack(
            pady=30
        )


    def show_profile(self):

        try:

            with open(
                "Data/user_profile.json",
                "r",
                encoding="utf-8"
            ) as file:

                profile = json.load(file)

        except Exception as e:

            print("Profile loading error:", e)

            return


        name = profile.get(
            "name",
            "User"
        )

        university = profile.get(
            "university",
            ""
        )

        program = profile.get(
            "program",
            profile.get("programme", "")
        )

        year = profile.get(
            "year",
            ""
        )

        semester = profile.get(
            "semester",
            ""
        )


        tk.Label(
            self.content,
            text=f"Hi, {name}! 👋",
            font=("Segoe UI", 22, "bold"),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(
            pady=(50, 20)
        )


        self.create_profile_row(
            "University",
            university
        )

        self.create_profile_row(
            "Program",
            program
        )

        self.create_profile_row(
            "Year",
            year
        )

        self.create_profile_row(
            "Semester",
            semester
        )


        tk.Button(
            self.content,
            text="Edit Profile",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            activebackground=self.theme.get("accent"),
            activeforeground=self.theme.get("text"),
            relief="flat",
            bd=0,
            command=self.open_account_setup
        ).pack(
            pady=30
        )


    def create_profile_row(self, label, value):

        row = tk.Frame(
            self.content,
            bg=self.theme.get("background")
        )

        row.pack(
            fill="x",
            padx=50,
            pady=6
        )


        tk.Label(
            row,
            text=f"{label}:",
            font=("Segoe UI", 10, "bold"),
            width=15,
            anchor="w",
            bg=self.theme.get("background"),
            fg=self.theme.get("secondary_text")
        ).pack(
            side="left"
        )


        tk.Label(
            row,
            text=value,
            font=("Segoe UI", 11),
            anchor="w",
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(
            side="left"
        )


    def open_account_setup(self):

        profile = {}

        if os.path.exists("Data/user_profile.json"):

            try:

                with open(
                    "Data/user_profile.json",
                    "r",
                    encoding="utf-8"
                ) as file:

                    profile = json.load(file)

            except Exception as e:

                print("Profile loading error:", e)


        window = tk.Toplevel(
            self.frame
        )

        window.title(
            "Edit Profile"
        )

        window.geometry(
            "450x520"
        )

        window.resizable(
            False,
            False
        )

        window.configure(
            bg=self.theme.get("background")
        )

        window.transient(
            self.frame.winfo_toplevel()
        )

        window.grab_set()


        title = tk.Label(
            window,
            text="Edit Profile",
            font=("Segoe UI", 22, "bold"),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        )

        title.pack(
            pady=(25, 20)
        )


        form = tk.Frame(
            window,
            bg=self.theme.get("background")
        )

        form.pack(
            fill="both",
            expand=True,
            padx=40
        )


        self.profile_fields = {}


        self.create_field(
            form,
            "Name",
            "name",
            profile.get("name", "")
        )


        self.create_field(
            form,
            "University",
            "university",
            profile.get("university", "")
        )


        self.create_field(
            form,
            "Program",
            "program",
            profile.get(
                "program",
                profile.get("programme", "")
            )
        )


        self.create_field(
            form,
            "Year",
            "year",
            profile.get("year", "")
        )


        self.create_field(
            form,
            "Semester",
            "semester",
            profile.get("semester", "")
        )


        buttons = tk.Frame(
            window,
            bg=self.theme.get("background")
        )

        buttons.pack(
            pady=25
        )


        tk.Button(
            buttons,
            text="Cancel",
            width=12,
            bg=self.theme.get("button"),
            fg=self.theme.get("text"),
            activebackground=self.theme.get("button_hover"),
            activeforeground=self.theme.get("text"),
            relief="flat",
            bd=0,
            command=window.destroy
        ).pack(
            side="left",
            padx=5
        )


        tk.Button(
            buttons,
            text="Save Profile",
            width=12,
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            activebackground=self.theme.get("accent"),
            activeforeground=self.theme.get("text"),
            relief="flat",
            bd=0,
            command=lambda: self.save_profile(
                window
            )
        ).pack(
            side="left",
            padx=5
        )


    def create_field(
        self,
        parent,
        label,
        key,
        value
    ):

        tk.Label(
            parent,
            text=label,
            bg=self.theme.get("background"),
            fg=self.theme.get("secondary_text"),
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            pady=(8, 3)
        )


        variable = tk.StringVar(
            value=value
        )


        entry = tk.Entry(
            parent,
            textvariable=variable,
            font=("Segoe UI", 11),
            bg=self.theme.get("card"),
            fg=self.theme.get("text"),
            insertbackground=self.theme.get("text"),
            relief="flat",
            bd=0
        )

        entry.pack(
            fill="x",
            ipady=8
        )


        self.profile_fields[key] = variable


    def save_profile(self, window):

        profile = {}


        for key, variable in self.profile_fields.items():

            profile[key] = variable.get().strip()


        os.makedirs(
            "Data",
            exist_ok=True
        )


        try:

            with open(
                "Data/user_profile.json",
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    profile,
                    file,
                    indent=4
                )


            window.destroy()

            self.refresh()


            print("Profile saved successfully.")


        except Exception as e:

            print(
                "Profile save error:",
                e
            )