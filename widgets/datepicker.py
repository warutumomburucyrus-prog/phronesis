import tkinter as tk
import calendar
from datetime import date
from managers.thememanager import ThemeManager


class DatePicker:

    def __init__(self, parent, callback):

        self.theme= ThemeManager()

        self.callback = callback

        self.window = tk.Toplevel(parent)

        self.window.title("Select Date")
        self.window.geometry("300x300")

        self.window.configure(
            bg=self.theme.get("background")
        )

        self.current_date = date.today()

        self.create_ui()


    def create_ui(self):

        self.header = tk.Frame(
            self.window,
            bg=self.theme.get("background")
        )

        self.header.pack(
            pady=10
        )


        self.month_label = tk.Label(
            self.header,
            font=("Segoe UI",14,"bold"),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        )

        self.month_label.pack(
            side="left",
            padx=20
        )


        tk.Button(
            self.header,
            text="<",
            command=self.previous_month
        ).pack(
            side="left"
        )


        tk.Button(
            self.header,
            text=">",
            command=self.next_month
        ).pack(
            side="right"
        )


        self.days_frame = tk.Frame(
            self.window,
            bg=self.theme.get("background")
        )

        self.days_frame.pack()


        self.draw_calendar()


    def draw_calendar(self):

        for widget in self.days_frame.winfo_children():
            widget.destroy()


        year = self.current_date.year
        month = self.current_date.month


        self.month_label.config(
            text=f"{calendar.month_name[month]} {year}"
        )


        for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:

            tk.Label(
                self.days_frame,
                text=day,
                bg=self.theme.get("background"),
                fg=self.theme.get("text"),
                width=4
            ).grid(
                row=0,
                column=["Mo","Tu","We","Th","Fr","Sa","Su"].index(day)
            )


        cal = calendar.monthcalendar(
            year,
            month
        )


        for r, week in enumerate(cal, start=1):

            for c, day in enumerate(week):

                if day != 0:

                    tk.Button(
                        self.days_frame,
                        text=str(day),
                        width=4,
                        command=lambda d=day:self.select_day(d)
                    ).grid(
                        row=r,
                        column=c
                    )


    def previous_month(self):

        if self.current_date.month == 1:

            self.current_date = self.current_date.replace(
                year=self.current_date.year-1,
                month=12
            )

        else:

            self.current_date = self.current_date.replace(
                month=self.current_date.month-1
            )


        self.draw_calendar()



    def next_month(self):

        if self.current_date.month == 12:

            self.current_date = self.current_date.replace(
                year=self.current_date.year+1,
                month=1
            )

        else:

            self.current_date = self.current_date.replace(
                month=self.current_date.month+1
            )


        self.draw_calendar()



    def select_day(self, day):

        selected = self.current_date.replace(
            day=day
        )


        self.callback(
            selected.strftime("%d/%m/%Y")
        )


        self.window.destroy()