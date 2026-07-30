import tkinter as tk


class CourseCompletionDialog:


    def __init__(self, parent, course, save_callback):

        self.window = tk.Toplevel(parent)

        self.window.title("Complete Course Information")

        self.window.geometry(
            "400x400"
        )

        self.window.configure(
            bg="#202020"
        )


        self.course = course
        self.save_callback = save_callback


        tk.Label(
            self.window,
            text=course["course_code"],
            font=("Segoe UI",20,"bold"),
            bg="#202020",
            fg=self.theme.get("text")
        ).pack(
            pady=20
        )


        self.name = self.create_entry(
            "Course Name"
        )


        self.credits = self.create_entry(
            "Credits"
        )


        self.exam = self.create_entry(
            "Exam Date"
        )


        tk.Button(
            self.window,
            text="Save",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            command=self.save
        ).pack(
            pady=30
        )



    def create_entry(self,label):

        tk.Label(
            self.window,
            text=label,
            bg="#202020",
            fg=self.theme.get("text")
        ).pack(
            anchor="w",
            padx=40
        )


        entry = tk.Entry(
            self.window,
            width=35
        )


        entry.pack(
            pady=5
        )


        return entry



    def save(self):

        updated = {

            "name": self.name.get(),

            "credits": self.credits.get(),

            "exam_date": self.exam.get()

        }


        self.save_callback(
            self.course["course_code"],
            updated
        )


        self.window.destroy()