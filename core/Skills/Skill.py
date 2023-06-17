from core.States.State import State


class Skill(State):
    def __init__(self, source, id=None, name='None', constant=False, stage='pre-action'):
        super().__init__(source, id, name, constant, stage)

        self.description = 'Информация еще не написана.'
