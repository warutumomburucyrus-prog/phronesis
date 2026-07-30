import os
import json
import ast

from google import genai
from dotenv import load_dotenv


load_dotenv()


class TimetableAI:


    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )



    def load_profile(self):

        try:

            with open(
                "Data/user_profile.json",
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception:

            return {}



    def save_schedule(self, schedule):

        print("TYPE:", type(schedule))
        print("DATA:")
        print(schedule)

        os.makedirs(
            "data",
            exist_ok=True
        )

        path = os.path.abspath(
            "data/schedule.json"
        )

        print("Saving to: ")
        print(path)

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                schedule,
                file,
                indent=4
            )

        print("schedule.json saved")

        # Test read back

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:
            
            content = file.read()

            print("File now contains: ")
            print(content)



    def clean_gemini_response(self, text):

        text = text.strip()


        # remove markdown

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )


        text = text.strip()


        # Find only the list part

        start = text.find("[")

        end = text.rfind("]")


        if start != -1 and end != -1:

            text = text[start:end+1]



        try:

            # Try normal JSON first

            return json.loads(text)



        except Exception:


            try:

                # Convert python list with single quotes

                return ast.literal_eval(text)


            except Exception as e:

                print(
                    "Failed converting Gemini response"
                )

                print(e)

                print(
                    "Gemini returned:"
                )

                print(text)

                return []



    def convert_to_schedule(self, timetable_text):


        profile = self.load_profile()



        prompt = f"""

You are a university timetable parser.

Extract ONLY classes belonging to this student.

Student profile:

University:
{profile.get("university")}

Program:
{profile.get("program")}

Year:
{profile.get("year")}

Semester:
{profile.get("semester")}


Ignore other programs.

IMPORTANT EXTRACTION RULES:

- Scan the ENTIRE timetable before answering.
- Do not stop after finding some classes.
- Extract every class belonging to the student.
- Check every day from Monday to Friday.
- If a day contains classes, it MUST appear in the output.
- Preserve duplicate course codes if they occur on different days.
- Never merge classes.
- Never omit afternoon classes.

IMPORTANT TIMETABLE EXTRACTION RULES:

1. The timetable is a table. Read the entire table before answering.

2. Extract every class belonging to the student.

3. Preserve the exact day of each class.
   Do not assign classes to Monday unless the timetable says Monday.

4. The timetable can contain:
   Monday
   Tuesday
   Wednesday
   Thursday
   Friday

5. Check every day column before returning the answer.

6. Do not stop after finding some classes.

7. Do not merge multiple classes together.

8. If the same course appears on different days, keep each class entry separately.

9. Verify that the returned JSON contains all detected days.


Return ONLY a JSON list.

No explanations.
No markdown.

Format:

[
{{
"course_code":"CIT 3117",
"day":"Monday",
"start_time":"8:00 AM",
"end_time":"11:00 AM",
"venue":"TB02",
"lecturer":"T. ANONDO"
}}
]


Timetable:

{timetable_text}

"""


        try:


            print("Sending timetable to Gemini...")

            print(
                "Text length:",
                len(timetable_text)
            )

            print(timetable_text)

            response = self.client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )


            print("Gemini responded")

            print(response.text)

            schedule = self.clean_gemini_response(
                response.text
            )


            print(
                "Classes extracted:",
                len(schedule)
            )

            days = {
                item.get("day")
                for item in schedule
            }

            print(
                "Days detected:",
                days
            )

            if len(days) < 3:

                print(
                    "Warning: timetable may be incomplete"
                )

            if len(schedule) == 0:

                print(
                    "No classes found"
                )

                return []



            self.save_schedule(
                schedule
            )


            return schedule



        except Exception as e:


            print(
                "Gemini error:"
            )

            print(e)

            return []