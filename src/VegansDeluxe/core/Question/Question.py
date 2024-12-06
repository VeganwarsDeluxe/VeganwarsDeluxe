from typing import Optional
from uuid import uuid4

from VegansDeluxe.core.Question.Choice import Choice
from VegansDeluxe.core.Translator.LocalizedString import LocalizedString


class Question:
    def __init__(self, text: str | LocalizedString):
        self.id: str = str(uuid4().hex)[:6]
        self.text: str | LocalizedString = text
        self.__choices: list[Choice] = []

    @property
    def choices(self):
        return self.__choices

    def get_choice(self, choice_id: str) -> Optional[Choice]:
        _ = [choice for choice in self.__choices if choice.id == choice_id]
        if _:
            return _[0]

    def add_choice(self, choice: Choice):
        choice.question_id = self.id
        self.__choices.append(choice)

