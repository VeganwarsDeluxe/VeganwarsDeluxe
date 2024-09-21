from VegansDeluxe.core import RegisterState
from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext, AttachedAction, FreeStateAction, Everyone, Entity
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls


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
class VisorAction(FreeStateAction):
    id = 'visor'
    name = ls("rebuild.skill.visor.action.name")
    target_type = Everyone()
    priority = -2

    def __init__(self, session: Session, source: Entity, state: Visor):
        super().__init__(session, source, state)
        self.state = state

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    async def func(self, source: Entity, target: Entity):
        self.state.cooldown_turn = self.session.turn + 3
        source.notifications.append(ls("rebuild.skill.visor.notification.name")
                                    .format(name=target.name))
        source.notifications.append(ls("rebuild.skill.visor.notification_hp")
                                    .format(hearts=target.hearts, hp=target.hp, max_hp=target.max_hp))
        source.notifications.append(ls("rebuild.skill.visor.notification_energy")
                                    .format(hearts=target.energies, hp=target.energy, max_hp=target.max_energy))
        source.notifications.append(ls("rebuild.skill.visor.hit_chance")
                                    .format(target.hit_chance))

