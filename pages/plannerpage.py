import tkinter as tk
import threading
import json

from tkinter import filedialog, messagebox

from managers.aimanager import AIManager
from managers.studymanager import StudyManager
from managers.notereader import NoteReader
from managers.progressmanager import ProgressManager
from managers.thememanager import ThemeManager


class PlannerPage:

    def __init__(self, parent):

        self.theme = ThemeManager()

        self.ai = AIManager()

        self.study_manager = StudyManager()

        self.note_reader = NoteReader()

        self.progress_manager = ProgressManager()


        self.current_quiz = []

        self.current_question = 0

        self.score = 0

        self.user_answers = {}

        self.quiz_evaluations = {}

        self.review_question = 0

        self.answer_box = None

        self.previous_questions = []


        self.frame = tk.Frame(
            parent,
            bg=self.theme.get("background")
        )


        self.canvas = tk.Canvas(
            self.frame,
            bg=self.theme.get("background"),
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            self.frame,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scroll_frame = tk.Frame(
            self.canvas,
            bg=self.theme.get("background")
        )

        self.scroll_frame.bind(
            "<Configure>",
            lambda event:
                self.canvas.configure(
                    scrollregion=self.canvas.bbox("all")
                )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor="nw"
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_scroll_frame
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        library_title = tk.Label(
            self.scroll_frame,
            text="Your Notes",
            bg=self.theme.get("background"),
            fg=self.theme.get("text"),
            font=("Segoe UI", 12, "bold")
        )

        library_title.pack(
            pady=(20, 5)
        )

        self.notes_list = tk.Listbox(
            self.scroll_frame,
            width=60,
            height=6,
            bg=self.theme.get("card"),
            fg=self.theme.get("text"),
            selectbackground="#5B2EFF",
            selectforeground=self.theme.get("text"),
            relief="flat",
            highlightthickness=0
        )

        self.notes_list.pack(
            pady=(0, 10)
        )


        notes_button_frame = tk.Frame(
            self.scroll_frame,
            bg=self.theme.get("background")
        )

        notes_button_frame.pack(
            pady=(0, 15)
        )

        self.upload_button = tk.Button(
            notes_button_frame,
            text="Upload Notes",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            cursor="hand2",
            command=self.upload_pdf
        )

        self.upload_button.pack(
            side="left",
            padx=5
        )

        self.delete_button = tk.Button(
            notes_button_frame,
            text="Delete Selected",
            bg="#B22222",
            fg=self.theme.get("text"),
            relief="flat",
            cursor="hand2",
            command=self.delete_note
        )

        self.delete_button.pack(
            side="left",
            padx=5
        )

        self.refresh_notes()


        quiz_settings = tk.Frame(
            self.scroll_frame,
            bg=self.theme.get("background")
        )

        quiz_settings.pack(
            pady=(5, 10)
        )

        tk.Label(
            quiz_settings,
            text="Number of Questions",
            bg=self.theme.get("background"),
            fg=self.theme.get("secondary_text"),
            font=("Segoe UI", 10)
        ).pack(
            side="left",
            padx=(0, 8)
        )

        self.quiz_count_var = tk.IntVar(
            value=5
        )

        self.quiz_count = tk.Spinbox(
            quiz_settings,
            from_=3,
            to=30,
            textvariable=self.quiz_count_var,
            width=5,
            bg=self.theme.get("card"),
            fg=self.theme.get("text"),
            insertbackground="white",
            buttonbackground="#5B2EFF",
            relief="flat"
        )

        self.quiz_count.pack(
            side="left"
        )


        button_frame = tk.Frame(
            self.scroll_frame,
            bg=self.theme.get("background")
        )

        button_frame.pack(
            pady=10
        )

        self.summarise_button = tk.Button(
            button_frame,
            text="Summarise Notes",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            cursor="hand2",
            command=self.summarise_notes
        )

        self.summarise_button.pack(
            side="left",
            padx=10
        )

        self.quiz_button = tk.Button(
            button_frame,
            text="Generate Quiz",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            cursor="hand2",
            command=self.generate_quiz
        )

        self.quiz_button.pack(
            side="left",
            padx=10
        )

        self.quiz_display_frame = tk.Frame(
            self.scroll_frame,
            bg=self.theme.get("background")
        )

        self.quiz_display_frame.pack(
            fill="x",
            expand=True,
            pady=(30, 10)
        )

        self.quiz_display_frame.columnconfigure(
            0,
            weight=1
        )

        self.question_label = tk.Label(
            self.quiz_display_frame,
            text="",
            bg=self.theme.get("background"),
            fg=self.theme.get("text"),
            font=("Segoe UI", 15, "bold"),
            wraplength=800,
            justify="left"
        )

        self.question_label.pack(
            pady=(20, 25),
            padx=40,
            fill="x"
        )

        self.feedback_label = tk.Label(
            self.scroll_frame,
            text="",
            bg=self.theme.get("background"),
            fg=self.theme.get("secondary_text"),
            font=("Segoe UI", 12),
            wraplength=800,
            justify="left"
        )

        self.feedback_label.pack(
            pady=10
        )


        self.answer_var = tk.StringVar()

        self.answers_frame = tk.Frame(
            self.quiz_display_frame,
            bg=self.theme.get("background")
        )

        self.answers_frame.pack(
            pady=10,
            fill="x"
        )


        self.navigation_frame = tk.Frame(
            self.quiz_display_frame,
            bg=self.theme.get("background")
        )

        self.navigation_frame.pack(
            pady=(20, 30),
            fill="x"
        )

        self.previous_button = tk.Button(
            self.navigation_frame,
            text="Previous",
            bg="#444444",
            fg=self.theme.get("text"),
            relief="flat",
            command=self.previous_question
        )

        self.next_button = tk.Button(
            self.navigation_frame,
            text="Next",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.next_question
        )

        self.submit_button = tk.Button(
            self.navigation_frame,
            text="Submit Quiz",
            bg="#00AA55",
            fg=self.theme.get("text"),
            relief="flat",
            command=self.submit_quiz
        )

        self.review_button = tk.Button(
            self.scroll_frame,
            text="Review Answers",
            bg=self.theme.get("accent"),
            fg=self.theme.get("text"),
            relief="flat",
            command=self.start_review
        )


        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )


    def on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def resize_scroll_frame(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )


    def refresh_notes(self):

        self.notes_list.delete(
            0,
            tk.END
        )

        notes = self.study_manager.load_notes()

        for note in notes:

            self.notes_list.insert(
                tk.END,
                note.get(
                    "name",
                    "Unnamed note"
                )
            )

    def upload_pdf(self):

        file_path = filedialog.askopenfilename(
            title="Select Study Notes",
            filetypes=[
                ("PDF Files", "*.pdf")
            ]
        )

        if not file_path:
            return

        try:

            self.study_manager.add_pdf(
                file_path
            )

            self.refresh_notes()

            self.feedback_label.config(
                text="Note uploaded successfully.",
                fg="#66DD88"
            )

        except Exception as e:

            self.feedback_label.config(
                text=f"Could not upload note:\n{e}",
                fg="#FF7777"
            )

    def delete_note(self):

        selected = self.notes_list.curselection()

        if not selected:

            self.feedback_label.config(
                text="Select a note first.",
                fg=self.theme.get("secondary_text")
            )

            return

        index = selected[0]

        notes = self.study_manager.load_notes()

        if index >= len(notes):
            return

        note = notes[index]

        confirmed = messagebox.askyesno(
            "Delete Note",
            f"Delete '{note.get('name', 'this note')}'?"
        )

        if not confirmed:
            return

        try:

            self.study_manager.delete_note(
                index
            )

            self.refresh_notes()

            self.feedback_label.config(
                text="Note deleted.",
                fg=self.theme.get("secondary_text")
            )

        except Exception as e:

            self.feedback_label.config(
                text=f"Could not delete note:\n{e}",
                fg="#FF7777"
            )


    def summarise_notes(self):

        selected = self.notes_list.curselection()

        if not selected:

            self.feedback_label.config(
                text="Select a note first.",
                fg=self.theme.get("secondary_text")
            )

            return

        notes = self.study_manager.load_notes()

        note = notes[selected[0]]

        try:

            text = self.note_reader.extract_text(
                note["path"]
            )

        except Exception as e:

            self.feedback_label.config(
                text=f"Could not read PDF:\n{e}",
                fg="#FF7777"
            )

            return

        if not text.strip():

            self.feedback_label.config(
                text="No readable text was found in this PDF.",
                fg="#FF7777"
            )

            return

        self.summarise_button.config(
            state="disabled",
            text="Summarising..."
        )

        self.feedback_label.config(
            text="Phronesis is reading your notes..."
        )

        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        self.question_label.config(
            text="Summarising your notes..."
        )

        self.previous_button.pack_forget()
        self.next_button.pack_forget()
        self.submit_button.pack_forget()
        self.review_button.pack_forget()

        self.current_quiz = []
        self.current_question = 0
        self.score = 0
        self.user_answers = {}
        self.quiz_evaluations = {}
        self.review_question = 0
        self.answer_box = None

        self.previous_button.config(
            command=self.previous_question
        )

        self.next_button.config(
            command=self.next_question
        )

        self.submit_button.config(
            command=self.submit_quiz,
            state="normal",
            text="Submit Quiz"
        )

        self.review_button.config(
            command=self.start_review,
            text="Review Answers"
        )

        threading.Thread(
            target=self.summary_worker,
            args=(text,),
            daemon=True
        ).start()

    def summary_worker(self, text):

        try:

            print(
                "SUMMARY INPUT SIZE:",
                len(text)
            )

            summary = self.ai.summarise_notes(
                text
            )

            print(
                "SUMMARY RESULT SIZE:",
                len(summary) if summary else 0
            )

            print(
                "SUMMARY RESULT:",
                summary[:500] if summary else "EMPTY"
            )

            self.frame.after(
                0,
                lambda:
                    self.show_summary(summary)
            )

        except Exception as e:

            error = str(e)

            print(
                "SUMMARY GENERATION ERROR:",
                error
            )

            self.frame.after(
                0,
                lambda:
                    self.summary_failed(error)
            )

    def show_summary(self, summary):

        self.summarise_button.config(
            state="normal",
            text="Summarise Notes"
        )

        if not summary or not summary.strip():

            self.feedback_label.config(
                text="Phronesis generated an empty summary.",
                fg="#FF7777"
            )

            self.question_label.config(
                text="Summary unavailable."
            )

            return

        self.feedback_label.config(
            text="Summary generated successfully.",
            fg="#66DD88"
        )

        self.question_label.config(
            text="Revision Guide",
            fg=self.theme.get("text")
        )

        self.display_response(
            summary
        )

    def summary_failed(self, error):

        self.summarise_button.config(
            state="normal",
            text="Summarise Notes"
        )

        self.feedback_label.config(
            text=f"Summary generation failed:\n{error}",
            fg="#FF7777"
        )


    def display_response(self, response):

        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        response_box = tk.Text(
            self.answers_frame,
            width=90,
            height=18,
            bg=self.theme.get("card"),
            fg=self.theme.get("text"),
            insertbackground="white",
            relief="flat",
            wrap="word",
            font=("Segoe UI", 11)
        )

        response_box.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        response_box.insert(
            "1.0",
            response
        )

        response_box.config(
            state="disabled"
        )


    def generate_quiz(self):

        selected = self.notes_list.curselection()

        if not selected:

            self.feedback_label.config(
                text="Select notes first.",
                fg=self.theme.get("secondary_text")
            )

            return

        try:

            number = int(
                self.quiz_count_var.get()
            )

        except (ValueError, tk.TclError):

            self.feedback_label.config(
                text="Enter a valid number of questions.",
                fg="#FF7777"
            )

            return

        if number < 3 or number > 30:

            self.feedback_label.config(
                text="Choose between 3 and 30 questions.",
                fg="#FF7777"
            )

            return

        notes = self.study_manager.load_notes()

        note = notes[selected[0]]

        try:

            text = self.note_reader.extract_text(
                note["path"]
            )

        except Exception as e:

            self.feedback_label.config(
                text=f"Could not read PDF:\n{e}",
                fg="#FF7777"
            )

            return

        if not text.strip():

            self.feedback_label.config(
                text="No readable text was found in this PDF.",
                fg="#FF7777"
            )

            return

        # -----------------------------------------
        # CLEAR THE PREVIOUS QUIZ
        # -----------------------------------------

        self.current_quiz = []

        self.current_question = 0

        self.score = 0

        self.user_answers = {}

        self.quiz_evaluations = {}

        self.review_question = 0

        self.answer_box = None

        # -----------------------------------------
        # CLEAR OLD ANSWERS / RESULTS
        # -----------------------------------------

        for widget in self.answers_frame.winfo_children():

            widget.destroy()

        self.previous_button.pack_forget()

        self.next_button.pack_forget()

        self.submit_button.pack_forget()

        self.review_button.pack_forget()

        # -----------------------------------------
        # SHOW GENERATING MESSAGE
        # -----------------------------------------

        self.question_label.config(
            text="Generating your new quiz...",
            fg=self.theme.get("text")
        )

        self.feedback_label.config(
            text=f"Phronesis is generating {number} new questions...",
            fg="#66DD88"
        )

        # -----------------------------------------
        # DISABLE BUTTONS
        # -----------------------------------------

        self.quiz_button.config(
            state="disabled",
            text="Generating..."
        )

        self.summarise_button.config(
            state="disabled"
        )

        # -----------------------------------------
        # GENERATE IN BACKGROUND
        # -----------------------------------------

        threading.Thread(
            target=self.quiz_worker,
            args=(text, number),
            daemon=True
        ).start()

    def quiz_worker(self, text, number):

        try:

            # -----------------------------------------
            # PREVIOUS QUESTIONS
            # -----------------------------------------

            previous_questions_text = "\n".join(
                f"- {question}"
                for question in self.previous_questions
            )

            quiz = self.ai.generate_quiz(
                text,
                number,
                previous_questions_text
            )

            self.frame.after(
                0,
                lambda:
                    self.load_quiz(quiz)
            )

        except Exception as e:

            error = str(e)

            print(
                "QUIZ GENERATION ERROR:",
                error
            )

            self.frame.after(
                0,
                lambda:
                    self.quiz_generation_failed(error)
            )

    def quiz_generation_failed(self, error):

        self.quiz_button.config(
            state="normal",
            text="Generate Quiz"
        )

        self.summarise_button.config(
            state="normal"
        )

        self.feedback_label.config(
            text=(
                "Quiz generation failed.\n\n"
                f"{error}"
            ),
            fg="#FF7777"
        )


    def load_quiz(self, quiz):


        self.quiz_button.config(
            state="normal",
            text="Generate Quiz"
        )

        self.summarise_button.config(
            state="normal"
        )

        try:

            new_quiz = json.loads(quiz)

            if not isinstance(new_quiz, list):

                raise ValueError(
                    "AI did not return a quiz list."
                )

            if not new_quiz:

                raise ValueError(
                    "AI returned an empty quiz."
                )


            for question in new_quiz:

                if "question" not in question:
                    raise ValueError(
                        "A quiz question is missing its question field."
                    )

                if "answer" not in question:
                    raise ValueError(
                        "A quiz question is missing its answer."
                    )

                if "type" not in question:
                    raise ValueError(
                        "A quiz question is missing its type."
                    )

                if "topic" not in question:
                    raise ValueError(
                        "A quiz question is missing its topic."
                    )

                if question["type"] == "multiple_choice":

                    if len(
                        question.get("options", [])
                    ) != 4:

                        raise ValueError(
                            "A multiple-choice question "
                            "must have exactly 4 options."
                        )

            self.current_quiz = new_quiz

            for question in new_quiz:

                question_text = question.get(
                    "question",
                    ""
                ).strip()

                if question_text:

                    if question_text not in self.previous_questions:

                        self.previous_questions.append(
                            question_text
                        )

            self.current_question = 0
            self.score = 0
            self.user_answers = {}
            self.quiz_evaluations = {}
            self.review_question = 0
            self.answer_box = None


            self.previous_button.config(
                command=self.previous_question,
                state="normal"
            )

            self.next_button.config(
                command=self.next_question,
                state="normal"
            )

            self.submit_button.config(
                command=self.submit_quiz,
                state="normal",
                text="Submit Quiz"
            )

            self.review_button.config(
                command=self.start_review,
                text="Review Answers"
            )

            self.question_label.config(
                text=""
            )

            self.feedback_label.config(
                text="Quiz ready.",
                fg=self.theme.get("secondary_text")
            )

            for widget in self.answers_frame.winfo_children():
                widget.destroy()

            self.previous_button.pack_forget()
            self.next_button.pack_forget()
            self.submit_button.pack_forget()
            self.review_button.pack_forget()


            self.show_question()

            self.canvas.yview_moveto(0)

        except Exception as e:

            self.current_quiz = []

            self.current_question = 0
            self.score = 0
            self.user_answers = {}
            self.quiz_evaluations = {}
            self.review_question = 0

            self.feedback_label.config(
                text=f"Could not load quiz:\n{e}",
                fg="#FF7777"
            )


    def show_question(self):

        if not self.current_quiz:
            return

        self.feedback_label.config(
            text="",
            fg=self.theme.get("secondary_text")
        )

        question = self.current_quiz[
            self.current_question
        ]

        self.question_label.config(
            text=(
                f"Question "
                f"{self.current_question + 1}/"
                f"{len(self.current_quiz)}"
                f"\n\n"
                f"{question['question']}"
            )
        )

        self.answer_var.set("")

        for widget in self.answers_frame.winfo_children():

            widget.destroy()

        self.answer_box = None

        if question["type"] == "multiple_choice":

            self.answer_var = tk.StringVar()

            saved = self.user_answers.get(
                self.current_question
            )

            if saved:
                self.answer_var.set(saved)

            for option in question["options"]:

                rb = tk.Radiobutton(
                    self.answers_frame,
                    text=option,
                    variable=self.answer_var,
                    value=option,
                    bg=self.theme.get("background"),
                    fg=self.theme.get("text"),
                    selectcolor="#5B2EFF",
                    activebackground="#202020",
                    activeforeground="white",
                    anchor="w",
                    justify="left",
                    wraplength=750
                )

                rb.pack(
                    fill="x",
                    pady=5,
                    padx=20
                )

        elif question["type"] == "short_answer":

            self.answer_box = tk.Text(
                self.answers_frame,
                width=90,
                height=5,
                bg=self.theme.get("card"),
                fg=self.theme.get("text"),
                insertbackground="white",
                relief="flat",
                wrap="word"
            )

            self.answer_box.pack(
                pady=10,
                padx=20,
                fill="x"
            )

            self.answer_box.bind(
                "<KeyRelease>",
                self.auto_resize_answer_box
            )

            saved = self.user_answers.get(
                self.current_question
            )

            if saved:

                self.answer_box.insert(
                    "1.0",
                    saved
                )

        self.update_question_navigation()


    def update_question_navigation(self):

        self.previous_button.pack_forget()

        self.next_button.pack_forget()

        self.submit_button.pack_forget()

        if self.current_question > 0:

            self.previous_button.pack(
                side="left",
                padx=10
            )

        if self.current_question < len(
            self.current_quiz
        ) - 1:

            self.next_button.pack(
                side="right",
                padx=10
            )

        elif self.current_quiz:

            self.submit_button.pack(
                side="right",
                padx=10
            )

    def save_current_answer(self):

        if not self.current_quiz:
            return

        question = self.current_quiz[
            self.current_question
        ]

        if question["type"] == "multiple_choice":

            self.user_answers[
                self.current_question
            ] = self.answer_var.get()

        elif self.answer_box:

            self.user_answers[
                self.current_question
            ] = self.answer_box.get(
                "1.0",
                tk.END
            ).strip()

    def previous_question(self):

        self.save_current_answer()

        if self.current_question > 0:

            self.current_question -= 1

            self.show_question()

    def next_question(self):

        self.save_current_answer()

        if self.current_question < len(
            self.current_quiz
        ) - 1:

            self.current_question += 1

            self.show_question()


    def submit_quiz(self):

        self.save_current_answer()

        self.previous_button.pack_forget()

        self.next_button.pack_forget()

        self.submit_button.config(
            state="disabled",
            text="Evaluating..."
        )

        self.question_label.config(
            text="Evaluating your answers..."
        )

        self.feedback_label.config(
            text="Phronesis is checking your answers..."
        )

        threading.Thread(
            target=self.evaluate_quiz_worker,
            daemon=True
        ).start()

    def evaluate_quiz_worker(self):

        score = 0

        evaluations = {}

        for index, question in enumerate(
            self.current_quiz
        ):

            user_answer = self.user_answers.get(
                index,
                ""
            )


            if question.get(
                "type"
            ) == "multiple_choice":

                correct = (
                    user_answer.strip().lower()
                    ==
                    question["answer"].strip().lower()
                )

                if correct:
                    score += 1

                evaluations[index] = {

                    "result":
                        "correct"
                        if correct
                        else
                        "incorrect",


                }

            else:

                try:

                    evaluation = self.ai.evaluate_short_answer(

                        question["question"],

                        question["answer"],

                        user_answer

                    )

                    evaluations[index] = evaluation

                    if evaluation.get(
                        "result"
                    ) == "correct":

                        score += 1

                except Exception as e:

                    print(
                        f"SHORT ANSWER EVALUATION ERROR "
                        f"FOR QUESTION {index + 1}:"
                    )

                    print(e)

                    evaluations[index] = {

                        "result": "incorrect",

                        "feedback":
                            "Phronesis could not evaluate "
                            "this answer."
                    }

        self.frame.after(
            0,
            lambda:
                self.finish_quiz(
                    score,
                    evaluations
                )
        )

    def finish_quiz(
        self,
        score,
        evaluations
    ):

        self.score = score

        self.quiz_evaluations = evaluations

        self.progress_manager.save_quiz_result(

            self.current_quiz,

            self.user_answers,

            score,

            evaluations

        )

        percentage = round(
            (
                score
                /
                len(self.current_quiz)
            ) * 100,
            2
        )

        self.question_label.config(
            text=(
                "Quiz Complete!\n\n"
                f"Score: "
                f"{score}/"
                f"{len(self.current_quiz)}\n"
                f"Accuracy: {percentage}%"
            )
        )

        self.feedback_label.config(
            text=(
                "Phronesis has evaluated your answers. "
                "Review the quiz to see what you got right "
                "and what needs more work."
            ),
            fg=self.theme.get("secondary_text")
        )

        for widget in self.answers_frame.winfo_children():

            widget.destroy()

        self.previous_button.pack_forget()

        self.next_button.pack_forget()

        self.submit_button.pack_forget()

        self.submit_button.config(
            state="normal",
            text="Submit Quiz"
        )

        self.review_button.pack(
            pady=10
        )


    def start_review(self):

        if not self.current_quiz:
            return

        self.review_question = 0

        self.review_button.pack_forget()

        self.show_review_question()

    def show_review_question(self):

        question = self.current_quiz[
            self.review_question
        ]

        user_answer = self.user_answers.get(
            self.review_question,
            "No answer"
        )

        correct_answer = question[
            "answer"
        ]

        evaluation = self.quiz_evaluations.get(
            self.review_question
        )

        if not evaluation:

            evaluation = {

                "result": "incorrect",

                "feedback":
                    "No evaluation was available."
            }

        result = evaluation.get(
            "result",
            "incorrect"
        )

        feedback = evaluation.get(
            "feedback",
            ""
        )

        if result == "correct":

            review_text = (
                "✓ Correct!\n\n"
                f"Your answer:\n"
                f"{user_answer}\n"
                f"{feedback}"
            )

        elif result == "partially_correct":

            review_text = (
                "△ Partially correct.\n\n"
                f"Your answer:\n"
                f"{user_answer}\n"
                f"{feedback}\n"
                f"Correct answer:\n"
                f"{correct_answer}"
            )

        else:

            review_text = (
                "✗ Incorrect.\n\n"
                f"Your answer:\n"
                f"{user_answer}\n"
                f"{feedback}\n"
                f"Correct answer:\n"
                f"{correct_answer}"
            )

        explanation = question.get(
            "explanation",
            ""
        )

        if explanation:

            review_text += (
                "\n\nExplanation:\n"
                f"{explanation}"
            )

        self.question_label.config(
            text=(
                "Review "
                f"{self.review_question + 1}/"
                f"{len(self.current_quiz)}"
                "\n\n"
                f"{question['question']}"
            )
        )

        self.feedback_label.config(
            text=review_text,
            fg=self.theme.get("secondary_text")
        )

        for widget in self.answers_frame.winfo_children():

            widget.destroy()

        self.previous_button.pack_forget()

        self.next_button.pack_forget()

        self.submit_button.pack_forget()

        if self.review_question > 0:

            self.previous_button.config(
                command=self.previous_review
            )

            self.previous_button.pack(
                side="left",
                padx=10
            )

        if self.review_question < len(
            self.current_quiz
        ) - 1:

            self.next_button.config(
                command=self.next_review
            )

            self.next_button.pack(
                side="right",
                padx=10
            )

        else:

            self.review_button.config(
                text="Back to Results",
                command=self.show_results
            )

            self.review_button.pack(
                pady=10
            )

    def next_review(self):

        if self.review_question < len(
            self.current_quiz
        ) - 1:

            self.review_question += 1

            self.show_review_question()

    def previous_review(self):

        if self.review_question > 0:

            self.review_question -= 1

            self.show_review_question()

    def show_results(self):

        self.question_label.config(
            text=(
                "Quiz Complete\n\n"
                f"Score: "
                f"{self.score}/"
                f"{len(self.current_quiz)}"
            )
        )

        percentage = round(
            (
                self.score
                /
                len(self.current_quiz)
            ) * 100,
            2
        )

        self.feedback_label.config(
            text=f"Accuracy: {percentage}%"
        )

        for widget in self.answers_frame.winfo_children():

            widget.destroy()

        self.previous_button.pack_forget()

        self.next_button.pack_forget()

        self.submit_button.pack_forget()

        self.review_button.config(
            text="Review Answers",
            command=self.start_review
        )

        self.review_button.pack(
            pady=10
        )

    def auto_resize_answer_box(
        self,
        event=None
    ):

        if not self.answer_box:
            return

        lines = int(
            self.answer_box.index(
                "end-1c"
            ).split(".")[0]
        )

        lines = max(
            3,
            min(
                lines,
                15
            )
        )

        self.answer_box.configure(
            height=lines
        )