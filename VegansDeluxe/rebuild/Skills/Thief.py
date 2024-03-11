from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import RegisterEvent, RegisterState, Nearest
from VegansDeluxe.core import AttachedAction
from VegansDeluxe.core import ItemAction
from VegansDeluxe.core.Actions.StateAction import DecisiveStateAction
from VegansDeluxe.core import Entity

from VegansDeluxe.core import PreActionsGameEvent, DeliveryRequestEvent, DeliveryPackageEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core import Enemies


class Thief(Skill):
    id = 'thief'
    name = 'Вор'
    description = 'Если применить эту способность на цель, которая применяет какой-либо предмет, вы ' \
                  'получите этот предмет. Дает +1 точности на дальнобойние оружия.'

    def __init__(self):
        super().__init__()
        self.cooldown_turn = 0


@RegisterState(Thief)
def register(root_context: StateContext[Thief]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, event=PreActionsGameEvent)
    def func(context: EventContext[PreActionsGameEvent]):
        if source.weapon and source.weapon.ranged:
            source.outbound_accuracy_bonus += 1


@AttachedAction(Thief)
class Steal(DecisiveStateAction):
    id = 'steal'
    name = 'Украсть предмет'
    priority = -3
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, skill: Thief):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    def func(self, source, target):
        @Nearest(self.session.id, event=DeliveryPackageEvent)
        def delivery(context: EventContext[DeliveryPackageEvent]):
            action_manager = context.action_manager

            self.state.cooldown_turn = self.session.turn + 3
            success = False
            for action in action_manager.action_queue:
                if action.type != 'item':
                    continue
                action: ItemAction
                if action.source != target:
                    continue
                item = action.item
                if action.canceled:
                    continue
                action.canceled = True

                self.session.say(f'😏|{target.name} хотел использовать {item.name}, но вор {source.name} его украл!')
                source.items.append(item)

                success = True
            if not success:
                self.session.say(f'😒|Вору {source.name} не удается ничего украсть у {target.name}!')

        self.event_manager.publish(DeliveryRequestEvent(self.session.id, self.session.turn))


