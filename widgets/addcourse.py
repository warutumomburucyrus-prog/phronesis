import tkinter as tk

from widgets.datepicker import DatePicker
from managers.thememanager import ThemeManager

class AddCourseDialog:

    def __init__(self, parent, save_callback):

        self.theme=ThemeManager()

        self.window = tk.Toplevel(parent)

        self.window.title("Add Course")
        self.window.geometry("400x450")

        self.window.configure(
            bg="#202020"
        )

        self.save_callback = save_callback


        title = tk.Label(
            self.window,
            text="Add Course",
            font=("Telma", 24),
            bg="#202020",
            fg=self.theme.get("text"))

        title.pack(
            pady=20
        )

        # Course code

        tk.Label(
            self.window,
            text="Course Code",
            bg="#202020",
            fg=self.theme.get("text"),
        ).pack(
            anchor="w",
            padx=40
        )

        self.course_code_entry = tk.Entry(
            self.window,
            width=35
        )

        self.course_code_entry.pack(
            pady=5
        )

        # Course name

        tk.Label(
            self.window,
            text="Course Name",
            bg="#202020",
            fg=self.theme.get("text")
        ).pack(
            anchor="w",
            padx=40
        )


        self.name_entry = tk.Entry(
            self.window,
            width=35
        )

        self.name_entry.pack(
            pady=5
        )


        # Lecturer

        tk.Label(
            self.window,
            text="Lecturer",
            bg="#202020",
            fg=self.theme.get("text")
        ).pack(
            anchor="w",
            padx=40
        )


        self.lecturer_entry = tk.Entry(
            self.window,
            width=35
        )

        self.lecturer_entry.pack(
            pady=5
        )


        # Credits

        tk.Label(
            self.window,
            text="Credits",
            bg="#202020",
            fg=self.theme.get("text")
        ).pack(
            anchor="w",
            padx=40
        )


        self.credits_entry = tk.Entry(
            self.window,
            width=35
        )

        self.credits_entry.pack(
            pady=5
        )


        # Exam date

        tk.Label(
            self.window,
            text="Exam Date (YYYY-MM-DD)",
            bg="#202020",
            fg=self.theme.get("text")
        ).pack(
            anchor="w",
            padx=40
        )


        self.date_value = tk.StringVar()

        self.date_entry = tk.Entry(
            self.window,
            width=35,
            textvariable=self.date_value
        )

        self.date_entry.pack(pady=5)

        tk.Button(
            self.window,
            text="Pick Date",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.open_date_picker
        ).pack(pady=5)

        save_button = tk.Button(
            self.window,
            text="Save Course",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.save
        )

        save_button.pack(
            pady=30,
            ipadx=20
        )


    def save(self):

        course = {

            "course_code": self.course_code_entry.get(),

            "name": self.name_entry.get(),

            "lecturer": self.lecturer_entry.get(),

            "credits": self.credits_entry.get(),

            "exam_date": self.date_entry.get()

        }

        print(course)

        self.save_callback(course)

        self.window.destroy()

    def open_date_picker(self):
        DatePicker(
            self.window,
            self.set_date
        )

    def set_date(self, value):
        self.date_value.set(value)