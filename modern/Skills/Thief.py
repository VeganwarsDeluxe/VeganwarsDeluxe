from core.Actions.ActionManager import AttachedAction
from core.Actions.StateAction import DecisiveStateAction
from core.Entities import Entity
from core.Sessions import Session
from core.Skills.Skill import Skill
from core.TargetType import Enemies


class Thief(Skill):
    id = 'thief'
    name = 'Вор'
    description = 'Если применить эту способность на цель, которая применяет какой-либо предмет, вы ' \
                  'получите этот предмет. Дает +1 точности на дальнобойние оружия. (еще не дает)'

    def __init__(self, source):
        super().__init__(source)
        self.cooldown_turn = 0


@AttachedAction(Thief)
class Steal(DecisiveStateAction):
    id = 'steal'
    name = 'Украсть предмет'
    priority = -2
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, skill: Thief):
        super().__init__(session, source, skill)
        self.state = skill

    def func(self, source, target):
        self.state.cooldown_turn = self.session.turn + 3
        success = False
        for item in [item for item in target.item_queue]:
            success = True
            self.session.say(f'😏|{target.name} хотел использовать {item.name}, но вор {source.name} его украл!')
            target.item_queue.remove(item)
            source.items.append(item)
            item.source = source
            item.canceled = True
        if target.action.type == 'item':
            success = True
            self.session.say(f'😏|{target.name} хотел использовать '
                             f'{target.action.name}, но вор {source.name} его украл!')
            target.action.source = source
            source.items.append(target.action)
            target.action.canceled = True
        if not success:
            self.session.say(f'😒|Вору {source.name} не удается ничего украсть у {target.name}!')
