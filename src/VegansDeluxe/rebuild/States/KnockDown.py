from VegansDeluxe.core.Actions.StateAction import DecisiveStateAction
from VegansDeluxe.core import AttachedAction, ActionTag
from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import Entity
from VegansDeluxe.core import PostUpdateActionsGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import State
from VegansDeluxe.core import OwnOnly
from VegansDeluxe.core.Translator.LocalizedString import ls


class Knockdown(State):
    id = 'knockdown'

    def __init__(self):
        super().__init__()
        self.active = False


@RegisterState(Knockdown)
async def register(root_context: StateContext[Knockdown]):
    session: Session = root_context.session
    source = root_context.entity
    state = root_context.state

    @RegisterEvent(session.id, event=PostUpdateActionsGameEvent)
    async def func(context: EventContext[PostUpdateActionsGameEvent]):
        if not state.active:
            return

        context.action_manager.remove_actions_by_tag(session, source, ActionTag.ATTACK)
        context.action_manager.remove_action(session, source, 'dodge')


@AttachedAction(Knockdown)
class StandUp(DecisiveStateAction):
    id = 'stand_up'
    name = ls("state_knockdown_name")
    target_type = OwnOnly()

    def __init__(self, session: Session, source: Entity, skill: Knockdown):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return not self.state.active

    async def func(self, source, target):
        self.state.active = False
        self.session.say(ls("state_knockdown_text").format(source.name))
