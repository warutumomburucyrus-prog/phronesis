import tkinter as tk
import socket
from datetime import datetime
from PIL import Image, ImageTk
from managers.thememanager import ThemeManager

class StatusBar:

    def __init__(self, parent):

        self.theme = ThemeManager()

        self.frame = tk.Frame(
            parent,
            height=35,
            bg=self.theme.get("sidebar")
        )

        self.frame.grid_propagate(False)

        self.icons = {}

        self.left = tk.Frame(
            self.frame,
            bg=self.theme.get("sidebar")
        )

        self.left.pack(
            side="left",
            padx=15
        )


        self.create_status_item(
            self.left,
            "internet",
            "assets/icons/internet.png",
            "Checking..."
        )

        self.create_status_item(
            self.left,
            "ai",
            "assets/icons/ai2.png",
            "Ready"
        )

        self.create_status_item(
            self.left,
            "streak",
            "assets/icons/streak.png",
            "0 Days"
        )

        self.right = tk.Frame(
            self.frame,
            bg=self.theme.get("sidebar")
        )

        self.right.pack(
            side="right",
            padx=15
        )

        self.version = tk.Label(
            self.right,
            text="Phronesis v1.0",
            bg=self.theme.get("sidebar"),
            fg=self.theme.get("secondary_text"),
            font=("Segoe UI",10)
        )

        self.version.pack(
            side="right"
        )


        self.create_status_item(
            self.right,
            "clock",
            "assets/icons/clock.png",
            ""
        )



        self.update_clock()

        self.check_internet()


    def create_status_item(
        self,
        parent,
        name,
        icon_path,
        text
    ):


        container = tk.Frame(
            parent,
            bg=self.theme.get("sidebar")
        )

        container.pack(
            side="left",
            padx=10
        )


        icon = self.load_icon(
            icon_path
        )


        self.icons[name] = icon


        image_label = tk.Label(
            container,
            image=icon,
            bg=self.theme.get("sidebar")
        )

        image_label.pack(
            side="left"
        )


        label = tk.Label(
            container,
            text=text,
            bg=self.theme.get("sidebar"),
            fg=self.theme.get("text"),
            font=("Segoe UI",10)
        )

        label.pack(
            side="left",
            padx=5
        )


        setattr(
            self,
            name + "_label",
            label
        )


    def load_icon(self, path):

        image = Image.open(
            path
        ).convert(
            "RGBA"
        )


        image = image.resize(
            (18,18),
            Image.LANCZOS
        )


        return ImageTk.PhotoImage(
            image
        )


    def update_clock(self):

        current = datetime.now().strftime(
            "%I:%M %p"
        )


        self.clock_label.config(
            text=current
        )


        self.frame.after(
            1000,
            self.update_clock
        )

    def check_internet(self):

        try:

            socket.create_connection(
                ("8.8.8.8",53),
                timeout=2
            )


            self.internet_label.config(
                text="Connected"
            )


        except OSError:

            self.internet_label.config(
                text="Offline"
            )


        self.frame.after(
            5000,
            self.check_internet
        )