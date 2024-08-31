from VegansDeluxe.core import GameEvent
from VegansDeluxe.core.Question.Question import Question


class QuestionGameEvent(GameEvent):
    """
    Published when game needs to request a choice from the entity.
    """

    def __init__(self, session_id, turn, entity_id, question: Question):
        super().__init__(session_id, turn)

        self.entity_id = entity_id
        self.question = question


class AnswerGameEvent(GameEvent):
    """
    Published when entity sends a response to the question.
    """

    def __init__(self, session_id, turn, entity_id, question: Question, choice_id: str):
        super().__init__(session_id, turn)
        self.entity_id = entity_id
        self.question = question
        self.choice_id = choice_id
