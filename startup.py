import json
from managers.timetableparserai import TimetableAI


class Startup:

    def __init__(self, splash):

        self.splash = splash

    def run(self):

        self.splash.set_status("Loading profile...")
        self.load_json("Data/user_profile.json")

        self.splash.set_status("Loading courses...")
        self.load_json("Data/courses.json")

        self.splash.set_status("Loading schedule...")
        self.load_json("Data/schedule.json")

        self.splash.set_status("Starting AI...")
        TimetableAI()

    def load_json(self, path):

        try:

            with open(path, "r", encoding="utf-8") as file:
                json.load(file)

        except Exception:
            pass