import json
import os

from jproperties import Properties

from VegansDeluxe.core.Translator.Locale import Locale


class Translator:
    def __init__(self, default_locale: str):
        self.default_locale = default_locale
        self.locales: dict[str: Locale] = dict()

    def get_string(self, key: str, code: str = ""):
        if not code:
            code = self.default_locale
        return self.get_locale(code).get_string(key)

    def get_locale(self, code: str) -> Locale:
        return self.locales.get(code)

    def create_locale(self, code: str) -> Locale:
        locale = Locale(code)
        self.locales.update({code: locale})
        return locale

    def update_locale(self, code: str, data: dict):
        locale = self.get_locale(code)
        if not locale:
            locale = self.create_locale(code)

        locale.add_data(data)

    def load_folder(self, folder_path: str):
        files = os.listdir(folder_path)

        for file in files:
            if file.endswith(".json"):
                code = file.split(".json", 1)[0]
                self.load_json(code, f"{folder_path}/{file}")
            elif file.endswith(".properties"):
                code = file.split(".json", 1)[0].split("locale_", 1)[1]
                self.load_properties(code, f"{folder_path}/{file}")

    def load_properties(self, code: str, filepath: str):
        properties = Properties()
        with open(filepath, "r", encoding="utf-8") as file:
            properties.load(file.read(), encoding="utf-8")

        # Access values
        data = {key: value.data for key, value in properties.items()}
        print(data)
        self.update_locale(code, data)

    def load_json(self, code: str, filepath: str):
        file = open(filepath, "r", encoding="utf-8")
        try:
            data = json.load(file)
        except:
            raise Exception(f"Fatal error while loading {filepath}.")

        self.update_locale(code, data)


translator = Translator('en')
