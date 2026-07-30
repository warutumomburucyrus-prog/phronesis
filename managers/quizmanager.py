import json
import os


class QuizManager:

    def __init__(self):

        self.quiz_file = "data/quizzes.json"

        if not os.path.exists(self.quiz_file):

            with open(
                self.quiz_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )


    def load_quizzes(self):

        with open(
            self.quiz_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)



    def save_quizzes(self, quizzes):

        with open(
            self.quiz_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                quizzes,
                file,
                indent=4
            )



    def add_quiz(self, quiz):

        quizzes = self.load_quizzes()

        quizzes.append(
            quiz
        )

        self.save_quizzes(
            quizzes
        )