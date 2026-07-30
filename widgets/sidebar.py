import tkinter as tk


class sidebar:

    def __init__(self, parent):

        self.parent = parent

        self.frame = tk.Frame(
            parent
        )
        self.frame.pack(
            side="left",
            fill="y"
        )