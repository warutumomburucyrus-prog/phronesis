import json
import os

from datetime import datetime
from datetime import datetime, timedelta


class ScheduleManager:

    def __init__(self):

        self.file_path = os.path.join(
            "data",
            "schedule.json"
        )


    def load_today_classes(self):

        if not os.path.exists(self.file_path):

            return []

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            if not content.strip():

                return []

            schedule = json.loads(content)

            today = datetime.now().strftime("%A")

            print("TODAY:", today)
            print("SCHEDULE DAYS:", [x["day"] for x in schedule])


            classes = []

            for item in schedule:

                if item["day"] == today:

                    classes.append(item)

            return classes

        except Exception as e:

            print("Schedule loading error:", e)

            return []
        
    def load_week_schedule(self):

        if not os.path.exists(self.file_path):

            return {}


        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                schedule = json.load(file)


            week = {}


            for item in schedule:

                day = item["day"]


                if day not in week:

                    week[day] = []


                week[day].append(item)


            return week


        except Exception as e:

            print(
                "Weekly schedule loading error:",
                e
            )

            return {}
        
    def load_tomorrow_classes(self):

        tomorrow = (
            datetime.now() +
            timedelta(days=1)
        ).strftime("%A")

        week = self.load_week_schedule()

        return week.get(tomorrow, [])