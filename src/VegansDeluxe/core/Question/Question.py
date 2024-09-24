from uuid import uuid4

from VegansDeluxe.core.Question.Choice import Choice
from VegansDeluxe.core.Translator.LocalizedString import LocalizedString


class Question:
    def __init__(self, text: str | LocalizedString):
        self.id: str = str(uuid4().hex)[:6]
        self.text: str | LocalizedString = text
        self.choices: list[Choice] = []
