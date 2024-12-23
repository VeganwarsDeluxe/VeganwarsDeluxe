from VegansDeluxe.core import PostUpdatesGameEvent, PostDamagesGameEvent
from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import State
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core.Events.MatchEvents import ChooseActionEvent
from VegansDeluxe.core.Translator.LocalizedString import ls


class Stun(State):
    id = 'stun'

    def __init__(self):
        super().__init__()
        self.stun = 0


@RegisterState(Stun)
async def register(root_context: StateContext[Stun]):
    session: Session = root_context.session
    source = root_context.entity
    state = root_context.state

    @RegisterEvent(session.id, event=PostUpdatesGameEvent)
    async def func(context: EventContext[PostUpdatesGameEvent]):
        if not state.stun:
            return
        for action in context.action_manager.get_actions(session, source):
            if action.id != 'lay_stun':
                action.removed = True

    @RegisterEvent(session.id, event=PostDamagesGameEvent)
    async def func(context: EventContext[PostDamagesGameEvent]):
        if not state.stun:
            return
        if state.stun == 1:
            session.say(ls("rebuild.state.stun.wake_up").format(source.name))
        state.stun -= 1

    @RegisterEvent(session.id, event=ChooseActionEvent, priority=-1)
    async def handle_choose_action_call(context: EventContext[ChooseActionEvent]):
        if source.id != context.event.entity_id or state.stun == 0:
            return
        context.event.canceled = True
