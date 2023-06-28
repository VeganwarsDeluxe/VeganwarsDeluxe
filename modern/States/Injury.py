from core.States.State import State


class Injury(State):
    id = 'injury'

    def __init__(self, source):
        super().__init__(source, constant=True)
        self.injury = 0

    def __call__(self):
        source = self.source
        if source.session.event.top != 'attack':
            return
        if not self.injury:
            return
        damage = 0
        entity = source
        for entity in source.session.entities:
            if entity.action.data.get('target') == source:
                damage = entity.action.data.get('damage')
                break
            return
        if damage == 0:
            return
        # source.say(f'От ранения урон увеличен c {damage} до {damage + self.injury}!')
        entity.action.data.update({'damage': damage + self.injury})



