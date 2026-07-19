from VegansDeluxe.core import RegisterState
from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext, AttachedAction, Everyone, Entity
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild.States.Info import InfoAction


class Visor(Skill):
    id = 'visor'
    name = ls("rebuild.skill.visor.name")
    description = ls("rebuild.skill.visor.description")

    def __init__(self):
        super().__init__()
        self.cooldown_turn = 0


@RegisterState(Visor)
async def register(root_context: StateContext[Visor]):
    session: Session = root_context.session
    source = root_context.entity


@AttachedAction(Visor)
class VisorAction(InfoAction):
    id = 'visor'
    name = ls("rebuild.skill.visor.action.name")
    target_type = Everyone()

    def __init__(self, session: Session, source: Entity, state: Visor):
        super().__init__(session, source, state)
        self.state: Visor = state

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    async def func(self, source: Entity, target: Entity):
        await super().func(source, target)
        self.state.cooldown_turn = self.session.turn + 3
