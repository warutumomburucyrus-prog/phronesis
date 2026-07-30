import tkinter as tk

from managers.progressmanager import ProgressManager
from managers.thememanager import ThemeManager


class ProgressPage:


    def __init__(self, parent):

        self.theme = ThemeManager()

        self.progress_manager = ProgressManager()

        self.progress = self.progress_manager.load_progress()

        stats = self.calculate_stats()

        self.frame = tk.Frame(
            parent,
            bg=self.theme.get("background")
        )


        title = tk.Label(
            self.frame,
            text="Learning Progress",
            font=("Telma", 28),
            bg=self.theme.get("background"),
            fg=self.theme.get("text")
        )

        title.pack(
            pady=20
        )


        self.summary_label = tk.Label(
            self.frame,
            text="",
            font=("Segoe UI", 14),
            bg=self.theme.get("background"),
            fg=self.theme.get("text"),
            justify="left"
        )

        self.summary_label.pack(
            pady=20
        )


        self.quiz_list = tk.Listbox(
            self.frame,
            width=60,
            height=10,
            bg=self.theme.get("card"),
            fg=self.theme.get("text"),
            relief="flat"
        )

        self.quiz_list.pack(
            pady=20
        )


        self.load_progress()

        self.summary = tk.Label(

            self.frame,

            text=
            f"""
        Total Quizzes : {stats['quizzes']}

        Questions Answered : {stats['questions']}

        Correct Answers : {stats['correct']}

        Overall Accuracy : {stats['accuracy']}%
        """,

            bg=self.theme.get("background"),

            fg=self.theme.get("text"),

            justify="left",

            font=("Segoe UI",14)

        )

        self.summary.pack(
            anchor="w",
            padx=25,
            pady=20
        )

        history_title = tk.Label(

            self.frame,

            text="Recent Quiz History",

            bg=self.theme.get("background"),

            fg=self.theme.get("text"),

            font=("Segoe UI",15,"bold")

        )

        history_title.pack(
            anchor="w",
            padx=25,
            pady=(15,10)
        )

        for quiz in reversed(self.progress[-5:]):

            tk.Label(

                self.frame,

                text=
                f"{quiz['date'][:16]}    {quiz['score']}/{quiz['total_questions']}    ({quiz['percentage']}%)",

                bg=self.theme.get("background"),

                fg="#CCCCCC",

                font=("Segoe UI",11)

            ).pack(
                anchor="w",
                padx=40,
                pady=2
            )


    def load_progress(self):

        progress = self.progress_manager.load_progress()


        if not progress:

            self.summary_label.config(
                text="No quiz attempts yet."
            )

            return



        total_score = 0
        total_questions = 0



        for quiz in progress:

            total_score += quiz["score"]

            total_questions += quiz["total_questions"]


            self.quiz_list.insert(
                tk.END,
                f'{quiz["date"][:10]}   Score: {quiz["score"]}/{quiz["total_questions"]}'
            )



        percentage = round(
            (total_score / total_questions) * 100,
            2
        )


        self.summary_label.config(
            text=
            f"""
        Overall Performance

        Questions Attempted:
        {total_questions}

        Correct Answers:
        {total_score}

        Average Score:
        {percentage}%
        """
                )

    def calculate_stats(self):

        progress = self.progress

        if not progress:

            return {
                "quizzes": 0,
                "questions": 0,
                "correct": 0,
                "accuracy": 0
            }

        quizzes = len(progress)

        questions = 0

        correct = 0

        for quiz in progress:

            questions += quiz["total_questions"]

            correct += quiz["score"]

        accuracy = round(
            (correct / questions) * 100,
            1
        )

        return {

            "quizzes": quizzes,

            "questions": questions,

            "correct": correct,

            "accuracy": accuracy

        }