import tkinter as tk


from tkinter import ttk
from tkinter import messagebox
from widgets.datepicker import DatePicker
from managers.coursemanager import CourseManager
from managers.thememanager import ThemeManager


class AddAssignmentDialog:

    def __init__(self, parent, save_callback, assignment=None):

        self.theme = ThemeManager()

        self.window = tk.Toplevel(parent)
        self.window.title("Assignment")
        self.window.geometry("400x450")
        self.window.configure(bg=self.theme.get("background"))

        self.save_callback = save_callback
        self.assignment = assignment
        self.course_manager = CourseManager()

        title = tk.Label(
            self.window,
            text="Assignment",
            font=("Segoe UI",20,"bold"),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        )

        title.pack(pady=20)


        self.fields = {}


        tk.Label(
            self.window,
            text="Topic",
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(
            anchor="w",
            padx=40
        )

        all_topics = []

        courses = self.course_manager.get_courses()

        for course in courses:

            for topic in course.get("topics", []):

                all_topics.append(topic)

        self.fields["topic"] = ttk.Combobox(
            self.window,
            values=all_topics,
            state="readonly",
            width=32
        )

        self.fields["topic"].pack(
            padx=40,
            pady=5
        )

        self.fields["topic"].bind(
            "<<ComboboxSelected>>",
            self.select_topic
        )
            
        
        tk.Label(
            self.window,
            text="Course",
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(
            anchor="w",
            padx=40
        )


        courses = self.course_manager.get_courses()

        course_names = [
            f"{course['course_code']} - {course['name']}"
            for course in courses
        ]


        self.fields["course"] = ttk.Combobox(
            self.window,
            values=course_names,
            state="readonly",
            width=32
        )

        self.fields["course"].pack(
            padx=40,
            pady=5
        )

        self.fields["course"].bind(
            "<<ComboboxSelected>>",
            self.load_topics
        )

        tk.Label(
            self.window,
            text="Submission Type",
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(
            anchor="w",
            padx=40
        )


        submission_options = [
            "PDF",
            "Word Document",
            "PowerPoint Presentation",
            "Source Code",
            "GitHub Repository",
            "Printed Copy",
            "Online Portal Upload",
            "Email Submission",
            "Physical Presentation"
        ]


        self.fields["submission"] = ttk.Combobox(
            self.window,
            values=submission_options,
            state="readonly",
            width=32
        )

        self.fields["submission"].pack(
            padx=40,
            pady=5
        )
                        

        tk.Label(
            self.window,
            text="Deadline",
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        ).pack(anchor="w", padx=40)


        self.deadline_value = tk.StringVar()

        self.fields["deadline"] = tk.Entry(
            self.window,
            width=35,
            textvariable=self.deadline_value
        )

        self.fields["deadline"].pack(
            padx=40,
            pady=5
        )


        tk.Button(
            self.window,
            text="Pick Date",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.open_date_picker
        ).pack(
            pady=5
        )


        if assignment:

            for key, entry in self.fields.items():

                entry.insert(
                    0,
                    assignment.get(key,"")
                )



        save = tk.Button(
            self.window,
            text="Save Assignment",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.save
        )

        save.pack(
            pady=25
        )



    def save(self):

        assignment = {}

        for key, entry in self.fields.items():

            assignment[key] = entry.get()


        if not assignment["topic"]:

            messagebox.showwarning(
                "Missing topic",
                "Please select a topic"
            )

            return

        assignment["completed"] = False

        self.save_callback(
            assignment
        )

        self.window.destroy()

    def open_date_picker(self):
        DatePicker(
            self.window,
            self.set_date
        )


    def set_date(self, value):
        self.deadline_value.set(value)

    def load_topics(self, event=None):

        selected = self.fields["course"].get()

        courses = self.course_manager.get_courses()

        for course in courses:

            course_display = (
                f"{course['course_code']} - {course['name']}"
            )

            if course_display == selected:

                self.fields["topic"]["values"] = course.get(
                    "topics",
                    []
                )

                break

    def select_topic(self, event=None):

        selected_topic = self.fields["topic"].get()

        courses = self.course_manager.get_courses()

        for course in courses:

            if selected_topic in course.get("topics", []):

                self.fields["course"].set(
                    f"{course['course_code']} - {course['name']}"
                )

                break