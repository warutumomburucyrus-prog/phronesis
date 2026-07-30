import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

from managers.pdf_manager import PDFManager
from managers.timetableparserai import TimetableAI
from managers.coursemanager import CourseManager
from managers.courseresolvermanager import CourseResolverManager
from widgets.coursecompletion import CourseCompletionDialog
from widgets.coursewizard import CourseWizard
from managers.schedulemanager import ScheduleManager
from managers.thememanager import ThemeManager
from managers.assignmentmanager import AssignmentManager
from widgets.addassignment import AddAssignmentDialog

class SchedulePage:


    def __init__(self, parent, navigate=None):

        self.theme = ThemeManager()

        self.navigate = navigate

        self.assignment_manager = AssignmentManager()

        self.frame = tk.Frame(
            parent,
            bg=self.theme.get("background")
        )

        # ==========================================================
        # MAIN SCHEDULE PAGE SCROLL
        # ==========================================================

        self.canvas = tk.Canvas(
            self.frame,
            bg=self.theme.get("background"),
            highlightthickness=0
        )

        self.scrollbar = tk.Scrollbar(
            self.frame,
            orient="vertical",
            command=self.canvas.yview
        )

        self.content_frame = tk.Frame(
            self.canvas,
            bg=self.theme.get("background")
        )

        self.content_window = self.canvas.create_window(
            (0, 0),
            window=self.content_frame,
            anchor="nw"
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

        # Update main scroll region whenever content changes
        self.content_frame.bind(
            "<Configure>",
            self._update_main_scrollregion
        )

        # Keep content width equal to the main canvas width
        self.canvas.bind(
            "<Configure>",
            self._resize_content
        )

        # ==========================================================
        # INNER TIMETABLE CANVASES
        # ==========================================================

        self.inner_canvases = set()

        # One global mouse-wheel binding.
        #
        # IMPORTANT:
        # Do NOT use bind_all/unbind_all inside individual
        # timetable cards. That was causing the scrolling conflict.
        self.frame.bind_all(
            "<MouseWheel>",
            self._on_global_mousewheel
        )

        # Linux support
        self.frame.bind_all(
            "<Button-4>",
            self._on_mousewheel_up
        )

        self.frame.bind_all(
            "<Button-5>",
            self._on_mousewheel_down
        )

        # ==========================================================
        # MANAGERS
        # ==========================================================

        self.pdf_manager = PDFManager()
        self.timetable_ai = TimetableAI()
        self.course_wizard = None
        self.course_manager = CourseManager()
        self.course_resolver = CourseResolverManager()
        self.schedule_manager = ScheduleManager()

        # ==========================================================
        # TITLE
        # ==========================================================

        title = tk.Label(
            self.content_frame,
            text="Timetable",
            font=("Telma", 28),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        )

        title.pack(
            pady=30
        )

        # ==========================================================
        # IMPORT BUTTON
        # ==========================================================

        self.import_button = tk.Button(
            self.content_frame,
            text="Import Timetable PDF",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.import_pdf
        )

        self.import_button.pack(
            pady=10
        )

        # ==========================================================
        # TIMETABLE CARD
        # ==========================================================

        self.schedule_card = tk.Frame(
            self.content_frame,
            bg=self.theme.get("card"),
            width=1000,
            height=460,
            highlightbackground=self.theme.get("button_hover"),
            highlightthickness=1
        )

        self.schedule_card.pack(
            padx=40,
            pady=20,
            fill="x",
            expand=True
        )

        self.schedule_card.pack_propagate(False)

        self.timetable_frame = tk.Frame(
            self.schedule_card,
            bg=self.theme.get("card")
        )

        self.timetable_frame.pack(
            fill="both",
            expand=True
        )

        # ==========================================================
        # BUILD TIMETABLE
        # ==========================================================

        self.build_timetable()

        # ==========================================================
        # ASSIGNMENTS HEADER
        # ==========================================================

        assignment_header = tk.Frame(
            self.content_frame,
            bg=self.theme.get("background")
        )

        assignment_header.pack(
            fill="x",
            padx=40,
            pady=(20, 10)
        )

        assignments_title = tk.Label(
            assignment_header,
            text="Assignments",
            font=("Segoe UI", 22, "bold"),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        )

        assignments_title.pack(
            side="left"
        )

        add_assignment_button = tk.Button(
            assignment_header,
            text="+ Add Assignment",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.add_assignment
        )

        add_assignment_button.pack(
            side="right"
        )

        # ==========================================================
        # ASSIGNMENTS CONTAINER
        # ==========================================================

        self.assignment_container = tk.Frame(
            self.content_frame,
            bg=self.theme.get("card"),
            highlightbackground=self.theme.get("button_hover"),
            highlightthickness=1
        )

        self.assignment_container.pack(
            padx=40,
            pady=10,
            fill="x"
        )

        self.assignment_container.grid_columnconfigure(
            0,
            weight=1
        )

        self.assignment_container.grid_columnconfigure(
            1,
            weight=1
        )

        self.load_assignments()

    # ==============================================================
    # MAIN SCROLL REGION
    # ==============================================================

    def _update_main_scrollregion(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def _resize_content(self, event):

        self.canvas.itemconfig(
            self.content_window,
            width=event.width
        )

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # ==============================================================
    # FIND INNER CANVAS UNDER MOUSE
    # ==============================================================

    def _find_inner_canvas(self, widget):

        current = widget

        while current is not None:

            if current in self.inner_canvases:

                return current

            try:
                current = current.master
            except AttributeError:
                break

        return None

    # ==============================================================
    # GLOBAL MOUSE WHEEL
    # ==============================================================

    def _on_global_mousewheel(self, event):

        inner_canvas = self._find_inner_canvas(
            event.widget
        )

        # If mouse is inside one of the timetable day cards,
        # scroll that day's class list.
        if inner_canvas is not None:

            inner_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

            return

        # Otherwise scroll the entire SchedulePage.
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ==============================================================
    # LINUX MOUSE WHEEL
    # ==============================================================

    def _on_mousewheel_up(self, event):

        inner_canvas = self._find_inner_canvas(
            event.widget
        )

        if inner_canvas is not None:

            inner_canvas.yview_scroll(
                -1,
                "units"
            )

            return

        self.canvas.yview_scroll(
            -1,
            "units"
        )

    def _on_mousewheel_down(self, event):

        inner_canvas = self._find_inner_canvas(
            event.widget
        )

        if inner_canvas is not None:

            inner_canvas.yview_scroll(
                1,
                "units"
            )

            return

        self.canvas.yview_scroll(
            1,
            "units"
        )

    # ==============================================================
    # IMPORT TIMETABLE
    # ==============================================================

    def import_pdf(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("PDF Files", "*.pdf")
            ]
        )

        if not file_path:
            return

        try:

            # Step 1: Extract PDF text
            text = self.pdf_manager.extract_text(
                file_path
            )

            # Step 2: Ask Gemini to structure timetable
            schedule_json = self.timetable_ai.convert_to_schedule(
                text
            )

            added = self.course_manager.auto_add_from_schedule(
                schedule_json
            )

            print(
                f"automatically added {added} new courses"
            )

            course_codes = list({
                lesson["course_code"]
                for lesson in schedule_json
            })

            resolved_names = self.course_resolver.resolve(
                course_codes
            )

            self.course_manager.update_course_names(
                resolved_names
            )

            missing = self.course_manager.get_incomplete_courses()

            if missing:

                if self.course_wizard is None:

                    self.course_wizard = CourseWizard(
                        self.frame,
                        missing,
                        self.course_manager.update_course_by_code,
                        self.wizard_finished
                    )

            # Step 3: Save timetable
            os.makedirs(
                "data",
                exist_ok=True
            )

            with open(
                "data/schedule.json",
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    schedule_json,
                    file,
                    indent=4
                )

            # Rebuild timetable immediately after importing.
            self.schedule_manager = ScheduleManager()

            for widget in self.timetable_frame.winfo_children():
                widget.destroy()

            self.inner_canvases.clear()

            self.build_timetable()

            self.content_frame.update_idletasks()

            self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )

            messagebox.showinfo(
                "Success",
                f"Timetable imported successfully\n\n"
                f"{added} new course(s) added automatically."
            )

        except Exception as e:

            import traceback
            traceback.print_exc()

            messagebox.showerror(
                "Import Error",
                f"Could not import timetable.\n\n{e}"
            )

    # ==============================================================
    # WIZARD FINISHED
    # ==============================================================

    def wizard_finished(self):

        self.course_wizard = None

        messagebox.showinfo(
            title="Complete",
            message="All courses completed!"
        )

        # Refresh timetable course names after wizard
        for widget in self.timetable_frame.winfo_children():
            widget.destroy()

        self.inner_canvases.clear()

        self.build_timetable()

        self.content_frame.update_idletasks()

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # ==============================================================
    # BUILD TIMETABLE
    # ==============================================================

    def build_timetable(self):

        schedule = self.schedule_manager.load_week_schedule()

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]

        self.timetable_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.timetable_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.timetable_frame.grid_columnconfigure(
            2,
            weight=1
        )

        self.timetable_frame.grid_rowconfigure(
            0,
            weight=1
        )

        self.timetable_frame.grid_rowconfigure(
            1,
            weight=1
        )

        for index, day in enumerate(days):

            if index < 3:

                row = 0
                column = index

            else:

                row = 1
                column = index - 3

            # ======================================================
            # DAY CARD
            # ======================================================

            day_frame = tk.Frame(
                self.timetable_frame,
                bg=self.theme.get("button"),
                highlightbackground=self.theme.get("button_hover"),
                highlightthickness=1
            )

            day_frame.grid(
                row=row,
                column=column,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            # ======================================================
            # DAY TITLE
            # ======================================================

            title = tk.Label(
                day_frame,
                text=day,
                font=("Segoe UI", 14, "bold"),
                bg=self.theme.get("button"),
                fg=self.theme.get("text")
            )

            title.pack(
                fill="x",
                padx=12,
                pady=(10, 8)
            )

            # ======================================================
            # INNER CLASS CANVAS
            # ======================================================

            class_canvas = tk.Canvas(
                day_frame,
                bg=self.theme.get("button"),
                highlightthickness=0
            )

            class_scrollbar = tk.Scrollbar(
                day_frame,
                orient="vertical",
                command=class_canvas.yview
            )

            class_list = tk.Frame(
                class_canvas,
                bg=self.theme.get("button")
            )

            class_window = class_canvas.create_window(
                (0, 0),
                window=class_list,
                anchor="nw"
            )

            # Register this inner canvas.
            self.inner_canvases.add(
                class_canvas
            )

            # Update inner scroll region.
            class_list.bind(
                "<Configure>",
                lambda event, canvas=class_canvas:
                canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            # Keep inner content width equal to canvas width.
            class_canvas.bind(
                "<Configure>",
                lambda event,
                canvas=class_canvas,
                window=class_window:
                canvas.itemconfig(
                    window,
                    width=event.width
                )
            )

            class_canvas.configure(
                yscrollcommand=class_scrollbar.set
            )

            class_canvas.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(8, 0),
                pady=(0, 8)
            )

            class_scrollbar.pack(
                side="right",
                fill="y",
                pady=(0, 8)
            )

            # ======================================================
            # CLASSES FOR THIS DAY
            # ======================================================

            classes = schedule.get(
                day,
                []
            )

            if not classes:

                tk.Label(
                    class_list,
                    text="No classes",
                    bg=self.theme.get("button"),
                    fg=self.theme.get("secondary_text"),
                    font=("Segoe UI", 10)
                ).pack(
                    anchor="w",
                    padx=10,
                    pady=10
                )

            else:

                for item in classes:

                    course_name = self.course_manager.get_course_name(
                        item["course_code"]
                    )

                    class_box = tk.Frame(
                        class_list,
                        bg=self.theme.get("card"),
                        highlightbackground=self.theme.get("button_hover"),
                        highlightthickness=1
                    )

                    class_box.pack(
                        fill="x",
                        padx=8,
                        pady=5
                    )

                    # ==================================================
                    # COURSE NAME
                    # ==================================================

                    tk.Label(
                        class_box,
                        text=(
                            course_name
                            if course_name
                            else item["course_code"]
                        ),
                        bg=self.theme.get("card"),
                        fg=self.theme.get("text"),
                        font=("Segoe UI", 10, "bold"),
                        anchor="w",
                        justify="left",
                        wraplength=250
                    ).pack(
                        fill="x",
                        padx=10,
                        pady=(8, 1)
                    )

                    # ==================================================
                    # COURSE CODE
                    # ==================================================

                    tk.Label(
                        class_box,
                        text=item["course_code"],
                        bg=self.theme.get("card"),
                        fg=self.theme.get("secondary_text"),
                        font=("Segoe UI", 9),
                        anchor="w"
                    ).pack(
                        fill="x",
                        padx=10
                    )

                    # ==================================================
                    # TIME
                    # ==================================================

                    tk.Label(
                        class_box,
                        text=(
                            f"{item['start_time']} - "
                            f"{item['end_time']}"
                        ),
                        bg=self.theme.get("card"),
                        fg=self.theme.get("secondary_text"),
                        font=("Segoe UI", 9),
                        anchor="w"
                    ).pack(
                        fill="x",
                        padx=10
                    )

                    # ==================================================
                    # VENUE
                    # ==================================================

                    tk.Label(
                        class_box,
                        text=f"📍 {item['venue']}",
                        bg=self.theme.get("card"),
                        fg=self.theme.get("secondary_text"),
                        font=("Segoe UI", 9),
                        anchor="w"
                    ).pack(
                        fill="x",
                        padx=10,
                        pady=(0, 8)
                    )

    # ==============================================================
    # ASSIGNMENTS
    # ==============================================================

    def load_assignments(self):

        assignments = [
            assignment
            for assignment in self.assignment_manager.load_assignments()
            if not assignment.get("completed", False)
        ]

        if not assignments:

            tk.Label(
                self.assignment_container,
                text="No assignments yet.",
                bg=self.theme.get("card"),
                fg=self.theme.get("secondary_text"),
                font=("Segoe UI", 11)
            ).pack(
                padx=20,
                pady=20
            )

            return

        for index, assignment in enumerate(assignments):

            card = tk.Frame(
                self.assignment_container,
                bg=self.theme.get("button"),
                highlightbackground=self.theme.get("button_hover"),
                highlightthickness=1
            )

            card.grid(
                row=index // 2,
                column=index % 2,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            info = tk.Frame(
                card,
                bg=self.theme.get("button")
            )

            info.pack(
                side="left",
                expand=True,
                fill="x",
                padx=10,
                pady=10
            )

            tk.Label(
                info,
                text=assignment.get(
                    "topic",
                    "Unnamed Assignment"
                ),
                font=("Segoe UI", 13, "bold"),
                bg=self.theme.get("button"),
                fg=self.theme.get("text")
            ).pack(
                anchor="w"
            )

            tk.Label(
                info,
                text=(
                    f"Course: {assignment.get('course', '')}\n"
                    f"Deadline: {assignment.get('deadline', '')}\n"
                    f"Submit: {assignment.get('submission', '')}"
                ),
                bg=self.theme.get("button"),
                fg=self.theme.get("secondary_text"),
                justify="left"
            ).pack(
                anchor="w"
            )

            buttons = tk.Frame(
                card,
                bg=self.theme.get("button")
            )

            buttons.pack(
                side="right",
                padx=10
            )

            tk.Button(
                buttons,
                text="Edit",
                bg=self.theme.get("button_hover"),
                fg=self.theme.get("text"),
                relief="flat",
                command=lambda a=assignment:
                self.edit_assignment(a)
            ).pack(
                pady=5
            )

            tk.Button(
                buttons,
                text="✓ Complete",
                bg=self.theme.get("accent"),
                fg=self.theme.get("text"),
                relief="flat",
                command=lambda a=assignment:
                self.complete_assignment(a)
            ).pack(
                pady=5
            )

    # ==============================================================
    # COMPLETE ASSIGNMENT
    # ==============================================================

    def complete_assignment(self, assignment):

        self.assignment_manager.complete_assignments(
            assignment.get("topic")
        )

        for widget in self.assignment_container.winfo_children():
            widget.destroy()

        self.load_assignments()

        self.content_frame.update_idletasks()

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # ==============================================================
    # ADD ASSIGNMENT
    # ==============================================================

    def add_assignment(self):

        AddAssignmentDialog(
            self.frame,
            self.save_assignment
        )

    # ==============================================================
    # EDIT ASSIGNMENT
    # ==============================================================

    def edit_assignment(self, assignment):

        AddAssignmentDialog(
            self.frame,
            lambda updated:
            self.update_assignment(
                assignment,
                updated
            ),
            assignment
        )

    # ==============================================================
    # SAVE ASSIGNMENT
    # ==============================================================

    def save_assignment(self, assignment):

        assignments = self.assignment_manager.load_assignments()

        assignments.append(
            assignment
        )

        self.assignment_manager.save_assignments(
            assignments
        )

        messagebox.showinfo(
            "Success",
            "Assignment added successfully!"
        )

        if self.navigate:
            self.navigate()

    # ==============================================================
    # UPDATE ASSIGNMENT
    # ==============================================================

    def update_assignment(
        self,
        old_assignment,
        updated_assignment
    ):

        assignments = self.assignment_manager.load_assignments()

        for index, assignment in enumerate(assignments):

            if assignment == old_assignment:

                assignments[index] = updated_assignment

                break

        self.assignment_manager.save_assignments(
            assignments
        )

        for widget in self.assignment_container.winfo_children():
            widget.destroy()

        self.load_assignments()

        self.content_frame.update_idletasks()

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # ==============================================================
    # SHOW ASSIGNMENT SECTION
    # ==============================================================

    def show_assignment_section(self):

        self.canvas.update_idletasks()
        self.content_frame.update_idletasks()

        target_y = self.assignment_container.winfo_y()

        content_height = self.content_frame.winfo_height()
        canvas_height = self.canvas.winfo_height()

        if content_height <= canvas_height:
            return

        max_scroll = content_height - canvas_height

        if max_scroll <= 0:
            return

        position = target_y / max_scroll

        position = max(
            0,
            min(position, 1)
        )

        self.canvas.yview_moveto(
            position
        )
