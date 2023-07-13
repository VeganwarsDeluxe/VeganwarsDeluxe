from core.Actions.ActionManager import AttachedAction
from core.Actions.StateAction import DecisiveStateAction, FreeStateAction
from core.Entities import Entity
from core.Events.DamageEvents import PostDamageGameEvent
from core.Events.EventManager import event_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from core.TargetType import Allies


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

        @event_manager.now(self.session.id, event=PostDamageGameEvent)
        def shield_block(event: PostDamageGameEvent):
            if event.target != target:
                return
            if not event.damage:
                return
            event.damage = 0
