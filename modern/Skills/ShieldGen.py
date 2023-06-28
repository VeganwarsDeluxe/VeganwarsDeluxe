from core.Skills.Skill import Skill
from core.Action import DecisiveAction
from core.TargetType import TargetType, Enemies, Allies


class ShieldGen(Skill):
    id = 'shield-gen'
    name = 'Генератор щитов'
    description = 'Вы получаете сгенерированный щит, работающий как обычный. Этот щит восстанавливается 5 ходов.'

    def __init__(self, source):
        super().__init__(source, constant=True)

        self.cooldown_turn = 0

    @property
    def actions(self):
        if self.source.session.turn < self.cooldown_turn:
            return []
        return [
            ShieldGenAction(self.source, self)
        ]


class ShieldGenAction(DecisiveAction):
    id = 'shield-gen'
    name = 'Щит | Генератор'

    def __init__(self, source, skill):
        super().__init__(source, Allies(), priority=-2)
        self.skill = skill

    def func(self, source, target):
        self.skill.cooldown_turn = source.session.turn + 5
        if target == source:
            target.session.say(f"🔵|{source.name} использует щит. Урон отражен!")
        else:
            target.session.say(f"🔵|{source.name} использует щит на {target.name}. Урон отражен!")

        @source.session.event_manager.at(turn=source.session.turn, events='post-attack')
        def shield_block(message):
            attack = source.session.event.action
            if not attack.target:
                return
            if attack.target != target:
                return
            damage = attack.data.get('damage')
            if not damage:
                return
            attack.data.update({'damage': 0})
