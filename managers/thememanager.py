import json
import os


class ThemeManager:

    
    current_theme ="dark"

    SETTINGS_FILE = "data/settings.json"

    THEMES = {

        "dark": {

            "background": "#202020",
            "sidebar": "#171717",
            "card": "#242424",

            "statusbar": "#2A2A2A",

            "text": "#FFFFFF",
            "secondary_text": "#AAAAAA",

            "accent": "#5B2EFF",

            "button": "#303030",
            "button_hover": "#404040",

            "icon": (255, 255, 255)

        },

        "light": {

            "background": "#F4F4F4",
            "sidebar": "#E8E8E8",
            "card": "#FFFFFF",

            "statusbar": "#FFFFFF",

            "text": "#202020",
            "secondary_text": "#666666",

            "accent": "#5B2EFF",

            "button": "#DDDDDD",
            "button_hover": "#CCCCCC",

            "icon": (32, 32, 32)

        }

    }

    
    def __init__(self):

        self.load()


    def load(self):

        if not os.path.exists(self.SETTINGS_FILE):

            self.save()
            return

        try:

            with open(self.SETTINGS_FILE, "r") as file:

                data = json.load(file)

                ThemeManager.current_theme = data.get(
                    "theme",
                    "dark"
                )

        except:

            ThemeManager.current_theme = "dark"


    def save(self):

        os.makedirs(
            os.path.dirname(self.SETTINGS_FILE),
            exist_ok=True
        )

        with open(self.SETTINGS_FILE, "w") as file:

            json.dump(
                {
                    "theme": ThemeManager.current_theme
                },
                file,
                indent=4
            )


    def set_theme(self, theme):

        if theme in self.THEMES:

            ThemeManager.current_theme = theme

            self.save()


    def get(self, key):

        return self.THEMES[ThemeManager.current_theme][key]