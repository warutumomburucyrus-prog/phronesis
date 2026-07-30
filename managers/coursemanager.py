import json
import os


class CourseManager:

    def __init__(self):

        self.file_path = os.path.join(
            "data",
            "courses.json"
        )

        self.create_file_if_missing()



    def create_file_if_missing(self):

        if not os.path.exists(self.file_path):

            with open(self.file_path, "w") as file:

                json.dump([], file)



    def load_courses(self):

        with open(
            self.file_path,
            "r"
        ) as file:

            return json.load(file)



    def save_courses(
        self,
        courses
    ):

        with open(
            self.file_path,
            "w"
        ) as file:

            json.dump(
                courses,
                file,
                indent=4
            )



    def add_course(
        self,
        course_code,
        name,
        lecturer,
        credits,
        exam_date
    ):

        courses = self.load_courses()


        courses.append({

            "course_code": course_code,

            "name": name,

            "lecturer": lecturer,

            "credits": credits,

            "exam_date": exam_date,

            "progress": 0,

            "topics": [],

            "assignments": [],

            "notes": []

        })


        self.save_courses(
            courses
        )



    def delete_course(
        self,
        course_code
    ):

        courses = self.load_courses()


        courses = [

            course

            for course in courses

            if course["course_code"] != course_code

        ]


        self.save_courses(
            courses
        )



    def update_course(
        self,
        old_name,
        updated_course
    ):

        courses = self.load_courses()


        for course in courses:

            if course["name"] == old_name:

                course.update(
                    updated_course
                )


        self.save_courses(
            courses
        )

    def get_course_name(self, course_code):

        courses = self.load_courses()

        for course in courses:

            if course.get("course_code") == course_code:

                return course.get("name", course_code)

        return course_code

    def get_courses(self):

        return self.load_courses()
    
    def auto_add_from_schedule(self, schedule):

        courses = self.load_courses()

        existing_codes = {
            course["course_code"]
            for course in courses
            if "course_code" in course
        }

        added = 0

        for lesson in schedule:

            code = lesson["course_code"]

            if code not in existing_codes:

                courses.append({

                    "course_code": code,

                    "name": "",

                    "lecturer": lesson.get("lecturer", ""),

                    "credits": "",

                    "exam_date": "",

                    "progress": 0,

                    "topics": [],

                    "assignments": [],

                    "notes": []
                })

                existing_codes.add(code)

                added += 1

        self.save_courses(courses)

        return added
    
    def get_incomplete_courses(self):

        courses = self.load_courses()

        incomplete = []

        for course in courses:

            if (
                course.get("name") == ""
                or course.get("credits") == ""
                or course.get("exam_date") == ""
            ):

                incomplete.append(course)


        return incomplete
    
    def update_course_by_code(
            self,
            code,
            updates
        ):

        courses = self.load_courses()


        for course in courses:

            if course["course_code"] == code:

                course.update(
                    updates
                )


        self.save_courses(
            courses
        )
    
    def get_incomplete_courses(self):

        courses = self.load_courses()

        incomplete = []

        for course in courses:

            if(
                course.get("name") == ""
                or course.get("credits") == ""
                or course.get("exam_date")  == ""
            ):
                
                incomplete.append(course)

        return incomplete
    
    def update_course_names(self, resolved_names):

        courses = self.load_courses()

        for course in courses:

            code = course.get(
                "course_code"
            )

            if code in resolved_names:

                course["name"] = resolved_names[code]

        self.save_courses(
            courses
        )