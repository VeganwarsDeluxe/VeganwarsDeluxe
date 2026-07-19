from VegansDeluxe.core import PreDamagesGameEvent
from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import State
from VegansDeluxe.core import StateContext, EventContext


class Blindness(State):
    id = 'blindness'

    def __init__(self):
        super().__init__()
        self.until = 0


@RegisterState(Blindness)
async def register(root_context: StateContext[Blindness]):
    session: Session = root_context.session
    source = root_context.entity
    state = root_context.state

    @RegisterEvent(session.id, event=PreDamagesGameEvent, filters=[lambda e: state.until <= session.turn])
    async def func(context: EventContext[PreDamagesGameEvent]):
        source.outbound_accuracy_bonus += -1
