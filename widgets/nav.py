import tkinter as tk
from PIL import Image, ImageTk

from managers.thememanager import ThemeManager


class NavButton:

    def __init__(
        self,
        parent,
        text,
        command,
        icon=None,
        icon_color =None
    ):
        self.theme = ThemeManager()

        self.frame = tk.Frame(
            parent,
            bg=self.theme.get("sidebar")
        )

        self.frame.pack(
            pady=8
        )
        

        self.icon = None

        if icon_color is None:
            icon_color = self.theme.get("icon")

        if icon:

            image = Image.open(icon).convert(
                "RGBA"
            )

            pixels = image.load()

            for y in range(image.height):
                for x in range(image.width):

                    r, g, b, a = pixels[x, y]

                    if r < 100 and g < 100 and b < 100:

                        pixels[x, y] = (
                            icon_color[0],
                            icon_color[1],
                            icon_color[2],
                            a
                        )



            image = image.resize(
                (32,32),
                Image.LANCZOS
            )

            self.icon = ImageTk.PhotoImage(
                image
            )


        self.button = tk.Button(
            self.frame,
            image=self.icon,
            text=text if not icon else "",
            command=command,
            bg=self.theme.get("sidebar"),
            fg=self.theme.get("text"),
            activebackground=self.theme.get("button_hover"),
            bd=0,
            relief="flat",
            width=45,
            height=45,
            cursor="hand2"
        )


        self.button.image = self.icon


        self.button.pack()

        from widgets.tooltip import ToolTip

        ToolTip(self.button, text)

    def set_selected(self, selected):

        if selected:

            self.button.configure(
                bg=self.theme.get("accent")
            )

        else:

            self.button.configure(
                bg=self.theme.get("sidebar")
            )