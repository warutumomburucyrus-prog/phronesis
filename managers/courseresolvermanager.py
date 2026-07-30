import json
import os

from managers.aimanager import AIManager
from managers.profilemanager import ProfileManager


class CourseResolverManager:

    def __init__(self):

        self.ai = AIManager()
        self.profile = ProfileManager()
        self.cache_path = "data/coursecache.json"

    def _clean_response(self, response):

        response = response.strip()

        response = response.replace(
            "'''json",
            ""
        )

        response = response.replace(
            "'''",
            ""
        )

        return response.strip()
    
    def load_cache(self):

        if not os.path.exists(self.cache_path):
            return {}
        
        with open(
            self.cache_path,
            "r",
            encoding="utf-8"
        )as file:
            
            return json.load(file)
        
    def save_cache(self, cache):

        with open(
            self.cache_path,
            "w",
            encoding="utf-8"
        )as file:
            
            json.dump(
                cache,
                file,
                indent=4
            )

    def resolve(self, course_codes):

        info = self.profile.get_academic_info()

        cache = self.load_cache()

        university = info["university"]
        programme = info["programme"]

        missing_codes = [

            code

            for code in course_codes

            if code not in cache
        ]

        if not missing_codes:

            return {

                code: cache[code]

                for code in course_codes
            }

        prompt = f"""
You are an expert on university curricula.

University:
{university}

Programme:
{programme}

Return ONLY valid JSON.

For every course code below return the official course title.

Example:

{{
    "CIT 3200": "Object Oriented Programming II",
    "CCS 3201": "Computer Networks"
}}

Course Codes:

{json.dumps(missing_codes, indent=2)}
"""

        response = self.ai.generate(prompt)

        print("\nGemini response:")
        print(response)

        if response.startswith("Gemini Error:"):
            return {}

        response = self._clean_response(response)

        try:

            resolved = json.loads(response)

            print("\nResolved dictionary:")
            print(resolved)
            
            cache.update(resolved)

            self.save_cache(cache)

            return {

                code: cache[code]

                for code in course_codes
            }

        except Exception:

            print("Gemini returned invalid JSON:")
            print(response)

            return {}