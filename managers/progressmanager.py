import json
import os
from datetime import datetime

from managers.coursemanager import CourseManager


class ProgressManager:

    def __init__(self):

        self.file = "Data/progress.json"

        self.course_manager = CourseManager()


    def load_progress(self):

        if not os.path.exists(self.file):

            return []

        with open(
            self.file,
            "r"
        ) as f:

            return json.load(f)


    def save_quiz_result(
        self,
        quiz,
        user_answers,
        score,
        evaluations=None
    ):

        progress = self.load_progress()

        if evaluations is None:
            evaluations = {}

        result = {

            "date": str(datetime.now()),

            "total_questions": len(quiz),

            "score": score,

            "percentage": round(
                (score / len(quiz)) * 100,
                2
            ),

            "questions": []

        }

        for index, question in enumerate(quiz):

            user_answer = user_answers.get(
                index,
                ""
            )

            question_result = {

                "question": question["question"],

                "topic": question.get(
                    "topic",
                    "Unknown"
                ),

                "correct_answer": question["answer"],

                "user_answer": user_answer,

                "type": question.get(
                    "type",
                    "multiple_choice"
                )

            }

            # --------------------------------
            # MULTIPLE CHOICE
            # --------------------------------

            if question.get("type") == "multiple_choice":

                correct = (
                    user_answer.strip().lower()
                    ==
                    question["answer"].strip().lower()
                )

                question_result["correct"] = correct

                question_result["evaluation"] = {

                    "result":
                        "correct"
                        if correct
                        else "incorrect",

                    "feedback":
                        ""
                }

            # --------------------------------
            # SHORT ANSWER
            # --------------------------------

            else:

                evaluation = evaluations.get(
                    index
                )

                if evaluation:

                    question_result["correct"] = (
                        evaluation["result"]
                        == "correct"
                    )

                    question_result["evaluation"] = evaluation

                else:

                    question_result["correct"] = False

                    question_result["evaluation"] = {

                        "result": "incorrect",

                        "feedback":
                            "Phronesis could not evaluate this answer."
                    }

            result["questions"].append(
                question_result
            )

        progress.append(result)

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                progress,
                f,
                indent=4
            )
    
    def get_recommendation(self):

        progress = self.load_progress()

        if not progress:

            return (
                "Complete your first quiz to receive AI study recommendations."
            )


        # Look across all answered questions.

        topic_results = {}


        for quiz in progress:

            for question in quiz.get(
                "questions",
                []
            ):

                topic = question.get(
                    "topic",
                    "Unknown"
                )

                if not topic:
                    continue

                if topic.lower() == "unknown":
                    continue


                if topic not in topic_results:

                    topic_results[topic] = {

                        "correct": 0,

                        "total": 0

                    }


                topic_results[topic]["total"] += 1


                if question.get(
                    "correct",
                    False
                ):

                    topic_results[topic]["correct"] += 1


        if not topic_results:

            return (
                "Complete a quiz to receive study recommendations."
            )


        # Find the weakest topic.

        weakest_topic = min(

            topic_results,

            key=lambda topic:
                topic_results[topic]["correct"]
                /
                topic_results[topic]["total"]

        )


        weakest = topic_results[
            weakest_topic
        ]


        accuracy = round(

            (
                weakest["correct"]
                /
                weakest["total"]
            ) * 100,

            1

        )


        if accuracy < 50:

            return (

                f"Priority: Review {weakest_topic}. "
                f"You're currently scoring only {accuracy}% "
                f"on questions about this topic. "
                f"Focus your next study session on {weakest_topic} "
                f"before taking another quiz."

            )


        if accuracy < 70:

            return (

                f"Review {weakest_topic}. "
                f"You're showing some difficulty with this topic, "
                f"currently scoring {accuracy}%. "
                f"Review your notes and retry some questions."

            )


        if accuracy < 85:

            return (

                f"Keep practicing {weakest_topic}. "
                f"You're currently at {accuracy}% accuracy. "
                f"A little more practice should strengthen your understanding."

            )


        return (

            f"Great work. Your weakest tracked topic is "
            f"{weakest_topic}, but you're still scoring "
            f"{accuracy}% on it. You're ready for more challenging questions."

        )


  
    def get_dashboard_progress(self):

        progress = self.load_progress()
        courses = self.course_manager.load_courses()

        dashboard = []

        for course in courses:

            topics = course.get("topics", [])

            if not topics:
                continue

            encountered = []

            # ----------------------------------------
            # CHECK WHICH COURSE TOPICS HAVE APPEARED
            # ----------------------------------------

            for topic in topics:

                topic_words = set(
                    topic.lower()
                    .replace(",", "")
                    .replace(":", "")
                    .replace("(", "")
                    .replace(")", "")
                    .split()
                )

                found = False

                for quiz in progress:

                    for question in quiz.get("questions", []):

                        quiz_topic = question.get("topic", "")

                        if not quiz_topic:
                            continue

                        quiz_words = set(
                            quiz_topic.lower()
                            .replace(",", "")
                            .replace(":", "")
                            .replace("(", "")
                            .replace(")", "")
                            .split()
                        )

                        # Exact match
                        if topic.lower() == quiz_topic.lower():
                            found = True
                            break

                        # Match when the quiz topic is contained
                        # within the actual course topic
                        if (
                            quiz_topic.lower() in topic.lower()
                            or topic.lower() in quiz_topic.lower()
                        ):
                            found = True
                            break

                        # Match using meaningful shared words
                        meaningful_topic_words = {
                            word for word in topic_words
                            if len(word) > 3
                        }

                        meaningful_quiz_words = {
                            word for word in quiz_words
                            if len(word) > 3
                        }

                        shared_words = (
                            meaningful_topic_words
                            & meaningful_quiz_words
                        )

                        if len(shared_words) >= 2:
                            found = True
                            break

                    if found:
                        break

                if found:
                    encountered.append(topic)

            # ----------------------------------------
            # FAMILIARITY
            # ----------------------------------------

            familiarity = int(
                (
                    len(encountered)
                    /
                    len(topics)
                ) * 100
            )

            # ----------------------------------------
            # DASHBOARD MESSAGE
            # ----------------------------------------

            if familiarity == 0:

                message = (
                    f"You haven't explored "
                    f"{course['name']} yet."
                )

            elif familiarity < 25:

                next_topic = next(
                    (
                        t
                        for t in topics
                        if t not in encountered
                    ),
                    None
                )

                message = (
                    f"You've begun exploring "
                    f"{course['name']}. "
                    f"Next, learn {next_topic}."
                )

            elif familiarity < 50:

                next_topic = next(
                    (
                        t
                        for t in topics
                        if t not in encountered
                    ),
                    None
                )

                message = (
                    f"You have built a foundation in "
                    f"{course['name']}. "
                    f"Next, study {next_topic}."
                )

            elif familiarity < 75:

                next_topic = next(
                    (
                        t
                        for t in topics
                        if t not in encountered
                    ),
                    None
                )

                message = (
                    f"You're becoming comfortable with "
                    f"{course['name']}. "
                    f"Next, tackle {next_topic}."
                )

            else:

                message = (
                    f"You have strong familiarity with "
                    f"{course['name']}."
                )

            dashboard.append({

                "course": course["name"],

                "message": message,

                "familiarity": familiarity

            })

        dashboard.sort(
            key=lambda x: x["familiarity"],
            reverse=True
        )

        return dashboard


