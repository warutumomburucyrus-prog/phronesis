import tkinter as tk

from widgets.datepicker import DatePicker


class CourseWizard:


    def __init__(
        self,
        parent,
        courses,
        save_callback,
        finished_callback
    ):

        self.parent = parent

        self.courses = courses

        self.save_callback = save_callback

        self.finished_callback = finished_callback

        self.index = 0


        self.window = tk.Toplevel(parent)

        self.window.title(
            "Complete Courses"
        )

        self.window.geometry(
            "400x450"
        )

        self.window.configure(
            bg="#202020"
        )

        self.window.transient(parent)

        self.window.grab_set()

        self.show_course()



    def show_course(self):

        for widget in self.window.winfo_children():

            widget.destroy()


        if self.index >= len(self.courses):

            self.finished_callback()

            self.window.destroy()

            return



        self.current = self.courses[self.index]


        tk.Label(
            self.window,
            text=f"Course {self.index + 1} of {len(self.courses)}\n\nComplete {self.current['course_code']}",
            font=("Segoe UI",20,"bold"),
            bg="#202020",
            fg=self.theme.get("text")
        ).pack(
            pady=20
        )


        self.name = self.create_field(
            "Course Name"
        )


        self.credits = self.create_field(
            "Credits"
        )


        tk.Label(
            self.window,
            text="Exam Date",
            bg="#202020",
            fg=self.theme.get("text")
        ).pack(
            anchor="w",
            padx=40
        )

        self.exam_value = tk.StringVar()

        self.exam = tk.Entry(
            self.window,
            textvariable=self.exam_value,
            width=35
        )

        self.exam.pack(
            pady=5
        )


        tk.Button(
            self.window,
            text="Pick Date",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            command=self.open_date_picker
        ).pack(
            pady=5
        )


        tk.Button(
            self.window,
            text="Save & Continue",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            command=self.save
        ).pack(
            pady=30
        )



    def create_field(self,text):

        tk.Label(
            self.window,
            text=text,
            bg="#202020",
            fg=self.theme.get("text")
        ).pack(
            anchor="w",
            padx=40
        )


        entry=tk.Entry(
            self.window,
            width=35
        )


        entry.pack(
            pady=5
        )


        return entry

    def create_date_field(self, text):

        tk.Label(
            self.window,
            text=text,
            bg="#202020",
            fg=self.theme.get("text")
        ).pack(
            anchor="w",
            padx=40
        )


        self.exam_value = tk.StringVar()


        entry = tk.Entry(
            self.window,
            width=35,
            textvariable=self.exam_value
        )

        entry.pack(
            pady=5
        )


        tk.Button(
            self.window,
            text="Pick Date",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            command=self.open_date_picker
        ).pack(
            pady=5
        )


        return entry
    

    def save(self):

        updates = {

            "name":self.name.get(),

            "credits":self.credits.get(),

            "exam_date":self.exam_value.get()

        }


        self.save_callback(
            self.current["course_code"],
            updates
        )


        self.index += 1


        self.show_course()

    def open_date_picker(self):

        DatePicker(
            self.window,
            self.set_date
        )


    def set_date(self, value):

        self.exam_value.set(value)