import tkinter as tk
import ctypes

from widgets.windowcontrols import WindowControls
from widgets.title_bar import TitleBar
from widgets.nav import NavButton
from widgets.statusbar import StatusBar

from pages.dashboardpage import DashboardPage
from pages.coursespage import CoursesPage
from pages.plannerpage import PlannerPage
from pages.schedulepage import SchedulePage
from pages.progresspage import ProgressPage
from pages.profilepage import ProfilePage
from pages.settingspage import SettingsPage

from managers.thememanager import ThemeManager


class Dashboard:

    def __init__(self, root):

        self.root = root

        self.window = root

        self.window.title("Phronesis")
        
        self.theme = ThemeManager()

        window_width = 1200
        window_height = 700

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.window.geometry(
            f"{window_width}x{window_height}+{x}+{y}"
        )

        self.window.configure(
            bg=self.theme.get("background")
        )

        self.window.update()

        hwnd = ctypes.windll.user32.GetParent(
            self.window.winfo_id()
        )

        value = ctypes.c_int(1)

        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            20,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )

        self.update_title_bar()

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        self.sidebar = tk.Frame(
            self.window,
            width=90,
            bg=self.theme.get("sidebar")
        )

        self.sidebar.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="ns"
        )

        self.sidebar.grid_propagate(False)

        self.dashboard_btn=NavButton(
            self.sidebar,
            "Dashboard",
            self.show_dashboard,
            "assets/icons/dashboard.png",
            self.theme.get("icon")
        )


        self.courses_btn=NavButton(
            self.sidebar,
            "Courses",
            self.show_courses,
            "assets/icons/courses.png",
             self.theme.get("icon")
        )


        self.planner_btn=NavButton(
            self.sidebar,
            "Planner",
            self.show_planner,
            "assets/icons/planner.png",
             self.theme.get("icon")
        )


        self.schedule_btn=NavButton(
            self.sidebar,
            "Schedule",
            self.show_schedule,
            "assets/icons/schedule.png",
             self.theme.get("icon")
        )


        self.progress_btn=NavButton(
            self.sidebar,
            "Progress",
            self.show_progress,
            "assets/icons/progress.png",
             self.theme.get("icon")
        )

        self.profile_btn=NavButton(
            self.sidebar,
            "Profile",
            self.show_profile,
            "assets/icons/profile.png",
             self.theme.get("icon")
        )

        tk.Frame(
            self.sidebar,
            bg=self.theme.get("sidebar")
        ).pack(
            expand=True,
            fill="both"
        )


        self.settings_btn=NavButton(
            self.sidebar,
            "Settings",
            self.show_settings,
            "assets/icons/settings.png"
        )

        self.content = tk.Frame(
            self.window,
            bg=self.theme.get("background")
        )


        self.content.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.page_container = tk.Frame(
            self.content,
            bg=self.theme.get("background")
        )


        self.page_container.pack(
            expand=True,
            fill="both"
        )


        self.current_page = None
        self.show_dashboard()


        self.status_bar = StatusBar(
            self.window
        )

        self.status_bar.frame.grid(
            row = 1,
            column = 1,
            sticky = "ew"
        )

    def show_page(self, page_class, button):

        if not hasattr(self, "pages"):
            self.pages = {}


        page_name = page_class.__name__


        if page_name not in self.pages:

            if page_class == DashboardPage:

                page = page_class(
                    self.page_container,
                    self.show_schedule
                )

            elif page_class == SchedulePage:

                page = page_class(
                    self.page_container,
                    self.show_dashboard
                )

            elif page_class == SettingsPage:

                page = page_class(
                    self.page_container,
                    self.refresh_theme
                )

            else:

                page = page_class(
                    self.page_container
                )


            self.pages[page_name] = page


        page = self.pages[page_name]

        if page_class == DashboardPage:

            page.refresh_dashboard()

        elif page_class == SchedulePage:

            for widget in page.assignment_container.winfo_children():
                widget.destroy()

            page.load_assignments()

        for p in self.pages.values():

            p.frame.pack_forget()

        page.frame.pack(
            expand=True,
            fill="both"
        )


        self.select_button(button)


        self.current_page = page.frame

    def select_button(self, selected_button):

        buttons = [
            self.dashboard_btn,
            self.courses_btn,
            self.planner_btn,
            self.schedule_btn,
            self.progress_btn,
            self.profile_btn,
            self.settings_btn
        ]

        for button in buttons:
            button.set_selected(False)
        
        selected_button.set_selected(True)

    def show_dashboard(self):

        self.show_page(
            DashboardPage,
            self.dashboard_btn
        )



    def show_courses(self):

        self.show_page(
            CoursesPage,
            self.courses_btn
        )



    def show_profile(self):

        self.show_page(
            ProfilePage,
            self.profile_btn
        )



    def show_planner(self):

        self.show_page(
            PlannerPage,
            self.planner_btn
        )


    def show_schedule(self, focus_assignments=False):

        self.show_page(
            SchedulePage,
            self.schedule_btn
        )

        if focus_assignments:

            self.window.after(
                100,
                self.focus_schedule_assignments
            )

    def focus_schedule_assignments(self):

        schedule_page = self.pages.get(
            "SchedulePage"
        )

        if schedule_page:

            schedule_page.show_assignment_section()

    def show_progress(self):

        self.show_page(
            ProgressPage,
            self.progress_btn
        )

    def show_settings(self):

        self.show_page(
            SettingsPage,
            self.settings_btn
        )

    def refresh_theme(self):

        self.theme = ThemeManager()

        # Main window
        self.window.configure(
            bg=self.theme.get("background")
        )

        # Sidebar
        self.sidebar.configure(
            bg=self.theme.get("sidebar")
        )

        # Rebuild sidebar buttons
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        self.dashboard_btn = NavButton(
            self.sidebar,
            "Dashboard",
            self.show_dashboard,
            "assets/icons/dashboard.png",
            self.theme.get("icon")
        )

        self.courses_btn = NavButton(
            self.sidebar,
            "Courses",
            self.show_courses,
            "assets/icons/courses.png",
            self.theme.get("icon")
        )

        self.planner_btn = NavButton(
            self.sidebar,
            "Planner",
            self.show_planner,
            "assets/icons/planner.png",
            self.theme.get("icon")
        )

        self.schedule_btn = NavButton(
            self.sidebar,
            "Schedule",
            self.show_schedule,
            "assets/icons/schedule.png",
            self.theme.get("icon")
        )

        self.progress_btn = NavButton(
            self.sidebar,
            "Progress",
            self.show_progress,
            "assets/icons/progress.png",
            self.theme.get("icon")
        )

        self.profile_btn = NavButton(
            self.sidebar,
            "Profile",
            self.show_profile,
            "assets/icons/profile.png",
            self.theme.get("icon")
        )

        tk.Frame(
            self.sidebar,
            bg=self.theme.get("sidebar")
        ).pack(
            expand=True,
            fill="both"
        )

        self.settings_btn = NavButton(
            self.sidebar,
            "Settings",
            self.show_settings,
            "assets/icons/settings.png",
            self.theme.get("icon")
        )

        # Rebuild pages
        self.pages = {}

        for widget in self.page_container.winfo_children():
            widget.destroy()

        # Rebuild status bar
        if hasattr(self, "status_bar"):
            self.status_bar.frame.destroy()

        self.status_bar = StatusBar(
            self.window
        )

        self.status_bar.frame.grid(
            row=1,
            column=1,
            sticky="ew"
        )

        # Update Windows title bar
        self.update_title_bar()

        # Show dashboard again
        self.show_dashboard()

    def update_title_bar(self):

        hwnd = ctypes.windll.user32.GetParent(
            self.window.winfo_id()
        )

        color = self.theme.get("background")

        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)

        color_ref = r | (g << 8) | (b << 16)

        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            35,
            ctypes.byref(
                ctypes.c_int(color_ref)
            ),
            ctypes.sizeof(
                ctypes.c_int(color_ref)
            )
        )