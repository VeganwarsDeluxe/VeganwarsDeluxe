from core.Actions.ActionManager import AttachedAction
from core.Actions.StateAction import DecisiveStateAction
from core.Entities import Entity
from core.Sessions import Session
from core.Skills.Skill import Skill
from core.TargetType import Everyone


class Mimic(Skill):
    id = 'mimic'
    name = 'Мимик'
    description = 'Если применить эту способность на цель, которая что то делает, вы ' \
                  'получите возможность его повторить!'

    def __init__(self, source):
        super().__init__(source)
        self.cooldown_turn = 0


@AttachedAction(Mimic)
class CopyAction(DecisiveStateAction):
    id = 'copyAction'
    name = 'Запомнить действие'
    priority = -2
    target_type = Everyone()

    def __init__(self, session: Session, source: Entity, skill: Mimic):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    def func(self, source, target):
        self.state.cooldown_turn = self.session.turn + 6
        success = False
        if target.action.type == 'action':
            success = True
            self.session.say(f'🎭|Мимик {source.name} запоминает действие {target.name}!')
            source.items.append(target.action)
        if not success:
            self.session.say(f'🎭|Мимику {source.name} не удается ничего скопировать у {target.name}!')
