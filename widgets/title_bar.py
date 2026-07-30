import tkinter as tk

from managers.thememanager import ThemeManager

class TitleBar:

    def __init__(self, parent, window):

        self.window = window

        self.theme=ThemeManager()

        self.frame = tk.Frame(
            parent,
            height=40,
            bg=self.theme.get("background")
        )

        self.frame.pack(
            fill="x",
            side="top"
        )


        self.drag_area = tk.Frame(
            self.frame,
            bg=self.theme.get("background")
        )

        self.drag_area.pack(
            side="left",
            fill="both",
            expand=True
        )


        self.drag_area.bind(
            "<ButtonPress-1>",
            self.start_move
        )

        self.drag_area.bind(
            "<B1-Motion>",
            self.move_window
        )


        self.x = 0
        self.y = 0


    def start_move(self, event):

        self.x = event.x
        self.y = event.y


    def move_window(self, event):

        x = self.window.winfo_x() + event.x - self.x
        y = self.window.winfo_y() + event.y - self.y

        self.window.geometry(
            f"+{x}+{y}"
        )