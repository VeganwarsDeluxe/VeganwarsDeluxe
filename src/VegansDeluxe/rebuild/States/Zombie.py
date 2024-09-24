from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import PreDamagesGameEvent, PreDeathGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import State


class ZombieState(State):
    id = 'zombie-state'

    def __init__(self):
        super().__init__()
        self.timer = 0
        self.active = False
        self.deactivations = 0


@RegisterState(ZombieState)
async def register(root_context: StateContext[ZombieState]):
    session: Session = root_context.session
    source = root_context.entity
    state = root_context.state

    @RegisterEvent(session.id, event=PreDamagesGameEvent)
    async def func(context: EventContext[PreDamagesGameEvent]):
        if not state.active:
            return
        if state.timer <= 0:
            state.active = False
            state.deactivations += 1
        state.timer -= 1

    @RegisterEvent(session.id, event=PreDeathGameEvent)
    async def func(context: EventContext[PreDeathGameEvent]):
        if context.event.entity != source:
            return
        if state.active:
            context.event.canceled = True
