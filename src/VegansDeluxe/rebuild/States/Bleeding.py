from VegansDeluxe.core import PreDamagesGameEvent
from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import State
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core.Translator.LocalizedString import ls


class Bleeding(State):
    id = 'bleeding'

    def __init__(self):
        super().__init__()
        self.bleeding = 3
        self.active = False


@RegisterState(Bleeding)
async def register(root_context: StateContext[Bleeding]):
    session: Session = root_context.session
    source = root_context.entity
    state = root_context.state

    @RegisterEvent(session.id, event=PreDamagesGameEvent, filters=[lambda e: state.active])
    async def func(context: EventContext[PreDamagesGameEvent]):
        if state.bleeding <= 0:
            session.say(ls("rebuild.state.bleeding.hp_loss").format(source.name, source.hp - 1))
            source.hp -= 1
            state.active = False
            state.bleeding = 3
            return
        session.say(ls("rebuild.state.bleeding.timer").format(source.name, max(state.bleeding, 0)))
        state.bleeding -= 1
