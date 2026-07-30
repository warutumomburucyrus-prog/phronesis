import tkinter as tk

from managers.thememanager import ThemeManager

class CourseCard:

    def __init__(
        self,
        parent,
        course,
        edit_callback,
        delete_callback
    ):
        self.theme = ThemeManager()

        self.course = course


        self.edit_callback = edit_callback

        self.delete_callback = delete_callback



        self.frame = tk.Frame(
            parent,
            bg=self.theme.get("button"),
            width=250,
            height=220
        )

        self.frame.grid_propagate(False)


        name = tk.Label(
            self.frame,
            text=f"📘 {course['name']}",
            font=("Segoe UI",16),
            bg=self.theme.get("button"),
            fg=self.theme.get("text")
        )

        name.pack(
            anchor="w"
        )


        info = tk.Label(
            self.frame,
            text=(
                f"Lecturer: {course['lecturer']}\n"
                f"Credits: {course['credits']}\n"
                f"Exam: {course['exam_date']}"
            ),
            bg=self.theme.get("button"),
            fg=self.theme.get("secondary_text")
        )

        info.pack(
            anchor="w",
            pady=10
        )



        buttons = tk.Frame(
            self.frame,
            bg=self.theme.get("button")
        )

        buttons.pack(
            anchor="e"
        )



        edit_button = tk.Button(
            buttons,
            text="Edit",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.edit
        )

        edit_button.pack(
            side="left",
            padx=5
        )



        delete_button = tk.Button(
            buttons,
            text="Delete",
            bg="#8B0000",
            fg=self.theme.get("text"),
            relief="flat",
            command=self.delete
        )

        delete_button.pack(
            side="left"
        )



    def edit(self):

        self.edit_callback(
            self.course
        )



    def delete(self):

        self.delete_callback(
            self.course["course_code"]
        )