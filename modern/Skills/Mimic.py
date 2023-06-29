from core.Skills.Skill import Skill
from core.Action import DecisiveAction, FreeAction
from core.TargetType import TargetType, Enemies


class Mimic(Skill):
    id = 'mimic'
    name = 'Мимик'
    description = 'Если применить эту способность на цель, которая что то делает, вы ' \
                  'получите возможность его повторить!'

    def __init__(self, source):
        super().__init__(source)
        self.cooldown_turn = 0

    @property
    def actions(self):
        if self.source.session.turn < self.cooldown_turn:
            return []
        return [
            CopyAction(self.source, self)
        ]


class CopyAction(FreeAction):
    id = 'copyAction'
    name = 'Запомнить действие'

    def __init__(self, source, skill):
        super().__init__(source, Enemies(), priority=-2)
        self.skill = skill

    def func(self, source, target):
        self.skill.cooldown_turn = source.session.turn + 0
        success = False
        if target.action.type == 'action':
            success = True
            source.session.say(f'🎭|Мимик {source.name} запоминает действие {target.name}!')
            # target.action.source = source
            source.items.append(target.action)
        if not success:
            source.session.say(f'🎭|Мимику {source.name} не удается ничего скопировать у {target.name}!')
