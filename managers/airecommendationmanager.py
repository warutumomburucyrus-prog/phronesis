from managers.progressmanager import ProgressManager

class AIRecommendationManager:

    def __init__(
        self,
        course_manager,
        assignment_manager,
        schedule_manager
    ):

        self.course_manager = course_manager
        self.assignment_manager = assignment_manager
        self.schedule_manager = schedule_manager
        self.progress_manager = ProgressManager()


    def get_recommendation(self):

        recommendations = []

        progress = self.progress_manager.load_progress()

        topic_performance = {}

        for quiz in progress:

            for question in quiz.get("questions", []):

                topic = question.get(
                    "topic",
                    "Unknown"
                )

                if topic == "Unknown":
                    continue


                if topic not in topic_performance:

                    topic_performance[topic] = {
                        "correct": 0,
                        "total": 0
                    }


                topic_performance[topic]["total"] += 1


                if question.get("correct", False):

                    topic_performance[topic]["correct"] += 1


        weakest_topic = None
        weakest_percentage = 101


        for topic, performance in topic_performance.items():

            total = performance["total"]

            correct = performance["correct"]


            if total == 0:
                continue


            percentage = (
                correct / total
            ) * 100


            if percentage < weakest_percentage:

                weakest_percentage = percentage
                weakest_topic = topic


        if weakest_topic is not None:

            if weakest_percentage < 60:

                recommendations.append({

                    "priority": 120,

                    "title": "Study Priority",

                    "body":
                        f"You're struggling with "
                        f"{weakest_topic}.\n\n"
                        f"Your quiz accuracy on this topic is "
                        f"{weakest_percentage:.0f}%.\n\n"
                        f"Review your notes and practice "
                        f"{weakest_topic} before moving on."

                })


            elif weakest_percentage < 75:

                recommendations.append({

                    "priority": 90,

                    "title": "📖 Review Needed",

                    "body":
                        f"You're making progress with "
                        f"{weakest_topic}, but there's room "
                        f"for improvement.\n\n"
                        f"Your quiz accuracy is "
                        f"{weakest_percentage:.0f}%.\n\n"
                        f"Consider reviewing this topic "
                        f"and taking another quiz."

                })

        assignments = (
            self.assignment_manager.load_assignments()
        )


        pending = [

            assignment

            for assignment in assignments

            if not assignment.get(
                "completed",
                False
            )

        ]


        if pending:

            recommendations.append({

                "priority": 100,

                "title": "📋 Priority",

                "body":
                    f"You have "
                    f"{len(pending)} pending assignments.\n\n"
                    f"Start with "
                    f"'{pending[0].get('topic', 'assignment')}' "
                    f"for "
                    f"{pending[0].get('course', 'your course')}."

            })

        tomorrow = (
            self.schedule_manager.load_tomorrow_classes()
        )


        if tomorrow:

            recommendations.append({

                "priority": 80,

                "title": "📚 Tomorrow",

                "body":
                    f"You have "
                    f"{tomorrow[0]['course_code']} "
                    f"tomorrow."

            })


        courses = self.course_manager.get_courses()


        if courses:

            weakest_course = min(

                courses,

                key=lambda course:
                    course.get(
                        "progress",
                        0
                    )

            )


            recommendations.append({

                "priority": 50,

                "title": "📈 Course Progress",

                "body":
                    f"{weakest_course['course_code']} "
                    f"is only "
                    f"{weakest_course.get('progress', 0)}% "
                    f"complete."

            })

        if recommendations:

            recommendations.sort(

                key=lambda recommendation:
                    recommendation["priority"],

                reverse=True

            )


            best = recommendations[0]


            return (

                best["title"],

                best["body"]

            )


        return (

            "Great Job",

            "Everything is on schedule."

        )
