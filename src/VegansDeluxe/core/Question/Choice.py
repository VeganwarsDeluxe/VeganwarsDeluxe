from VegansDeluxe.core.Translator.LocalizedString import LocalizedString


class Choice:
    def __init__(self, choice_id: str, text: str | LocalizedString):
        self.id: str = choice_id
        self.text = text
