import tkinter as tk

from widgets.datepicker import DatePicker
from managers.thememanager import ThemeManager

class EditCourseDialog:


    def __init__(
        self,
        parent,
        course,
        save_callback
    ):

        self.theme = ThemeManager()

        self.window = tk.Toplevel(parent)

        self.window.title("Edit Course")

        self.window.geometry(
            "400x450"
        )

        self.window.configure(
            bg=self.theme.get("background")
        )

        self.course = course

        self.save_callback = save_callback

        title = tk.Label(
            self.window,
            text="Edit Course",
            font=("Telma", 24),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        )

        title.pack(
            pady=20
        )

        # ==========================================================
        # NAME
        # ==========================================================

        tk.Label(
            self.window,
            text="Course Name",
            bg=self.theme.get("background"),
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

        self.name_entry.insert(
            0,
            course.get("name", "")
        )

        # ==========================================================
        # LECTURER
        # ==========================================================

        tk.Label(
            self.window,
            text="Lecturer",
            bg=self.theme.get("background"),
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

        self.lecturer_entry.insert(
            0,
            course.get("lecturer", "")
        )

        # ==========================================================
        # CREDITS
        # ==========================================================

        tk.Label(
            self.window,
            text="Credits",
            bg=self.theme.get("background"),
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

        self.credits_entry.insert(
            0,
            course.get("credits", "")
        )

        # ==========================================================
        # EXAM DATE
        # ==========================================================

        tk.Label(
            self.window,
            text="Exam Date",
            bg=self.theme.get("background"),
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

        self.date_entry.pack(
            pady=5
        )

        pick_button = tk.Button(
            self.window,
            text="Pick Date",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.open_date_picker
        )

        pick_button.pack(
            pady=5
        )

        self.date_value.set(
            course.get("exam_date", "")
        )

        # ==========================================================
        # SAVE
        # ==========================================================

        save_button = tk.Button(
            self.window,
            text="Save Changes",
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

        updated_course = {

            "name": self.name_entry.get(),

            "lecturer": self.lecturer_entry.get(),

            "credits": self.credits_entry.get(),

            "exam_date": self.date_entry.get()

        }

        self.save_callback(
            self.course["name"],
            updated_course
        )

        self.window.destroy()

    def open_date_picker(self):

        DatePicker(
            self.window,
            self.set_date
        )

    def set_date(self, value):

        self.date_value.set(value)
