import json
import os


class AssignmentManager:

    def __init__(self):

        self.path = "Data/assignments.json"


    def load_assignments(self):

        if not os.path.exists(self.path):
            return []

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    def save_assignments(self, assignments):

        os.makedirs(
            "Data",
            exist_ok=True
        )

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                assignments,
                file,
                indent=4
            )


    def add_assignment(
        self,
        assignment
    ):

        assignments = self.load_assignments()

        assignments.append(
            assignment
        )

        self.save_assignments(
            assignments
        )
    
    def complete_assignments(self, assignment_title):

        assignments = self.load_assignments()

        for assignment in assignments:

            if assignment.get("topic") == assignment_title:

                assignment["completed"] = True

        self.save_assignments(assignments)

    def get_completed_assignments(self):

        assignments = self.load_assignments()

        return [
            assignment 
            for assignment in assignments
            if assignment.get("completed", False)
        ]
    def get_completed_count(self):

        return sum(
            1
            for assignment in self.load_assignments()
            if assignment.get("completed", False)
        )
    
    def get_pending_count(self):

        return sum(
            1
            for assignment in self.load_assignments()
            if not assignment.get("completed", False)
        )
    
    def get_completion_percentage(self):

        assignments = self.load_assignments()

        if not assignments:
            return 0
        
        completed = self.get_completed_count()

        return int(((completed / len(assignments))) * 100)