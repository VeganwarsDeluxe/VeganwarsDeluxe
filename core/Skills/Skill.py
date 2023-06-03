class Skill(object):
    def __init__(self, id=None, name='None', constant=False, stage='pre-action'):
        self.id = id
        self.name = name
        self.constant = constant
        self.stage = stage

    @property
    def actions(self):
        return []

    def __call__(self, source):
        pass
