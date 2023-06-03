from core.Skills.Skill import Skill
from core.Action import DecisiveAction
from core.TargetType import TargetType


class Thief(Skill):
    def __init__(self):
        super().__init__(id='thief', name='Вор', constant=True)

    def __call__(self, source):
        pass

    def steal(self, source, target):
        success = False
        for entity in source.session.alive_entities:
            if entity == source:
                continue
            for item in entity.using_items.copy():
                source.say(f'{entity.name} хотел использовать {item.name}, но я его украл!')
                success = True
                source.items.append(item)
                item.canceled = True
        if not success:
            source.say('У меня не получилось ничего украсть!')

    @property
    def actions(self):
        return [
            DecisiveAction(self.steal, name='Украсть предмет', id='steal', priority=-1, type=TargetType(ally=False))
        ]


