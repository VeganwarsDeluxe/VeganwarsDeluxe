from VegansDeluxe.core.Actions.StateAction import FreeStateAction
from VegansDeluxe.core import At
from VegansDeluxe.core import AttachedAction
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import Entity
from VegansDeluxe.core import PostDamageGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core import Allies


class Concentration(Skill):
    id = 'concentration'
    name = 'Концентрация'
    description = 'Вы можете попытаться нанести критический удар с определённым шансом ' \
                  '100%/75%/50%/25% для 1/2/3/4 соответственно, но за это теряете точность.'

    def __init__(self):
        super().__init__()
        self.multiplier = 1


@AttachedAction(Concentration)
class ShieldGenAction(FreeStateAction):
    id = 'concentration-x1'
    name = 'Щит | Генератор'
    target_type = Allies()
    priority = -10

    def __init__(self, session: Session, source: Entity, skill: Concentration):
        super().__init__(session, source, skill)
        self.state = skill

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
            context.event.damage = 0
