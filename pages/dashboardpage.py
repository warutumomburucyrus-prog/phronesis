import tkinter as tk

from datetime import datetime
from managers.coursemanager import CourseManager
from managers.schedulemanager import ScheduleManager
from widgets.glasscard import GlassCard
from managers.profilemanager import ProfileManager
from managers.assignmentmanager import AssignmentManager
from managers.airecommendationmanager import AIRecommendationManager
from managers.progressmanager import ProgressManager
from managers.thememanager import ThemeManager

class DashboardPage:

    def __init__(self, parent, navigate=None):

        self.theme = ThemeManager()

        self.frame = tk.Frame(
            parent,
            bg=self.theme.get("background")
        )

        self.course_manager = CourseManager()

        self.schedule_manager = ScheduleManager()

        self.profile_manager = ProfileManager()

        self.assignment_manager = AssignmentManager()

        self.progress_manager = ProgressManager()

        self.ai_manager = AIRecommendationManager(
            self.course_manager,
            self.assignment_manager,
            self.schedule_manager
        )

        recommendation = self.progress_manager.get_recommendation()

        self.navigate = navigate

        hour = datetime.now().hour

        if hour < 12:
            greeting = "Good Morning "

        elif hour < 18:
            greeting = "Good Afternoon "

        else:
            greeting = "Good Evening "



        title = tk.Label(
            self.frame,
            text=f"{greeting} {self.profile_manager.get_name()}",
            font=("Segoe UI", 28, "bold"),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        )

        title.pack(
            anchor="w",
            padx=35,
            pady=(25, 5)
        )



        subtitle = tk.Label(
            self.frame,
            text="Welcome",
            font=("Segoe UI", 13),
            bg=self.theme.get("background"),
            fg=self.theme.get("secondary_text")
        )

        subtitle.pack(
            anchor="w",
            padx=35,
            pady=(0, 25)
        )


        self.cards = tk.Frame(
            self.frame,
            bg=self.theme.get("background")
        )

        self.cards.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=25
        )


        self.cards.grid_columnconfigure(
            0,
            weight=1,
            uniform="card"
        )

        self.cards.grid_columnconfigure(
            1,
            weight=1,
            uniform="card"
        )

        self.cards.grid_rowconfigure(
            0,
            weight=1,
            uniform="card"
        )

        self.cards.grid_rowconfigure(
            1,
            weight=1,
            uniform="card"
        )

        today_classes =  self.get_active_today_classes()

        self.frame.after(30000, self.auto_refresh_classes)

        self.make_schedule_card(
            self.cards,
            0,
            0,
            today_classes
        )

        self.make_assignment_card(
            self.cards,
            0,
            1
        )



        self.make_progress_card(
            self.cards,
            1,
            0
        )



        title, body = self.ai_manager.get_recommendation()

        self.make_card(
            self.cards,
            1,
            1,
            title,
            body
        )



    def make_schedule_card(
        self,
        parent,
        row,
        column,
        classes
    ):

        print("CLASSES SENT TO CARD:", classes)

        card = GlassCard(parent)

        card.frame.grid(
            row=row,
            column=column,
            padx=12,
            pady=12,
            sticky="nsew"
        )

        card.frame.grid_propagate(False)

        card.frame.configure(
            width=450,
            height=300
        )


        content_frame = card.content

        content_frame.pack(
            fill="both",
            expand=True
        )


        header = tk.Frame(
            content_frame,
            bg=self.theme.get("card")
        )

        header.pack(
            fill="x",
            padx=15,
            pady=(10,5)
        )


        heading = tk.Label(
            header,
            text="Today's Classes",
            font=("Segoe UI",14,"bold"),
            bg=self.theme.get("card"),
            fg=self.theme.get("text"))

        heading.pack(
            side="left"
        )



        canvas = tk.Canvas(
            content_frame,
            bg=self.theme.get("card"),
            highlightthickness=0
        )


        scrollbar = tk.Scrollbar(
            content_frame,
            orient="vertical",
            command=canvas.yview
        )


        list_frame = tk.Frame(
            canvas,
            bg=self.theme.get("card")
        )


        window = canvas.create_window(
            (0,0),
            window=list_frame,
            anchor="nw"
        )


        list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )


        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(
                window,
                width=e.width
            )
        )


        canvas.configure(
            yscrollcommand=scrollbar.set
        )


        scroll_frame = tk.Frame(
            content_frame,
            bg=self.theme.get("background")
        )


        scroll_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0,10)
        )


        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.bind(
            "<Enter>",
            lambda e: canvas.bind_all(
                "<MouseWheel>",
                lambda event: canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )
            )
        )

        canvas.bind(
            "<Leave>",
            lambda e: canvas.unbind_all("<MouseWheel>")
        )



        if not classes:

            tk.Label(
                list_frame,
                text="No classes today.",
                bg=self.theme.get("card"),
                fg=self.theme.get("secondary_text"),
                font=("Segoe UI",11)
            ).pack(
                anchor="w",
                padx=10,
                pady=10
            )

            return



        # CLASS LIST

        for item in classes:

            print("CREATING CLASS:", item)


            class_box = tk.Frame(
                list_frame,
                bg=self.theme.get("button"),
                highlightbackground=self.theme.get("button_hover"),
                highlightthickness=1
            )


            class_box.pack(
                fill="x",
                padx=8,
                pady=8
            )


            course_name = self.course_manager.get_course_name(
                item["course_code"]
            )

            
            tk.Label(
                class_box,
                text=course_name if course_name else "Course name not added",
                font=("Segoe UI",11,"bold"),
                bg=self.theme.get("button"),
                fg=self.theme.get("text")
            ).pack(
                anchor="w",
                padx=10
            )

            tk.Label(
                class_box,
                text=item["course_code"],
                font=("Segoe UI",9),
                bg=self.theme.get("button"),
                fg=self.theme.get("secondary_text")
            ).pack(
                anchor="w",
                padx=10,
                pady=(8,0)
            )



            tk.Label(
                class_box,
                text=f"{item['start_time']} - {item.get('end_time','')}",
                font=("Segoe UI",9),
                bg=self.theme.get("button"),
                fg=self.theme.get("secondary_text")
            ).pack(
                anchor="w",
                padx=10
            )


            tk.Label(
                class_box,
                text=f"📍 {item['venue']}",
                font=("Segoe UI",9),
                bg=self.theme.get("button"),
                fg=self.theme.get("secondary_text")
            ).pack(
                anchor="w",
                padx=10,
                pady=(0,8)
            )

    def make_card(
        self,
        parent,
        row,
        column,
        title,
        body
    ):

        #print("TITLE:", title)
        #print("BODY:", body)

        card = GlassCard(parent)


        card.frame.grid(
            row=row,
            column=column,
            padx=12,
            pady=12,
            sticky="nsew"
        )

        card.frame.grid_propagate(False)
        card.frame.configure(
            width=450,
            height=300
        )

        content_frame = card.content

        content_frame.pack(
            side="right",
            fill="both",
            expand=True
        )
        
        heading = tk.Label(
            content_frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            bg=self.theme.get("card"),
            fg=self.theme.get("text")
        )


        heading.pack(
            anchor="w",
            padx=20,
            pady=(18,10)
        )

        body_frame = tk.Frame(
            content_frame,
            bg=self.theme.get("card")
        )

        body_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        body_canvas = tk.Canvas(
            body_frame,
            bg=self.theme.get("card"),
            highlightthickness=0
        )

        body_scrollbar = tk.Scrollbar(
            body_frame,
            orient="vertical",
            command=body_canvas.yview
        )

        body_content = tk.Frame(
            body_canvas,
            bg=self.theme.get("card")
        )

        body_window = body_canvas.create_window(
            (0, 0),
            window=body_content,
            anchor="nw"
        )

        body_content.bind(
            "<Configure>",
            lambda e: body_canvas.configure(
                scrollregion=body_canvas.bbox("all")
            )
        )

        body_canvas.bind(
            "<Configure>",
            lambda e: body_canvas.itemconfig(
                body_window,
                width=e.width
            )
        )

        body_canvas.configure(
            yscrollcommand=body_scrollbar.set
        )

        body_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        body_scrollbar.pack(
            side="right",
            fill="y"
        )

        content = tk.Label(
            body_content,
            text=body,
            justify="left",
            anchor="nw",
            wraplength=360,
            font=("Segoe UI", 12),
            bg=self.theme.get("card"),
            fg=self.theme.get("secondary_text")
        )

        content.pack(
            anchor="w",
            padx=10,
            pady=5,
            fill="x"
        )

        body_canvas.bind(
            "<Enter>",
            lambda e: body_canvas.bind_all(
                "<MouseWheel>",
                lambda event: body_canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )
            )
        )

        body_canvas.bind(
            "<Leave>",
            lambda e: body_canvas.unbind_all(
                "<MouseWheel>"
            )
        )

    def make_assignment_card(
        self,
        parent,
        row,
        column
    ):

        card = GlassCard(parent)
        

        card.frame.grid(
            row=row,
            column=column,
            padx=12,
            pady=12,
            sticky="nsew"
        )

        card.frame.grid_propagate(False)
        card.frame.configure(
            width=450,
            height=300
        )
        
        content_frame = card.content

        header = tk.Frame(
            content_frame,
            bg=self.theme.get("card")
        )

        header.pack(
            fill="x",
            padx=15,
            pady=(2,2)
        )


        heading = tk.Label(
            header,
            text="Upcoming Tasks",
            font=("Segoe UI",16,"bold"),
            bg=self.theme.get("card"),
            fg=self.theme.get("text")
        )

        heading.pack(
            side="left"
        )

        add_button = tk.Button(
            header,
            text="Add Assignment",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.open_assignment_page
        )

        add_button.pack(
            side="right"
        )

        # Scrollable assignment area
        assignment_canvas = tk.Canvas(
            content_frame,
            bg=self.theme.get("card"),
            highlightthickness=0
        )

        assignment_scrollbar = tk.Scrollbar(
            content_frame,
            orient="vertical",
            command=assignment_canvas.yview
        )


        assignment_grid = tk.Frame(
            assignment_canvas,
            bg=self.theme.get("card")
        )


        assignment_window = assignment_canvas.create_window(
            (0,0),
            window=assignment_grid,
            anchor="nw"
        )


        assignment_grid.bind(
            "<Configure>",
            lambda e: assignment_canvas.configure(
                scrollregion=assignment_canvas.bbox("all")
            )
        )


        assignment_canvas.bind(
            "<Configure>",
            lambda e: assignment_canvas.itemconfig(
                assignment_window,
                width=e.width
            )
        )


        assignment_canvas.configure(
            yscrollcommand=assignment_scrollbar.set
        )

        scroll_frame = tk.Frame(
            content_frame,
            bg=self.theme.get("card")
        )

        scroll_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0,10)
        )


        assignment_canvas.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=0
        )

        assignment_scrollbar.pack(
            side="right",
            fill="y"
        )

        assignment_canvas.bind(
            "<Enter>",
            lambda e: assignment_canvas.bind_all(
                "<MouseWheel>",
                lambda event: assignment_canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )
            )
        )


        assignment_canvas.bind(
            "<Leave>",
            lambda e: assignment_canvas.unbind_all(
                "<MouseWheel>"
            )
        )

        # Make 2 columns
        assignment_grid.grid_columnconfigure(
            0,
            weight=1,
            uniform="assignment"
        )

        assignment_grid.grid_columnconfigure(
            1,
            weight=1,
            uniform="assignment"
        )

        assignment_grid.grid_rowconfigure(
            0,
            weight=1,
            uniform="assignment"
        )

        assignment_grid.grid_rowconfigure(
            1,
            weight=1,
            uniform="assignment"
        )

        assignments = [

            assignment

            for assignment in self.assignment_manager.load_assignments()

            if not assignment.get("completed", False)
        ]


        if not assignments:

            tk.Label(
                assignment_grid,
                text="No assignments yet.",
                bg=self.theme.get("card"),
                fg=self.theme.get("secondary_text")
            ).grid(
                row=0,
                column=0,
                padx=20,
                pady=20,
                sticky="w"
            )

            return


        for index, assignment in enumerate(assignments):

            box = tk.Frame(
                assignment_grid,
                bg=self.theme.get("button"),
                highlightbackground=self.theme.get("button_hover"),
                highlightthickness=1
            )


            box.grid(
                row=index // 2,
                column=index % 2,
                padx=10,
                pady=10,
                sticky="nsew"
            )


            tk.Label(
                box,
                text=assignment.get(
                    "topic",
                    "Unnamed"
                ),
                font=("Segoe UI",12,"bold"),
                bg=self.theme.get("button"),
                fg=self.theme.get("text")
            ).pack(
                anchor="w",
                padx=10,
                pady=(8,0)
            )

            


            tk.Label(
                box,
                text=(
                    f"{assignment.get('course','')}\n"
                    f"Deadline: {assignment.get('deadline','')}"
                ),
                bg=self.theme.get("button"),
                fg=self.theme.get("secondary_text")
            ).pack(
                anchor="w",
                padx=10,
                pady=(0,8)
            )

            complete_button = tk.Button(
                box,
                text="Complete",
                bg=self.theme.get("accent"),
                fg=self.theme.get("text"),
                relief="flat",
                cursor="hand2",
                command=lambda a=assignment: self.complete_assignment(
                    a.get("topic")
                )
            )

            complete_button.pack(
                anchor="e",
                padx=10,
                pady=(0,10)
            )

    def open_assignment_page(self):

        if self.navigate:

            self.navigate(True)


    def complete_assignment(self, title):

        self.assignment_manager.complete_assignments(title)

        self.refresh_dashboard()

    def refresh_dashboard(self):

        for widget in self.cards.winfo_children():
            widget.destroy()

        today_classes =  self.get_active_today_classes()

        self.make_schedule_card(
            self.cards,
            0,
            0,
            today_classes
        )

        self.make_assignment_card(
            self.cards,
            0,
            1
        )

        self.make_progress_card(
            self.cards,
            1,
            0
        )

        title, body = self.ai_manager.get_recommendation()

        self.make_card(
            self.cards,
            1,
            1,
            title,
            body
        )

    def make_progress_card(
            self,
            parent,
            row,
            column
    ):
        
        card = GlassCard(parent)

        card.frame.grid(
            row=row,
            column=column,
            padx=12,
            pady=12,
            sticky="nsew"
        )

        card.frame.grid_propagate(False)

        card.frame.configure(
            width=450,
            height=300
        )

        content_frame = card.content
              
        tk.Label(
            content_frame,
            text="Progress",
            font=("Segoe UI",16,"bold"),
            bg=self.theme.get("card"),
            fg=self.theme.get("text")
        ).pack(
            anchor="w",
            padx=15,
            pady=(12,10)
        )

        progress_canvas = tk.Canvas(
            content_frame,
            bg=self.theme.get("card"),
            highlightthickness=0
        )

        progress_scrollbar = tk.Scrollbar(
            content_frame,
            orient="vertical",
            command=progress_canvas.yview
        )


        progress_frame = tk.Frame(
            progress_canvas,
            bg=self.theme.get("card")
        )


        progress_window = progress_canvas.create_window(
            (0,0),
            window=progress_frame,
            anchor="nw"
        )


        progress_frame.bind(
            "<Configure>",
            lambda e: progress_canvas.configure(
                scrollregion=progress_canvas.bbox("all")
            )
        )


        progress_canvas.bind(
            "<Configure>",
            lambda e: progress_canvas.itemconfig(
                progress_window,
                width=e.width
            )
        )


        progress_canvas.configure(
            yscrollcommand=progress_scrollbar.set
        )


        progress_canvas.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )


        progress_scrollbar.pack(
            side="right",
            fill="y"
        )

        progress_canvas.bind(
            "<Enter>",
            lambda e: progress_canvas.bind_all(
                "<MouseWheel>",
                lambda event: progress_canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )
            )
        )


        progress_canvas.bind(
            "<Leave>",
            lambda e: progress_canvas.unbind_all(
                "<MouseWheel>"
            )
        )


        recommendations = self.progress_manager.get_dashboard_progress()


        if not recommendations:

            tk.Label(
                progress_frame,
                text="Take a quiz to begin tracking your learning.",
                bg=self.theme.get("card"),
                fg=self.theme.get("secondary_text"),
                wraplength=380,
                justify="left"
            ).pack(
                anchor="w",
                padx=20,
                pady=10
            )

            return


        for item in recommendations:

            box = tk.Frame(
                progress_frame,
                bg=self.theme.get("button")
            )

            box.pack(
                fill="x",
                padx=15,
                pady=8
            )


            tk.Label(
                box,
                text=item["course"],
                bg=self.theme.get("button"),
                fg=self.theme.get("text"),
                font=("Segoe UI",12,"bold")
            ).pack(
                anchor="w",
                padx=10,
                pady=(8,2)
            )


            tk.Label(
                box,
                text=item["message"],
                bg=self.theme.get("button"),
                fg=self.theme.get("secondary_text"),
                wraplength=360,
                justify="left"
            ).pack(
                anchor="w",
                padx=10,
                pady=(0,8)
            )

    def get_active_today_classes(self):

        classes = self.schedule_manager.load_today_classes()

        now = datetime.now()

        active_classes = []

        for item in classes:

            end_time = item.get("end_time", "").strip()

            if not end_time:
                active_classes.append(item)
                continue

            try:

                end_datetime = datetime.strptime(
                    end_time,
                    "%I:%M %p"
                ).replace(
                    year=now.year,
                    month=now.month,
                    day=now.day
                )

                if end_datetime > now:
                    active_classes.append(item)

            except ValueError:

                # Keep the class visible if the time
                # cannot be interpreted safely.
                active_classes.append(item)

        return active_classes

    def auto_refresh_classes(self):

        if self.frame.winfo_exists():

            self.refresh_dashboard()

            self.frame.after(
                30000,
                self.auto_refresh_classes
            )