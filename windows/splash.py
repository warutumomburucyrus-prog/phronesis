import tkinter as tk

from managers.thememanager import ThemeManager

class SplashScreen:

    def __init__(self, root):

        self.root = root

        self.theme = ThemeManager()

        self.splash = tk.Toplevel(root)
        self.splash.overrideredirect(True)
        self.splash.configure(bg="#171717")

        width = 650
        height = 380

        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.splash.geometry(f"{width}x{height}+{x}+{y}")

        # ==========================
        # Main Container
        # ==========================

        container = tk.Frame(
            self.splash,
            bg="#171717"
        )

        container.pack(
            expand=True,
            fill="both"
        )

        # ==========================
        # Logo
        # ==========================

        tk.Label(
            container,
            text="🧠",
            font=("Segoe UI Emoji", 52),
            bg="#171717",
            fg=self.theme.get("text")
        ).pack(
            pady=(45, 10)
        )

        tk.Label(
            container,
            text="PHRONESIS",
            font=("Segoe UI", 28, "bold"),
            bg="#171717",
            fg=self.theme.get("text")
        ).pack()

        tk.Label(
            container,
            text="AI Academic Companion",
            font=("Segoe UI", 11),
            bg="#171717",
            fg="#A0A0A0"
        ).pack(
            pady=(0, 35)
        )

        # ==========================
        # Progress Bar
        # ==========================

        self.progress_bg = tk.Frame(
            container,
            bg="#303030",
            height=6
        )

        self.progress_bg.pack(
            fill="x",
            padx=70
        )

        self.progress_bg.pack_propagate(False)

        self.progress_fill = tk.Frame(
            self.progress_bg,
            bg="#4CAF50",
            width=0
        )

        self.progress_fill.pack(
            side="left",
            fill="y"
        )

        # ==========================
        # Status
        # ==========================

        self.status_label = tk.Label(
            container,
            text="Starting...",
            font=("Segoe UI", 10),
            bg="#171717",
            fg=self.theme.get("secondary_text")
        )

        self.status_label.pack(
            pady=18
        )

        self.progress = 0

        self.splash.update()

    # ====================================

    def set_status(self, text):

        self.status_label.config(text=text)
        self.splash.update()

    # ====================================

    def step(self, amount=20):

        self.progress += amount

        if self.progress > 100:
            self.progress = 100

        total_width = 650 - 140

        width = int(total_width * (self.progress / 100))

        self.progress_fill.config(width=width)

        self.splash.update()

    # ====================================

    def close(self):

        self.splash.destroy()

        self.root.deiconify()

        self.root.lift()

        self.root.focus_force()