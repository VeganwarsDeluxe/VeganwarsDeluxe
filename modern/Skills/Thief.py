from core.Skills.Skill import Skill
from core.Action import DecisiveAction, FreeAction
from core.TargetType import TargetType, Enemies


class Thief(Skill):
    id = 'thief'
    name = 'Вор'
    description = 'Если применить эту способность на цель, которая применяет какой-либо предмет, вы ' \
                  'получите этот предмет. Дает +1 точности на дальнобойние оружия. (еще не дает)'

    def __init__(self, source):
        super().__init__(source, constant=True)
        self.cooldown_turn = 0

    @property
    def actions(self):
        if self.source.session.turn < self.cooldown_turn:
            return []
        return [
            Steal(self.source, self)
        ]


class Steal(FreeAction):
    id = 'steal'
    name = 'Украсть предмет'

    def __init__(self, source, skill):
        super().__init__(source, Enemies(), priority=-2)
        self.skill = skill

    def func(self, source, target):
        self.skill.cooldown_turn = source.session.turn + 0  # 3
        success = False
        for item in [item for item in target.item_queue]:
            success = True
            source.session.say(f'😏|{target.name} хотел использовать {item.name}, но вор {source.name} его украл!')
            target.item_queue.remove(item)
            source.items.append(item)
            item.source = source
            item.canceled = True
        if target.action.type == 'item':
            success = True
            source.session.say(f'😏|{target.name} хотел использовать '
                               f'{target.action.name}, но вор {source.name} его украл!')
            target.action.source = source
            source.items.append(target.action)
            target.action.canceled = True
        if not success:
            source.session.say(f'😒|Вору {source.name} не удается ничего украсть у {target.name}!')