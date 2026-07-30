import tkinter as tk

from managers.thememanager import ThemeManager


class GlassCard:

    def __init__(self, parent):

        self.theme = ThemeManager()

        self.frame = tk.Frame(
            parent,
            bg="#171717",
            bd=0
        )


        self.accent = tk.Frame(
            self.frame,
            bg=self.theme.get("accent"),
            width=4
        )

        self.accent.pack(
            side="left",
            fill="y"
        )


        self.surface = tk.Frame(
            self.frame,
            bg=self.theme.get("card")
        )

        self.surface.pack(
            side="right",
            fill="both",
            expand=True,
            padx=2,
            pady=2
        )


        self.content = tk.Frame(
            self.surface,
            bg=self.theme.get("card")
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )