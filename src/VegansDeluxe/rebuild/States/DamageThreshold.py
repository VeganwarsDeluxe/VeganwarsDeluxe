from VegansDeluxe.core import HPLossGameEvent
from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import State
from VegansDeluxe.core import StateContext, EventContext


class DamageThreshold(State):
    id = 'damage-threshold'

    def __init__(self):
        super().__init__()
        self.threshold = 6


@RegisterState(DamageThreshold)
async def register(root_context: StateContext[DamageThreshold]):
    session: Session = root_context.session
    state = root_context.state
    source = root_context.entity

    @RegisterEvent(session.id, event=HPLossGameEvent)
    async def func(context: EventContext[HPLossGameEvent]):
        if not context.event.damage:
            return
        if context.event.source != source.id:
            return
        context.event.hp_loss = (context.event.damage // max(state.threshold, 1)) + 1
