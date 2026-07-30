import json
import os


class ProfileManager:

    def __init__(self):

        self.path = "Data/user_profile.json"


    def load_profile(self):

        if not os.path.exists(self.path):
            return {}

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)



    def get_name(self):

        profile = self.load_profile()

        return profile.get(
            "name",
            "Student"
        )
    
    def get_university(self):

        profile = self.load_profile()

        return profile.get(
            "university",
            ""
        )
    
    def get_programme(self):

        profile = self.load_profile()

        return profile.get(
            "programme",
            ""
        )
    
    def get_academic_info(self):

        profile = self.load_profile()

        return {

            "university": profile.get(
                "university",
                ""
            )
        ,

        "programme": profile.get(
            "programme",
            ""
        )}