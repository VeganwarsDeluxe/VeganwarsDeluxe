from core.Context import Context
from core.Decorators import RegisterEvent, RegisterState
from core.Actions.ActionManager import AttachedAction, action_manager
from core.Actions.ItemAction import ItemAction
from core.Actions.StateAction import DecisiveStateAction
from core.Entities import Entity
from core.Events.EventManager import event_manager
from core.Events.Events import AttachStateEvent, PreActionsGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from core.TargetType import Enemies


class Thief(Skill):
    id = 'thief'
    name = 'Вор'
    description = 'Если применить эту способность на цель, которая применяет какой-либо предмет, вы ' \
                  'получите этот предмет. Дает +1 точности на дальнобойние оружия.'

    def __init__(self):
        super().__init__()
        self.cooldown_turn = 0


@RegisterState(Thief)
def register(root_context: Context[AttachStateEvent]):
    session: Session = root_context.session
    source = session.get_entity(root_context.event.entity_id)

    @RegisterEvent(session.id, event=PreActionsGameEvent)
    def func(context: Context[PreActionsGameEvent]):
        if source.weapon.ranged:
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
