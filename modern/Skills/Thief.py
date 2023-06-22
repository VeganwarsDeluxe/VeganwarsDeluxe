from core.Skills.Skill import Skill
from core.Action import DecisiveAction
from core.TargetType import TargetType, Enemies


class Thief(Skill):
    def __init__(self, source):
        super().__init__(source, id='thief', name='Вор', constant=True)
        self.description = 'Если применить эту способность на цель, которая применяет какой-либо предмет, вы ' \
                           'получите этот предмет. Дает +1 точности на дальнобойние оружия. (еще не дает)'

    def __call__(self):
        pass

    def steal(self, source, target):
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

    @property
    def actions(self):
        return [
            DecisiveAction(self.steal, self.source, target_type=Enemies(),
                           name='Украсть предмет', id='steal', priority=-2)
        ]


