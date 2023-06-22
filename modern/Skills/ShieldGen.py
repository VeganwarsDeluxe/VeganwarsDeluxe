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

    def shield(self, source, target):
        self.cooldown_turn = source.session.turn + 5
        if target == source:
            target.session.say(f"🔵|{source.name} использует щит. Урон отражен!")
        else:
            target.session.say(f"🔵|{source.name} использует щит на {target.name}. Урон отражен!")

        @source.session.handlers.at(turn=source.session.turn, events='post-attack')
        def shield_block():
            for entity in source.session.entities:
                attack_target = entity.action.data.get('target')
                if not attack_target:
                    continue
                if attack_target != target:
                    continue
                damage = entity.action.data.get('damage')
                if not damage:
                    continue
                entity.action.data.update({'damage': 0})

    @property
    def actions(self):
        if self.source.session.turn < self.cooldown_turn:
            return []
        return [
            DecisiveAction(self.shield, self.source, target_type=Allies(),
                           name='Щит | Генератор', id='shield-gen', priority=-2)
        ]
