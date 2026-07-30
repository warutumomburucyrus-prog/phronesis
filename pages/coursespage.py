import tkinter as tk
from tkinter import messagebox

from widgets.addcourse import AddCourseDialog
from widgets.coursecard import CourseCard

from managers.coursemanager import CourseManager
from managers.thememanager import ThemeManager



class CoursesPage:

    def __init__(self, parent):

        self.theme = ThemeManager()

        self.frame = tk.Frame(
            parent,
            bg=self.theme.get("background")
        )


        self.manager = CourseManager()



        title = tk.Label(
            self.frame,
            text="Courses",
            font=("Telma", 28),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        )

        title.pack(
            pady=20
        )



        add_button = tk.Button(
            self.frame,
            text="+ Add Course",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.open_add_course
        )

        add_button.pack(
            pady=10
        )



        container = tk.Frame(
            self.frame,
            bg=self.theme.get("background")
        )

        container.pack(
            expand=True,
            fill="both",
            padx=30,
            pady=20
        )


        self.canvas = tk.Canvas(
            container,
            bg=self.theme.get("background"),
            highlightthickness=0
        )

        self.scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )


        self.course_area = tk.Frame(
            self.canvas,
            bg=self.theme.get("background")
        )

        for column in range(4):
            self.course_area.grid_columnconfigure(
                column,
                weight=1
            )

        self.course_area.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )


        self.canvas_window = self.canvas.create_window(
            (0,0),
            window=self.course_area,
            anchor="nw"
        )


        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(
                self.canvas_window,
                width=e.width
            )
        )


        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )


        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.bind(
            "<Enter>",
            lambda e: self.canvas.bind_all(
                "<MouseWheel>",
                self._on_mousewheel
            )
        )

        self.canvas.bind(
            "<Leave>",
            lambda e: self.canvas.unbind_all(
                "<MouseWheel>"
            )
        )

        self.load_courses()



    def open_add_course(self):

        AddCourseDialog(
            self.frame,
            self.add_course
        )



    def add_course(
        self,
        course
    ):

        self.manager.add_course(

            course["course_code"],

            course["name"],

            course["lecturer"],

            course["credits"],

            course["exam_date"],

        )


        self.load_courses()


    def delete_course(
        self,
        course_code
    ):

        confirm = messagebox.askyesno(
            "Delete Course",
            f"Are you sure you want to delete {course_code}?"
        )


        if confirm:

            self.manager.delete_course(
                course_code
            )


            self.load_courses()



    def load_courses(self):


        for widget in self.course_area.winfo_children():

            widget.destroy()



        courses = self.manager.get_courses()



        if not courses:

            empty = tk.Label(
                self.course_area,
                text="No courses added yet",
                font=("Segoe UI",14),
                bg=self.theme.get("background"),
                fg=self.theme.get("secondary_text")
            )

            empty.pack(
                pady=30
            )

            return



        for course in courses:


            card = CourseCard(

                self.course_area,

                course,

                self.edit_course,

                self.delete_course

            )


            index = courses.index(course)

            card.frame.grid(
                row=index // 4,
                column=index % 4,
                padx=10,
                pady=10,
                sticky="nsew"
            )
    
    def edit_course(self, course):

        from widgets.editcourses import EditCourseDialog


        EditCourseDialog(

            self.frame,

            course,

            self.update_course

        )
    def update_course(
        self,
        old_name,
        updated_course
    ):

        self.manager.update_course(

            old_name,

            updated_course

        )


        self.load_courses()

    def _on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )