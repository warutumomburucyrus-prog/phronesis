import tkinter as tk

from managers.thememanager import ThemeManager

class ToolTip:

    def __init__(self, widget, text):

        self.widget = widget
        self.text = text
        self.tip = None

        self.theme=ThemeManager()

        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):

        if self.tip is not None:
            return

        self.tip = tk.Toplevel(self.widget)
        self.tip.overrideredirect(True)
        self.tip.configure(bg="#303030")

        label = tk.Label(
            self.tip,
            text=self.text,
            bg=self.theme.get("button"),
            fg=self.theme.get("text"),
            font=("Segoe UI", 10),
            padx=10,
            pady=4
        )

        label.pack()

        self.tip.update_idletasks()

        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 8
        y = self.widget.winfo_rooty() + 5

        self.tip.geometry(f"+{x}+{y}")

    def hide(self, event=None):

        if self.tip:
            self.tip.destroy()
            self.tip = None