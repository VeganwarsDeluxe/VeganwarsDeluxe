from VegansDeluxe.core import AttachedAction
from VegansDeluxe.core.Actions.StateAction import DecisiveStateAction
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import At
from VegansDeluxe.core import Entity
from VegansDeluxe.core import PostDamageGameEvent

from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core import Allies


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

        @At(self.session.id, turn=self.session.turn, event=PostDamageGameEvent)
        def shield_block(context: EventContext[PostDamageGameEvent]):
            if context.event.target != target:
                return
            if not context.event.damage:
                return
            self.session.say(f"🔵|Щит {source.name} заблокировал весь урон!")
            context.event.damage = 0
