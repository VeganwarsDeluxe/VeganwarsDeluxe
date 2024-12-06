from VegansDeluxe.core.Translator.LocalizedString import LocalizedString, ls


class Choice:
    def __init__(self,
                 choice_id: str,
                 text: str | LocalizedString = None,
                 result_text: str | LocalizedString = ls("")
                 ):
        self.id: str = choice_id
        self.question_id: str = ""

        self.text: str | LocalizedString \
            = text or ls("core.question.choice.base_text").format(self.question_id, self.id)

        self.result_text: str | LocalizedString \
            = result_text or ls("core.question.choice.base_text").format(self)
