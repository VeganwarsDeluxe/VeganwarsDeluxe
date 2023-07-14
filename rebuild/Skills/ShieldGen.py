from core.Actions.ActionManager import AttachedAction
from core.Actions.StateAction import DecisiveStateAction
from core.Entities import Entity
from core.Events.DamageEvents import PostDamageGameEvent
from core.Events.EventManager import event_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from core.TargetType import Allies


class ShieldGen(Skill):
    id = 'shield-gen'
    name = 'Генератор щитов'
    description = 'Вы получаете сгенерированный щит, работающий как обычный. Этот щит восстанавливается 5 ходов.'

    def __init__(self):
        super().__init__()
        self.cooldown_turn = 0


@AttachedAction(ShieldGen)
class ShieldGenAction(DecisiveStateAction):
    id = 'shield-gen'
    name = 'Щит | Генератор'
    target_type = Allies()
    priority = -2

    def __init__(self, session: Session, source: Entity, skill: ShieldGen):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    def func(self, source, target):
        self.state.cooldown_turn = self.session.turn + 5
        if target == source:
            self.session.say(f"🔵|{source.name} использует щит. Урон отражен!")
        else:
            self.session.say(f"🔵|{source.name} использует щит на {target.name}. Урон отражен!")

        @event_manager.now(self.session.id, event=PostDamageGameEvent)
        def shield_block(event: PostDamageGameEvent):
            if event.target != target:
                return
            if not event.damage:
                return
            self.session.say(f"🔵|Щит {source.name} заблокировал весь урон!")
            event.damage = 0
