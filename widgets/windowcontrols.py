import tkinter as tk
from PIL import Image, ImageTk

from managers.thememanager import ThemeManager


class WindowControls:

    def __init__(self, parent, window):

        self.theme = ThemeManager()

        self.window = window

        self.frame = tk.Frame(
            parent,
            bg="#202020"
        )

        self.frame.pack(
            side="right",
            padx=10,
            pady=5
        )


        self.icons = {}


        self.minimize = self.create_button(
            "minimize",
            "assets/icons/minimize.png",
            self.minimize_window
        )


        self.maximize = self.create_button(
            "maximize",
            "assets/icons/maximize.png",
            self.maximize_window
        )


        self.close = self.create_button(
            "close",
            "assets/icons/close.png",
            self.window.destroy
        )


        self.maximized = False



    def create_button(
        self,
        name,
        icon_path,
        command
    ):

        image = Image.open(
            icon_path
        ).convert(
            "RGBA"
        )


        image = image.resize(
            (16,16),
            Image.LANCZOS
        )


        icon = ImageTk.PhotoImage(
            image
        )


        self.icons[name] = icon


        button = tk.Button(
            self.frame,
            image=icon,
            bg=self.theme.get("background"),
            activebackground=self.theme.get("button_hover"),
            bd=0,
            relief="flat",
            command=command,
            cursor="hand2"
        )


        button.image = icon


        button.pack(
            side="left",
            padx=5
        )

        # Hover effects

        if name == "close":

            button.bind(
                "<Enter>",
                lambda e: button.config(
                    bg="#C42B1C"
                )
            )

            button.bind(
                "<Leave>",
                lambda e: button.config(
                    bg=self.theme.get("background")
                )
            )

        else:

            button.bind(
                "<Leave>",
                lambda e: button.config(
                    bg=self.theme.get("background")
                )
            )

        return button



    def minimize_window(self):

        self.window.iconify()



    def maximize_window(self):

        if self.maximized:

            self.window.state(
                "normal"
            )

        else:

            self.window.state(
                "zoomed"
            )


        self.maximized = not self.maximized