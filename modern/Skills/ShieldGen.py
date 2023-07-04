from core.Actions.ActionManager import AttachedAction
from core.Actions.StateAction import FreeStateAction
from core.Entities import Entity
from core.Events.Events import PostAttackGameEvent
from core.Sessions import Session
from core.Skills.Skill import Skill
from core.TargetType import Allies


class ShieldGen(Skill):
    id = 'shield-gen'
    name = 'Генератор щитов'
    description = 'Вы получаете сгенерированный щит, работающий как обычный. Этот щит восстанавливается 5 ходов.'

    def __init__(self, source):
        super().__init__(source)
        self.cooldown_turn = 0


@AttachedAction(ShieldGen)
class ShieldGenAction(FreeStateAction):
    id = 'shield-gen'
    name = 'Щит | Генератор'
    target_type = Allies()

    def __init__(self, session: Session, source: Entity, skill: ShieldGen):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    def func(self, source, target):
        self.state.cooldown_turn = self.session.turn + 5
        if target == source:
            target.session.say(f"🔵|{source.name} использует щит. Урон отражен!")
        else:
            target.session.say(f"🔵|{source.name} использует щит на {target.name}. Урон отражен!")

        @self.event_manager.now(self.session.id, event=PostAttackGameEvent)
        def shield_block(event: PostAttackGameEvent):
            if event.target != target:
                return
            if not event.damage:
                return
            event.damage = 0
